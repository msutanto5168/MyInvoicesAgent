$ErrorActionPreference = "Stop"
$FunctionName = "send-email"
$Region = "ap-southeast-2"
$ZipFile = "function.zip"

Write-Host "Packaging $FunctionName..."
if (Test-Path $ZipFile) { Remove-Item $ZipFile }
Compress-Archive -Path "sendemail.py" -DestinationPath $ZipFile

Write-Host "Deploying to Lambda..."
aws lambda update-function-code `
    --function-name $FunctionName `
    --zip-file "fileb://$ZipFile" `
    --region $Region

Write-Host "Done. $FunctionName deployed successfully."
