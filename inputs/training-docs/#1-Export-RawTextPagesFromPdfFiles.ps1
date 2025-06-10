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

        Write-Information $($S + 'Started exporting raw-text pages from all pdf-files...' + $R)
    }

    Add-LoggingMethod 'EachPdf_Exporting_Started' -Method {

        param($file)

        $S = $PSStyle.Foreground.White
        $F = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Exporting raw-text pages from pdf-file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R)
    }

    Add-LoggingMethod 'EachPdf_Exporting_Failed' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightRed + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed exporting raw-text pages from pdf-file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R + "`n$err")
    }

    Add-LoggingMethod 'EachPdf_WarnRawTextDirExists' -Method {

        param($file)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Raw-text folder allready exists: $F[ $($file.LoggedDir) ]" + $R)
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

#region -- Declare: Initialize-PdfImporting --
function Initialize-PdfImporting() {

    $Logging.LibInit_PdfImporting_Started()

    Add-Type -Path "$PSScriptRoot\.lib\BouncyCastle.Cryptography\lib\net6.0\BouncyCastle.Cryptography.dll"
    Add-Type -Path "$PSScriptRoot\.lib\iTextSharp\itextsharp.dll"

    $Logging.LibInit_PdfImporting_Finished()
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

#region -- Declare: Export-RawTextPagesFromSourceFile --
function Export-RawTextPagesFromSourceFile {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $SourceFile,

        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $TargetFile,

        [switch] $OnlyUpdateExistingPages
    )

    begin {
        function Export-RawTextPages([iTextSharp.text.pdf.PdfReader] $Source_PdfReader) {

            $PageMax = $Source_PdfReader.NumberOfPages
            for ($PageNr = 1; $PageNr -le $PageMax; $PageNr++) {

                $TargetPageFile = Get-FileInfo $($TargetFile.Path -f $PageNr) -LoggedDir $TargetFile.LoggedDir
                $TargetPageFileExists = Test-Path $TargetPageFile.Path -PathType Leaf

                if (($OnlyUpdateExistingPages.IsPresent -and $TargetPageFileExists) -or -not $OnlyUpdateExistingPages.IsPresent) {

                    $TargetPageText = [iTextSharp.text.pdf.parser.PdfTextExtractor]::GetTextFromPage($Source_PdfReader, $PageNr).Trim()

                    foreach ($EndOfPage in $("$PageNr", "([\p{P}]+)$PageNr([\p{P}]+)", "([\s\p{P}]+)$PageNr([\s\p{P}]+)")) {
                        if ($TargetPageText -match "($EndOfPage)\Z") {
                            $TargetPageText = "$($TargetPageText -replace "($EndOfPage)\Z")".Trim()
                        }
                    }

                    if ($(Get-Content -Path $TargetPageFile.Path -Raw).Trim() -ne $TargetPageText) {
                        Set-Content -Path $TargetPageFile.Path -Value $TargetPageText

                        Write-Output $TargetPageFile
                    }
                }
            }
        }
    }

    process {
        $TargetFolderExists = Test-Path $TargetFile.Folder -PathType Container
        if ($TargetFolderExists -and -not $OnlyUpdateExistingPages.IsPresent) {
            $Logging.EachPdf_WarnRawTextDirExists($TargetFile)

        } else {
            $Logging.EachPdf_Exporting_Started($SourceFile)

            try {
                if (-not $TargetFolderExists) {
                    mkdir $TargetFile.Folder -Force | Out-Null
                }

                $Source_PdfReader = [iTextSharp.text.pdf.PdfReader]::new($SourceFile.Path)

                Export-RawTextPages $Source_PdfReader

            } catch {
                $Logging.EachPdf_Exporting_Failed($TargetFile, $_)
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
        git commit -m "Added batch of extracted raw-text files from pdf files #$BatchNr"
        git push
    }



    Initialize-PdfImporting



    $Logging.Process_Started()

    Get-ChildItem -Path "$PSScriptRoot" -Filter *.pdf -File -Recurse |
        Get-TargetInfoFromSourceFile -SourceRootPath $PSScriptRoot |
        Export-RawTextPagesFromSourceFile -OnlyUpdateExistingPages |
        ForEach-Object {
            $BatchProc.ForEachItem($PSItem)
        }

    $BatchProc.FlushItems()

} finally {
    Pop-Location
}
