@echo off
setlocal
cd /d "%~dp0"
title EC v1.0.1 Windows Compatibility Fix

echo ============================================================
echo EC v1.0.1 - Manufacturing Intelligence Reference System
echo Windows one-click validation
echo ============================================================
echo.

set "PYEXE="

py -3.12 -c "import sys; assert sys.version_info[:2] == (3,12)" >nul 2>&1
if not errorlevel 1 set "PYEXE=py -3.12"

if not defined PYEXE (
  py -3.13 -c "import sys; assert sys.version_info[:2] == (3,13)" >nul 2>&1
  if not errorlevel 1 set "PYEXE=py -3.13"
)

if not defined PYEXE (
  echo [ERROR] Python 3.12 or 3.13 was not found.
  echo Install Python 3.12 x64, then run this file again.
  echo Python 3.14 is not part of the v1.0.1 certified Windows profile.
  pause
  exit /b 1
)

echo [0/5] Using:
%PYEXE% --version

if not exist ".venv\Scripts\python.exe" (
  echo.
  echo [1/5] Creating local virtual environment .venv ...
  %PYEXE% -m venv .venv
  if errorlevel 1 goto :fail
) else (
  echo.
  echo [1/5] Existing .venv found.
)

set "VENV_PY=.venv\Scripts\python.exe"

echo.
echo [2/5] Installing EC v1.0.1 locally ...
"%VENV_PY%" -m pip install -e .
if errorlevel 1 goto :fail

echo.
echo [3/5] EC doctor ...
"%VENV_PY%" -m ec doctor
if errorlevel 1 goto :fail

echo.
echo [4/5] Running full reference test suite ...
"%VENV_PY%" -m unittest discover -s tests -v
if errorlevel 1 goto :fail

echo.
echo [5/5] Running Manufacturing Intelligence demo ...
"%VENV_PY%" -m ec demo-manufacturing
if errorlevel 1 goto :fail

echo.
echo ============================================================
echo EC v1.0.1 WINDOWS VALIDATION: PASS
echo ============================================================
echo .venv is local-only and is ignored by Git.
echo.
pause
exit /b 0

:fail
echo.
echo ============================================================
echo EC v1.0.1 WINDOWS VALIDATION: FAILED
echo ============================================================
echo Please copy the full console output and send it back.
echo.
pause
exit /b 1
