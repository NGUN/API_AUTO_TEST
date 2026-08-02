@echo off

set HTML_REPORT=reports\report.html

pytest --html=%HTML_REPORT% --self-contained-html

if errorlevel 1 (
    echo.
    echo pytest failed. Please check terminal log and HTML report.
    exit /b 1
)

echo.
echo HTML report generated: %HTML_REPORT%