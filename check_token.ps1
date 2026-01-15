# Сохраните как check_token.ps1 и запустите: .\check_token.ps1

Write-Host "🔍 Проверка безопасности токена..." -ForegroundColor Yellow
Write-Host "=" * 50

# Проверка .env файла
if (Test-Path .env) {
    $envContent = Get-Content .env
    if ($envContent -match "8462465684") {
        Write-Host "❌ ОШИБКА: Старый токен найден в .env!" -ForegroundColor Red
        Write-Host "Замените токен в .env на новый!" -ForegroundColor Red
    } else {
        Write-Host "✅ .env файл в порядке" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  Файл .env не найден" -ForegroundColor Yellow
}

# Проверка Python файлов
$pyFiles = Get-ChildItem -Filter "*.py" -Recurse
foreach ($file in $pyFiles) {
    $content = Get-Content $file.FullName
    if ($content -match "8462465684" -or $content -match "AAGAj7s4lUdUJXteqwqAvELuuZ") {
        Write-Host "❌ ОШИБКА: Токен найден в $($file.Name)!" -ForegroundColor Red
    }
}

Write-Host "=" * 50
Write-Host "✅ Проверка завершена" -ForegroundColor Green

# Проверка Git истории
Write-Host "`n🔍 Проверка Git истории..." -ForegroundColor Yellow
git log --all --oneline | Select-String "8462465684"