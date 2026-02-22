@echo off
echo ========================================
echo Adding Frontend Src Folder
echo ========================================
echo.

echo Removing node_modules from git if tracked...
git rm -r --cached frontend/node_modules 2>nul

echo.
echo Force adding frontend/src folder...
git add -f frontend/src/

echo.
echo Adding other files...
git add .

echo.
echo Committing...
git commit -m "Add frontend src folder"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo Done!
echo ========================================
pause
