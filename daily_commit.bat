@echo off
REM Daily commit helper for CodeGuru (Windows)

echo.
echo 🚀 CodeGuru Daily Commit
echo.

REM Check if there are changes
git status --short > nul 2>&1
if errorlevel 1 (
    echo No changes to commit!
    pause
    exit /b
)

REM Show status
echo 📊 Changes:
git status -s
echo.

REM Ask for commit message
set /p message="What did you work on today? (Commit message): "

REM If no message, use default
if "%message%"=="" set message=Daily update: %date%

REM Add all changes
git add .

REM Commit
git commit -m "🔄 %message%"

REM Push
echo.
echo 📤 Pushing to GitHub...
git push

echo.
echo ✅ Daily commit complete!
echo Keep building! 💪
echo.
pause
