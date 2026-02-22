@echo off
echo ========================================
echo Checking Frontend Files
echo ========================================
echo.

echo Files in frontend/src:
dir /s /b frontend\src

echo.
echo ========================================
echo Git Status:
echo ========================================
git status

echo.
echo ========================================
echo Files staged for commit:
echo ========================================
git diff --cached --name-only

echo.
echo ========================================
echo All tracked files:
echo ========================================
git ls-files | findstr "frontend/src"

echo.
pause
