@echo off
REM Windows Code Signing Script for OpenLiveCaption
REM Signs executables and installers with a code signing certificate

setlocal enabledelayedexpansion

echo ======================================
echo OpenLiveCaption Windows Code Signing
echo ======================================
echo.

REM Configuration
REM Update these paths based on your system
set "SIGNTOOL_PATH=C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"
set "TIMESTAMP_URL=http://timestamp.digicert.com"

REM Certificate configuration from environment variables
REM Set these environment variables:
REM   CODESIGN_CERT_PATH - Path to your .pfx certificate file
REM   CODESIGN_CERT_PASSWORD - Password for the certificate
set "CERT_PATH=%CODESIGN_CERT_PATH%"
set "CERT_PASSWORD=%CODESIGN_CERT_PASSWORD%"

REM Check if file to sign was provided
if "%~1"=="" (
    echo Error: No file specified to sign
    echo.
    echo Usage: sign_windows.bat ^<file-to-sign^>
    echo Example: sign_windows.bat dist\OpenLiveCaption.exe
    echo.
    exit /b 1
)

set "FILE_TO_SIGN=%~1"

REM Check if file exists
if not exist "%FILE_TO_SIGN%" (
    echo Error: File not found: %FILE_TO_SIGN%
    exit /b 1
)

echo File to sign: %FILE_TO_SIGN%
echo.

REM Check if signtool exists
if not exist "%SIGNTOOL_PATH%" (
    echo Error: signtool.exe not found at: %SIGNTOOL_PATH%
    echo.
    echo Please install Windows SDK or update SIGNTOOL_PATH in this script
    echo Download from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
    echo.
    echo Alternative locations to check:
    echo   C:\Program Files (x86)\Windows Kits\10\bin\^<version^>\x64\signtool.exe
    echo   C:\Program Files (x86)\Windows Kits\10\bin\^<version^>\x86\signtool.exe
    echo.
    exit /b 1
)

echo Found signtool: %SIGNTOOL_PATH%

REM Check if certificate path is set
if "%CERT_PATH%"=="" (
    echo Error: Certificate path not set
    echo.
    echo Please set the CODESIGN_CERT_PATH environment variable:
    echo   setx CODESIGN_CERT_PATH "C:\path\to\your\certificate.pfx"
    echo.
    echo Or edit this script to set CERT_PATH directly
    echo.
    exit /b 1
)

REM Check if certificate exists
if not exist "%CERT_PATH%" (
    echo Error: Certificate file not found: %CERT_PATH%
    echo.
    echo Please verify the CODESIGN_CERT_PATH environment variable
    echo.
    exit /b 1
)

echo Found certificate: %CERT_PATH%

REM Check if password is set
if "%CERT_PASSWORD%"=="" (
    echo Error: Certificate password not set
    echo.
    echo Please set the CODESIGN_CERT_PASSWORD environment variable:
    echo   setx CODESIGN_CERT_PASSWORD "your-password"
    echo.
    echo Or edit this script to set CERT_PASSWORD directly
    echo.
    exit /b 1
)

echo Certificate password: [HIDDEN]
echo Timestamp server: %TIMESTAMP_URL%
echo.

REM Sign the file
echo Signing file...
"%SIGNTOOL_PATH%" sign ^
    /f "%CERT_PATH%" ^
    /p "%CERT_PASSWORD%" ^
    /fd SHA256 ^
    /tr "%TIMESTAMP_URL%" ^
    /td SHA256 ^
    /v ^
    "%FILE_TO_SIGN%"

if errorlevel 1 (
    echo.
    echo Error: Signing failed
    echo.
    echo Common issues:
    echo   - Incorrect certificate password
    echo   - Certificate expired
    echo   - Timestamp server unreachable
    echo   - File already signed
    echo.
    echo To verify certificate:
    echo   certutil -dump "%CERT_PATH%"
    echo.
    exit /b 1
)

echo.
echo ======================================
echo Signing completed successfully!
echo ======================================
echo.

REM Verify the signature
echo Verifying signature...
"%SIGNTOOL_PATH%" verify /pa /v "%FILE_TO_SIGN%"

if errorlevel 1 (
    echo.
    echo Warning: Signature verification failed
    echo The file was signed but verification encountered an issue
    echo.
    exit /b 1
)

echo.
echo ======================================
echo Verification successful!
echo ======================================
echo.
echo Signed file: %FILE_TO_SIGN%
echo.
echo To view signature in Windows:
echo   1. Right-click the file
echo   2. Select Properties
echo   3. Go to Digital Signatures tab
echo.

exit /b 0
