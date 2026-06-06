@echo off
setlocal

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  py -3 %*
  exit /b %ERRORLEVEL%
)

python %*
exit /b %ERRORLEVEL%
