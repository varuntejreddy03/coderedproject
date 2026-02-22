@echo off
echo ========================================
echo Fixing Git Rebase Issue
echo ========================================
echo.

echo Aborting rebase...
git rebase --abort

echo.
echo Adding files...
git add .

echo.
echo Committing changes...
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
git commit -m "Update: %timestamp%"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Done!
echo ========================================
pause
