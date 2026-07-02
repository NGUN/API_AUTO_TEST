import os

env = os.getenv("ENV","local")

if env == "local":
	base_url = "http://127.0.0.1:11011"
elif env == "test":
    base_url = "http://test.xxx.com"
elif env == "pre":
    base_url = "http://pre.xxx.com"
else:
    raise ValueError(f"未知环境: {env}")

login_url = base_url + "/auth/login"
current_user_url = base_url + "/api/v1/user"
users_url = base_url + "/api/v1/users"

timeout = 10

username = os.getenv("API_USERNAME", "admin")
password = os.getenv("API_PASSWORD", "admin123")