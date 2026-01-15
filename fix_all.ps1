# Сохраните как fix_all.ps1 и запустите: .\fix_all.ps1

Write-Host "🛠️  Исправление всех проблем..." -ForegroundColor Cyan

# 1. Исправляем .env
Write-Host "1. Обновляю .env файл..." -ForegroundColor Yellow
@"
BOT_TOKEN=8462465684:AAHdjhf7s4lUdUJXteqwqAvELuuZ-onmVuq7B
BOT_NAME=NeuraAI Assistant
BOT_VERSION=4.0
"@ | Out-File .env -Encoding UTF8 -Force

# 2. Проверяем super_bot.py
Write-Host "2. Проверяю super_bot.py..." -ForegroundColor Yellow
$botContent = Get-Content super_bot.py -Raw
if ($botContent -match "8462465684:AAGAj7s4lUdUJXteqwqAvELuuZ") {
    Write-Host "❌ Найден старый токен в коде!" -ForegroundColor Red
    # Заменяем если токен прямо в коде
    $botContent = $botContent -replace "8462465684:AAGAj7s4lUdUJXteqwqAvELuuZ-onmVuq7A", ""
    $botContent | Out-File super_bot.py -Encoding UTF8
    Write-Host "✅ Токен удален из кода" -ForegroundColor Green
}

# 3. Настраиваем Git
Write-Host "3. Настраиваю Git..." -ForegroundColor Yellow
git init
git add .
git commit -m "FIX: Security update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# 4. Проверяем ветку
Write-Host "4. Проверяю ветку..." -ForegroundColor Yellow
$branch = git branch --show-current
if (-not $branch) {
    git checkout -b main
    $branch = "main"
}
Write-Host "✅ Текущая ветка: $branch" -ForegroundColor Green

# 5. Отправляем на GitHub
Write-Host "5. Отправляю на GitHub..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/Ivancherem/neuraai-bot.git
git push -u origin $branch --force

Write-Host "`n🎉 ВСЕ ИСПРАВЛЕНО!" -ForegroundColor Green
Write-Host "Токен обновлен: 8462465684:AAHdjhf7s4lUdUJXteqwqAvELuuZ-onmVuq7B" -ForegroundColor Cyan
Write-Host "Обновите токен на Render.com!" -ForegroundColor Yellow