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
base_url = current_config["base_url"]

login_url = base_url + "/auth/login"
current_user_url = base_url + "/api/v1/user"
users_url = base_url + "/api/v1/users"

timeout = 10

username = os.getenv("API_USERNAME", "admin")
password = os.getenv("API_PASSWORD", "admin123")