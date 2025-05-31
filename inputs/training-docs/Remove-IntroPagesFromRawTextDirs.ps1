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



    Add-LoggingMethod 'Info_BatchProcessInvoked' -Method {

        param([int] $BatchNr, [int] $BatchedItems)

        $S = $PSStyle.Foreground.BrightBlue + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " ! Batch process invoked: $F [BatchNr: $BatchNr; BatchedItems: $BatchedItems]..." + $R)
    }

    Add-LoggingMethod 'Info_StartedRemovingIntroPages' -Method {

        $S = $PSStyle.Foreground.BrightWhite + $PSStyle.Bold + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Started removing intro-pages from all raw-text-dirs...' + $R)
    }

    Add-LoggingMethod 'Info_RemovingIntroPagesFrom' -Method {

        param($file)

        $S = $PSStyle.Foreground.Green + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Removing intro-pages from raw-text-dir: $F[ $($file.Folder) ]" + $R)
    }

    Add-LoggingMethod 'Warn_FirstRawTextPageNotExists' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed removing intro-pages from raw-text-dir: $F[ $($file.Folder) ]" + $R + "`n$err")
    }

    Add-LoggingMethod 'Warn_RemovingIntroPagesFailed' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed removing intro-pages from raw-text-dir: $F[ $($file.Folder) ]" + $R + "`n$err")
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

        if ($this.Items.Count -ge 0) {

            $this.Number++

            $global:Logging.Info_BatchProcessInvoked($this.Number, $this.Items.Count)
            $this.OnProcess.Invoke($this.Number, $this.Items)

            $this.Items.Clear()
        }
    }

    return $Batch
}
#endregion



#region -- Declare: Get-FileInfo --
function Get-FileInfo {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory, Position = 1)]
        [string] $FilePath,

        [Parameter(Mandatory)]
        [string] $LoggedDir
    )

    return [PSCustomObject] @{
        Name      = [System.IO.Path]::GetFileName($FilePath)
        Folder    = [System.IO.Path]::GetDirectoryName($FilePath)
        Path      = $FilePath
        LoggedDir = $LoggedDir
    }
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
        [string] $SourceRootPath
    )

    process {
        $SourceDir = [System.IO.Path]::GetDirectoryName($SourcePath)
        $RelFilePath = [System.IO.Path]::GetRelativePath($SourceRootPath, $SourceDir)

        $TargetDir = [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
        $TargetPath = Join-Path $SourceDir -ChildPath $TargetDir -AdditionalChildPath '{0:D4}.raw.txt'

        [PSCustomObject] @{
            SourceFile = Get-FileInfo $SourcePath -LoggedDir $RelFilePath
            TargetFile = Get-FileInfo $TargetPath -LoggedDir $RelFilePath
        }
    }
}
#endregion

#region -- Declare: Remove-IntroPagesFromSourceFile --
function Remove-IntroPagesFromSourceFile {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $SourceFile,

        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $TargetFile,

        [switch] $OnlyUpdateExistingPages
    )

    begin {
        function Get-RawTextPageFileInfo([int] $PageNr) {
            Get-FileInfo $($TargetFile.Path -f $PageNr) -LoggedDir $TargetFile.LoggedDir
        }

        function Test-FileExists([PSCustomObject] $FileInfo) {

            Test-Path $FileInfo.Path -PathType Leaf
        }

        function Test-IntroPage([int] $PageNr) {

        }
    }

    process {
        $Logging.Info_RemovingIntroPagesFrom($SourceFile)

        try {
            $FirstPageFile = Get-RawTextPageFileInfo -PageNr 1
            if (-not $(Test-FileExists $FirstPageFile)){

            }
            Remove-IntroPages $Source_PdfReader

        } catch {
            $Logging.Warn_RemovingIntroPagesFailed($TargetFile, $_)
        }
    }
}
#endregion



try {
    Push-Location "$PSScriptRoot\..\.." # Set to repo root

    $BatchProc = Initialize-BatchProcess -Size 300 -OnProcess {

        param([int] $BatchNr, [object[]] $BatchedItems)

        git add --all
        git commit -m "Added batch of removing intro-pages from raw-text dirs #$BatchNr"
        git push
    }



    $Logging.Info_StartedRemovingIntroPages()
    Get-ChildItem -Path $PSScriptRoot -Filter *.pdf -File -Recurse |
        Get-TargetInfoFromSourceFile -SourceRootPath $PSScriptRoot |
        Remove-IntroPagesFromSourceFile -OnlyUpdateExistingPages |
        ForEach-Object {
            $BatchProc.ForEachItem($PSItem)
        }

    $BatchProc.FlushItems()

} finally {
    Pop-Location
}
