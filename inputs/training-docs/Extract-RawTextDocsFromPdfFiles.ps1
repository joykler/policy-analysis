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

    Add-LoggingMethod 'Info_StartedExportingRawTexts' -Method {

        $S = $PSStyle.Foreground.BrightWhite + $PSStyle.Bold + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Started Exporting raw text from all pdf files...' + $R)
    }

    Add-LoggingMethod 'Info_ExportingRawTextFromFile' -Method {

        param($file)

        $S = $PSStyle.Foreground.Green + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Exporting raw-text from file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R)
    }

    Add-LoggingMethod 'Warn_TargetFolderAllreadyExists' -Method {

        param($file)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Target-folder allready exists: $F[ $($file.LoggedDir) ]" + $R)
    }

    Add-LoggingMethod 'Warn_ExportRawTextFailed' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightYellow + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed exporting raw-text from file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R + "`n$err")
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

#region -- Declare: Export-RawTextFromSourceFile --
function Export-RawTextFromSourceFile {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $SourceFile,

        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [PSCustomObject] $TargetFile
    )

    begin {
        function Export-RawText([iTextSharp.text.pdf.PdfReader] $Source_PdfReader) {

            $PageMax = $Source_PdfReader.NumberOfPages
            for ($PageNr = 1; $PageNr -le $PageMax; $PageNr++) {

                $TargetPageFile = Get-FileInfo $($TargetFile.Path -f $PageNr) -LoggedDir $TargetFile.LoggedDir

                $TargetPageText = [iTextSharp.text.pdf.parser.PdfTextExtractor]::GetTextFromPage($Source_PdfReader, $PageNr)

                Set-Content -Path $TargetPageFile.Path -Value $TargetPageText

                Write-Output $TargetPageFile
            }
        }
    }

    process {
        if ($(Test-Path $TargetFile.Folder -PathType Container)) {
            $Logging.Warn_TargetFolderAllreadyExists($TargetFile)

        } else {
            $Logging.Info_ExportingRawTextFromFile($SourceFile)

            try {
                mkdir $TargetFile.Folder -Force | Out-Null

                $Source_PdfReader = [iTextSharp.text.pdf.PdfReader]::new($SourceFile.Path)

                Export-RawText $Source_PdfReader -TargetPath $TargetFile.Path

            } catch {
                $Logging.Warn_ExportRawTextFailed($TargetFile, $_)

                if ($(Test-Path $TargetFile.Path -PathType Leaf)) {
                    Remove-Item $TargetFile.Path -Force
                }
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



    Add-Type -Path "$PSScriptRoot\.lib\BouncyCastle.Cryptography\lib\net6.0\BouncyCastle.Cryptography.dll"
    Add-Type -Path "$PSScriptRoot\.lib\iTextSharp\itextsharp.dll"



    $Logging.Info_StartedExportingRawTexts()
    Get-ChildItem -Path $PSScriptRoot -Filter *.pdf -File -Recurse |
        Get-TargetInfoFromSourceFile -SourceRootPath $PSScriptRoot |
        Export-RawTextFromSourceFile |
        ForEach-Object {
            $BatchProc.ForEachItem($PSItem)
        }

    $BatchProc.FlushItems()

} finally {
    Pop-Location
}
