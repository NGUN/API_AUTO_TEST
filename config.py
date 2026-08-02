import os

env = os.getenv("ENV","local")

env_config = {
    "local":{"base_url":"http://127.0.0.1:11011"
    },
    "test":{
        "base_url":"http://test.xxx.com"
    },
    "pre":{
        "base_url":"http://pre.xxx.com"
    },
}

if env not in env_config:
    raise ValueError(f"未知环境: {env}")

current_config = env_config[env]
base_url = os.getenv("API_BASE_URL", current_config["base_url"])

login_url = base_url + "/auth/login"
current_user_url = base_url + "/api/v1/user"
users_url = base_url + "/api/v1/users"

timeout = 10

username = os.getenv("API_USERNAME", "admin")
password = os.getenv("API_PASSWORD", "admin123")

allure_results_dir = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")

executor_name = os.getenv("EXECUTOR_NAME", "local pytest")
executor_type = os.getenv("EXECUTOR_TYPE", "local")
build_name = os.getenv("BUILD_NAME", "API_AUTO_TEST")
report_name = os.getenv("REPORT_NAME", "API 自动化测试报告")

# MySQL 数据库配置
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_port = int(os.getenv("DB_PORT", "3306"))
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "123456")
db_name = os.getenv("DB_NAME", "demo_project")