using namespace Microsoft.PowerShell.Commands
using namespace System.Net


$InformationPreference = 'Continue'
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'Ignore'

$PSDefaultParameterValues = @{
    'Write-Verbose:Verbose'                = $true

    'Add-Member:MemberType'                = 'ScriptMethod'
    'Add-Member:PassThru'                  = $true

    'Export-Excel:AutoSize'                = $true
    'Export-Excel:AutoFilter'              = $true
    'Export-Excel:BoldTopRow'              = $true
    'Export-Excel:FreezeTopRowFirstColumn' = $true
    'Export-Excel:TableStyle'              = 'Medium6'
}

$PSStyle.OutputRendering = 'Ansi'

$TargetReportFile = "$PSScriptRoot\MetaDataReport.xlsx"



#region -- Declare: $Logging --
$global:Logging = [PSCustomObject]::new()
& {
    function Add-LoggingMethod([string] $Name, [scriptblock] $Method) {

        $global:Logging = $global:Logging | Add-Member -Name $Name -Value $Method
    }



    Add-LoggingMethod 'LibInit_PdfImporting_Started' -Method {

        $S = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Started initializing library: Pdf importing' + $R)
    }

    Add-LoggingMethod 'LibInit_PdfImporting_Finished' -Method {

        $S = $PSStyle.Foreground.Green + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Finished initializing library: Pdf importing' + $R)
    }



    Add-LoggingMethod 'LibInit_ExcelExporting_Started' -Method {

        $S = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Started initializing library: Excel exporting' + $R)
    }

    Add-LoggingMethod 'LibInit_ExcelExporting_Finished' -Method {

        $S = $PSStyle.Foreground.Green + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Finished initializing library: Excel exporting' + $R)
    }



    Add-LoggingMethod 'Process_Started' -Method {

        $S = $PSStyle.Foreground.BrightWhite + $PSStyle.Bold + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + 'Started exporting meta-data report from all pdf-files...' + $R)
    }

    Add-LoggingMethod 'EachPdf_Exporting_Started' -Method {

        param($file)

        $S = $PSStyle.Foreground.White
        $F = $PSStyle.Foreground.White + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Information $($S + " * Exporting meta-data from pdf-file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R)
    }

    Add-LoggingMethod 'EachPdf_Exporting_Failed' -Method {

        param($file, $err)

        $S = $PSStyle.Foreground.BrightRed + $PSStyle.Bold
        $F = $PSStyle.Foreground.White + $PSStyle.BoldOff + $PSStyle.Italic
        $R = $PSStyle.Reset

        Write-Warning $($S + " ! Failed exporting meta-data from pdf-file: $F[ $($file.LoggedDir) ]> $($file.Name)" + $R + "`n$err")
    }

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

#region -- Declare: Initialize-ExcelExporting --
function Initialize-ExcelExporting() {

    $Logging.LibInit_ExcelExporting_Started()

    # Install & import module
    if (-not $(Get-InstalledModule 'ImportExcel' -ErrorAction Ignore)) {
        Install-Module 'ImportExcel' -Scope CurrentUser
    }

    Import-Module 'ImportExcel'

    # Close (any Excel) process
    while (@(Get-Process -Name 'Excel' -ErrorAction Ignore | Stop-Process -PassThru)) {
    }

    # Remove target report-file
    if ($(Test-Path $TargetReportFile -PathType Leaf)) {
        Remove-Item $TargetReportFile -Force
    }

    $Logging.LibInit_ExcelExporting_Finished()
}
#endregion



#region -- Declare: Export-MetaDataFromSourceFile --
function Export-MetaDataFromSourceFile {

    [CmdletBinding()]
    param(
        [Alias('FullName')]
        [Parameter(Mandatory, ValueFromPipelineByPropertyName)]
        [string] $SourcePath
    )

    process {
        $Logging.EachPdf_Exporting_Started($SourceFile)

        try {
            $Source_PdfReader = [iTextSharp.text.pdf.PdfReader]::new($SourceFile.Path)

            Export-MetaDataReport $Source_PdfReader

        } catch {
            $Logging.EachPdf_Exporting_Failed($SourceFile, $_)
        }
    }
}
#endregion



try {
    Push-Location "$PSScriptRoot\..\.." # Set to repo root



    Initialize-PdfImportinging

    Initialize-ExcelExportinging



    $Logging.Process_Started()

    Get-ChildItem -Path "$PSScriptRoot" -Filter '*.pdf' -File -Recurse |
        Export-MetaDataFromSourceFile -OnlyUpdateExistingPages |
        Export-Excel -Path $TargetReportFile

} finally {
    Pop-Location
}
