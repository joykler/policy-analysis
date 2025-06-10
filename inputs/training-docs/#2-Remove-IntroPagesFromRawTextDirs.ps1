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

        Write-Information $($S + 'Started removing intro-pages from all raw-text-dirs...' + $R)
    }

    Add-LoggingMethod 'RawTextDir_Removing_Skipped' -Method {

        param($file)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Skipped removing intro-pages from raw-text-dir: $F[ $($file.LoggedDir) ]" + $R)
    }

    Add-LoggingMethod 'RawTextDir_Removing_Started' -Method {

        param($file)

        $S = $PSStyle.Foreground.BrightCyan + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Started removing intro-pages from raw-text-dir: $F[ $($file.LoggedDir) ]" + $R)
    }

    Add-LoggingMethod 'RawTextDir_Removing_Finished' -Method {

        param($file, $TotalRemoved)

        $S = $PSStyle.Foreground.Green + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + "   Stopped removing intro-pages from raw-text-dir: $F[ $($file.LoggedDir) ]> #$TotalRemoved" + $R + "`n")
    }

    Add-LoggingMethod 'RawTextDir_Removing_Failed' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightRed + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed removing intro-pages from raw-text-dir: $F[ $($file.LoggedDir) ]" + $R + "`n$err")
    }

    Add-LoggingMethod 'RawTextDir_Removing_IntroPage' -Method {

        param($file, $pageNr)

        $S = $PSStyle.Foreground.Cyan
        $F = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + "    - Removed intro-page number from raw-text-dir: $F[ $($file.LoggedDir) ]]> #$pageNr" + $R)
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
        $SourceDir_AbsPath = [System.IO.Path]::GetDirectoryName($SourcePath)
        $SourceDir_RelPath = [System.IO.Path]::GetRelativePath($SourceRootPath, $SourceDir_AbsPath)

        $TargetDir_Name = [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
        $TargetDir_AbsPath = Join-Path $SourceDir_AbsPath -ChildPath $TargetDir_Name
        $TargetDir_RelPath = Join-Path $SourceDir_RelPath -ChildPath $TargetDir_Name

        $TargetPath = Join-Path $TargetDir_AbsPath -ChildPath '{0:D4}.raw.txt'

        [PSCustomObject] @{
            SourceFile = Get-FileInfo $SourcePath -LoggedDir $SourceDir_RelPath
            TargetFile = Get-FileInfo $TargetPath -LoggedDir $TargetDir_RelPath
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
            Test-Path -LiteralPath $FileInfo.Path -PathType Leaf
        }

        function Select-AllMatches ([string] $Pattern) {
            $Input |
                Select-String -Pattern $Pattern -AllMatches |
                ForEach-Object {
                    $_.Matches.Value
                }
        }

        function Test-IntroPage([PSCustomObject] $FileInfo) {

            if (-not $(Test-FileExists $FileInfo)) {
                return $false
            }

            $Text = "$(Get-Content -LiteralPath $FileInfo.Path -Raw)".Trim().Normalize()

            $Text = $Text -replace '[^\d\w\s]+', '' # Strip all chars (which are not number, word or whitespace)
            $Text = $Text -replace '[\s-[ \n]]', '' # Replace any whitespace char (which is not space or new-line) with a space
            $Text = $Text -replace '[ ]+', ' '      # Replace multiple to single: space
            $Text = $Text -replace '[\n]+', "`n"    # Replace multiple to single: new-line

            # Scan text as block for ratio numbers vs words
            $Block_Text = $Text -replace '\s+', ' '
            $Block_Numbers = @($Block_Text | Select-AllMatches '[\d]+')
            $Block_Words = @($Block_Text | Select-AllMatches '[\w]{4,}')
            $Block_Total = $Block_Numbers.Count + $Block_Words.Count
            $Block_NumbersRatio = 100.0 * $Block_Numbers.Count / $Block_Total

            # Scan text as lines for ratio index-like lines (def. as: starts or ends with a number)
            $Lines = @($Text -split '\n' | ForEach-Object { "$_".Trim() } | Where-Object { "$_".Length })
            $Lines_LikeIndex = @($Lines | Where-Object { "$_" -match '((^\d+)|(\d+$))' })
            $Lines_LikeIndexRatio = 100.0 * $Lines_LikeIndex.Count / $Lines.Count

            if ($Block_Words.Count -le 10 -or $Lines.Count -le 5) {
                return $true
            }

            if ($Block_NumbersRatio -gt 10 -or $Lines_LikeIndexRatio -gt 50) {
                return $true
            }

            return $false
        }
    }

    process {

        try {
            $FirstPageFile = Get-RawTextPageFileInfo -PageNr 1
            if (-not $(Test-FileExists $FirstPageFile)) {
                $Logging.RawTextDir_Removing_Skipped($TargetFile)
                return
            }

            $Logging.RawTextDir_Removing_Started($TargetFile)

            $PageMax = @(Get-ChildItem -Path $TargetFile.Folder -Filter '*.raw.txt' -File).Count
            $Current = [PSCustomObject]@{
                PageNr   = 1
                PageFile = $FirstPageFile
                Removed  = 0
            }

            while ($($Current.PageNr -le $PageMax) -and $(Test-IntroPage $Current.PageFile)) {

                Remove-Item -LiteralPath $Current.PageFile.Path
                $Logging.RawTextDir_Removing_IntroPage($TargetFile, $Current.PageNr)

                Write-Output $Current.PageFile

                $Current.PageNr++
                $Current.PageFile = Get-RawTextPageFileInfo $Current.PageNr
                $Current.Removed++
            }

            $Logging.RawTextDir_Removing_Finished($TargetFile, $Current.Removed)

        } catch {
            $Logging.RawTextDir_Removing_Failed($TargetFile, $_)
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



    $Logging.Process_Started()
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
