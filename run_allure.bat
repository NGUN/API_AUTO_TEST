@echo off

if exist reports\allure-results (
    rmdir /s /q reports\allure-results
)

pytest --alluredir=reports/allure-results

allure serve reports/allure-results