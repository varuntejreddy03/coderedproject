@echo off
echo ========================================
echo PumpWatch - Git Push Script
echo ========================================
echo.

REM Initialize git if not already done
if not exist .git (
    echo Initializing Git repository...
    git init
    git branch -M main
    git remote add origin https://github.com/varuntejreddy03/coderedproject.git
)

REM Add all files
echo Adding files...
git add .

REM Commit with timestamp
echo Committing changes...
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
git commit -m "Update: %timestamp%"

REM Create main branch if needed
git branch -M main

REM Pull first to merge remote changes
echo Pulling from GitHub...
git pull origin main --rebase

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo Push completed!
echo ========================================
pause
