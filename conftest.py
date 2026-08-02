import pytest
from api.auth_api import login
from config import username, password, env, base_url
from utils.assert_utils import assert_status_code,assert_data_not_none
from utils.allure_utils import write_environment_info, write_executor_info

#抽取token
def get_token():
	#登录并返回token
	login_response = login(username, password)

	assert_status_code(login_response,200)

	login_body = login_response.json()

	assert_data_not_none(login_body)
	return login_body["data"]["token"]

@pytest.fixture(scope="session")
def token():
	"""pytest fixture:给测试用例提供token,且只登录一次"""
	return get_token()

@pytest.fixture(scope="session")
def headers(token):
	"""统一生成带 Token 的请求头"""
	headers = {"Authorization": f"Bearer {token}"}
	return headers

@pytest.fixture(scope="session", autouse=True)
def write_allure_environment():
    """写入 Allure 环境信息"""
    write_environment_info(env, base_url)
    write_executor_info()