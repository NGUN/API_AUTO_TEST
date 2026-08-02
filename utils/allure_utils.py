import allure
import json
import os
from config import (allure_results_dir,executor_name,executor_type,build_name,report_name,)

def attach_response(response, name="接口响应"):
    """把接口响应内容附加到 Allure 报告"""

    allure.attach(
        response.text,
        name=name,
        attachment_type=allure.attachment_type.JSON
    )

def write_environment_info(env, base_url):
    """写入 Allure 环境信息"""
    os.makedirs(allure_results_dir, exist_ok=True)

    with open(f"{allure_results_dir}/environment.properties", "w", encoding="utf-8") as f:
        f.write(f"ENV={env}\n")
        f.write(f"base_url={base_url}\n")


def write_executor_info():
    """写入 Allure 执行信息"""
    os.makedirs(allure_results_dir, exist_ok=True)

    executor_info = {
        "name": executor_name,
        "type": executor_type,
        "buildName": build_name,
        "reportName": report_name,
    }

    with open(f"{allure_results_dir}/executor.json", "w", encoding="utf-8") as f:
        json.dump(executor_info, f, ensure_ascii=False, indent=2)