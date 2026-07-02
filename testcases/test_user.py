import pytest
from api.user_api import get_current_user, get_users, create_user
from utils.assert_utils import assert_status_code, assert_business_code, assert_data_not_none
from utils.data_utils import build_create_user_data
from utils.log_utils import get_logger
import allure

logger = get_logger()

@allure.feature("用户模块")
@allure.story("查询当前用户")
@allure.title("获取当前用户信息成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_get_current_user(headers):
	"""获取当前用户信息接口"""
	with allure.step("发送获取当前用户接口请求"):
		user_response = get_current_user(headers)

	assert_status_code(user_response, 200)

	with allure.step("断言获取当前用户接口响应"):
		user_body = user_response.json()
		assert_data_not_none(user_body)

@allure.feature("用户模块")
@allure.story("查询当前用户")
@allure.title("获取当前用户信息失败")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_get_current_user_without_token():
	"""获取当前用户信息接口"""
	with allure.step("发送获取当前用户接口请求"):
		response = get_current_user(headers={})

	with allure.step("断言获取当前用户接口响应"):
		assert_status_code(response, 401)

@allure.feature("用户模块")
@allure.story("查询用户列表")
@allure.title("获取用户列表成功")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.write
def test_get_users(headers):
	"""获取用户列表接口"""
	with allure.step("发送获取用户列表接口请求"):
		users_response = get_users(headers)

	with allure.step("断言获取用户列表接口响应"):
		assert_status_code(users_response, 200)

	users_body = users_response.json()
	assert_data_not_none(users_body)

@allure.feature("用户模块")
@allure.story("创建用户")
@allure.title("创建用户成功")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user(headers):
	"""创建用户接口"""
	with allure.step("准备创建用户测试数据"):
		create_user_data = build_create_user_data()

	with allure.step("发送创建用户请求"):
		create_response = create_user(headers,create_user_data)

	with allure.step("断言创建用户接口响应"):
		assert_status_code(create_response, 200)

	body = create_response.json()
	assert_data_not_none(body)
