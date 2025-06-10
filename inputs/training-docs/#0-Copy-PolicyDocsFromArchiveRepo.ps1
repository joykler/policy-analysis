using namespace Microsoft.PowerShell.Commands
using namespace System.Net


$InformationPreference = 'Continue'
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'Ignore'

$PSDefaultParameterValues = @{
    'Write-Verbose:Verbose' = $true

    'Add-Member:MemberType' = 'ScriptMethod'
    'Add-Member:PassThru'   = $true
}

$PSStyle.OutputRendering = 'Ansi'



#region -- Declare: $Logging --
$global:Logging = [PSCustomObject]::new()
& {
    function Add-LoggingMethod([string] $Name, [scriptblock] $Method) {

        $global:Logging = $global:Logging | Add-Member -Name $Name -Value $Method
    }



    Add-LoggingMethod 'BatchProcess_Invoked' -Method {

        param([int] $BatchNr, [int] $BatchedItems)

        $S = $PSStyle.Foreground.BrightBlue + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " ! Batch process invoked: $F [BatchNr: $BatchNr; BatchedItems: $BatchedItems]..." + $R)
    }

    Add-LoggingMethod 'Process_Started' -Method {

        $S = $PSStyle.Foreground.BrightWhite + $PSStyle.Bold + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Started copying policy-docs from archive-repo...' + $R)
    }

    Add-LoggingMethod 'EachDoc_Copying_Started' -Method {

        param($file)

        $S = $PSStyle.Foreground.White
        $F = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Copying policy-doc from archive-repo: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R)
    }

    Add-LoggingMethod 'EachDoc_Copying_Failed' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightRed + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed copying policy-doc from file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R + "`n$err")
    }

    Add-LoggingMethod 'EachDoc_CreatingTargetDir' -Method {

        param($file)

        $S = $PSStyle.Foreground.Magenta
        $F = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Creating policy-doc target folder: $F[ $($file.LoggedDir) ]" + $R)
    }

    Add-LoggingMethod 'EachDoc_WarnTargetFileExists' -Method {

        param($file)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Target-file allready exists: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R)
    }

}
#endregion

#region -- Declare: Initialize-BatchProcess --
function Initialize-BatchProcess ([int] $Size = 30, [scriptblock] $OnProcess) {

    $Batch = [PSCustomObject] @{
        Size      = $Size
        OnProcess = $OnProcess

        Number    = 0
        Items     = [System.Collections.Generic.List[PSCustomObject]]::new($Size)
    }

    $Batch = $Batch | Add-Member -Name 'ForEachItem' -Value {

        param([PSCustomObject] $Item)

        $this.Items.Add($Item)

        if ($this.Items.Count -ge $this.Size) {
            $this.FlushItems()
        }
    }

    $Batch = $Batch | Add-Member -Name 'FlushItems' -Value {

        if ($this.Items.Count -gt 0) {

            $this.Number++

            $global:Logging.BatchProcess_Invoked($this.Number, $this.Items.Count)
            $this.OnProcess.Invoke($this.Number, $this.Items)

            $this.Items.Clear()
        }
    }

    return $Batch
}
#endregion



#region -- Declare: Get-TargetInfoFromSourceFile --
function Get-TargetInfoFromSourceFile {

    [CmdletBinding()]
    param(
        [Alias('FullName')]
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [string] $SourcePath,

        [Parameter(Mandatory, Position = 1)]
        [string] $SourceRootPath,

        [Parameter(Mandatory)]
        [string] $TargetRootPath
    )

    begin {
        function Get-FileInfo([string] $FilePath, [string] $LoggedDir) {
            return [PSCustomObject] @{
                Name      = [System.IO.Path]::GetFileName($FilePath)
                Folder    = [System.IO.Path]::GetDirectoryName($FilePath)
                Path      = $FilePath

                LoggedDir = $LoggedDir
            }
        }
    }

    process {
        $RelFilePath = [System.IO.Path]::GetRelativePath($SourceRootPath, $SourcePath)

        $TargetPath = Join-Path $TargetRootPath -ChildPath $RelFilePath

        [PSCustomObject] @{
            SourceFile = Get-FileInfo $SourcePath -LoggedDir $RelFilePath
            TargetFile = Get-FileInfo $TargetPath -LoggedDir $RelFilePath
        }
    }
}
#endregion

#region -- Declare: Copy-PolicyDocFromArchiveRepo --
function Copy-PolicyDocFromArchiveRepo {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $SourceFile,

        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $TargetFile
    )

    process {
        if ($(Test-Path $TargetFile.Path -PathType Leaf)) {
            $Logging.EachDoc_WarnTargetFileExists($TargetFile)

        } else {
            $Logging.EachDoc_Copying_Started($SourceFile)

            try {
                if (-not $(Test-Path $TargetFile.Folder -PathType Container)) {
                    $Logging.EachDoc_CreatingTargetDir($TargetFile)
                    mkdir $TargetFile.Folder | Out-Null
                }

                Copy-Item $SourceFile.Path -Destination $TargetFile.Path

                Write-Output $TargetFile

            } catch {
                $Logging.EachDoc_Copying_Failed($TargetFile, $_)
            }
        }
    }
}
#endregion



try {
    Push-Location "$PSScriptRoot\..\.." # Set to repo root

    $BatchProc = Initialize-BatchProcess -Size 300 -OnProcess {

        param([int] $BatchNr, [object[]] $BatchedItems)

        git add --all
        git commit -m "Added batch of copyied policy-docs from archive-repo #$BatchNr"
        git push
    }



    $SourceRootPath = "$(Resolve-Path '..\policy-evaluation-2\policy-documents\Archive')"

    $TargetRootPaths = @{
        2015 = "$(Resolve-Path 'inputs\training-docs\policy\all-from-2015')"
        2023 = "$(Resolve-Path 'inputs\training-docs\policy\all-from-2023')"
    }



    $Logging.Process_Started()

    foreach ($current in $TargetRootPaths.GetEnumerator()) {
        Get-ChildItem -Path $SourceRootPath -Directory |
            Where-Object Name -In @(
                'kamerstukken',
                'rapporten',
                'publicaties',
                'jaarverslagen',
                'beleidsnotas'
            ) |
            Get-ChildItem -Directory |
            Where-Object Name -EQ $current.Key |
            Get-ChildItem -Filter *.pdf -File -Recurse |
            Get-TargetInfoFromSourceFile $SourceRootPath -TargetRootPath $current.Value |
            Copy-PolicyDocFromArchiveRepo |
            ForEach-Object {
                $BatchProc.ForEachItem($PSItem)
            }

        $BatchProc.FlushItems()
    }

} finally {
    Pop-Location
}
