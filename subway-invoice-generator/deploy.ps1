$ErrorActionPreference = "Stop"
$FunctionName = "create-invoice-subway"
$Region = "ap-southeast-2"
$BuildDir = "build"
$ZipFile = "function.zip"

Write-Host "Cleaning up previous build..."
if (Test-Path $BuildDir) { Remove-Item -Recurse -Force $BuildDir }
if (Test-Path $ZipFile) { Remove-Item $ZipFile }

Write-Host "Packaging $FunctionName..."
New-Item -ItemType Directory -Path $BuildDir | Out-Null
Copy-Item "subway.py" "$BuildDir\lambda_function.py"
Compress-Archive -Path "$BuildDir\*" -DestinationPath $ZipFile

Write-Host "Deploying to Lambda..."
aws lambda update-function-code `
    --function-name $FunctionName `
    --zip-file "fileb://$ZipFile" `
    --region $Region `
    --no-cli-pager

Write-Host "Cleaning up build folder..."
Remove-Item -Recurse -Force $BuildDir

Write-Host "Done. $FunctionName deployed successfully."
