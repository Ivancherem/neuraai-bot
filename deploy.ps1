# Создайте файл deploy.ps1
@'
Write-Host "🚀 Запуск деплоя NeuraAI Bot..." -ForegroundColor Cyan

# 1. Обновляем .env
Write-Host "1. Обновляю .env файл..." -ForegroundColor Yellow
@"
BOT_TOKEN=8462465684:AAHdjhf7s4lUdUJXteqwqAvELuuZ-onmVuq7B
BOT_NAME=NeuraAI Assistant
BOT_VERSION=4.0
"@ | Out-File .env -Encoding UTF8 -Force

# 2. Обновляем .gitignore
Write-Host "2. Обновляю .gitignore..." -ForegroundColor Yellow
if (-not (Test-Path .gitignore)) {
    @"
.env
*.ps1
__pycache__/
*.pyc
"@ | Out-File .gitignore -Encoding UTF8
}

# 3. Настраиваем Git
Write-Host "3. Настраиваю Git..." -ForegroundColor Yellow
git config --local user.email "bot@neuraai.com"
git config --local user.name "NeuraAI Bot"

# 4. Делаем коммит
Write-Host "4. Создаю коммит..." -ForegroundColor Yellow
git add .
git commit -m "Deploy NeuraAI Bot $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

# 5. Отправляем на GitHub
Write-Host "5. Отправляю на GitHub..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/Ivancherem/neuraai-bot.git
git branch -M main
git push -u origin main --force

Write-Host "`n✅ ГОТОВО!" -ForegroundColor Green
Write-Host "📦 Код отправлен на GitHub" -ForegroundColor Green
Write-Host "🌐 Теперь обновите BOT_TOKEN на Render.com" -ForegroundColor Yellow
'@ | Out-File deploy.ps1 -Encoding UTF8