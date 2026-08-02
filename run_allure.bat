@echo off

set ALLURE_RESULTS_DIR=reports\allure-results

pytest --alluredir=%ALLURE_RESULTS_DIR% --clean-alluredir

if errorlevel 1 (
    echo.
    echo pytest 执行失败，不启动 Allure 报告。
    exit /b 1
)

allure serve %ALLURE_RESULTS_DIR%