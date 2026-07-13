from idlelib.pyshell import idle_showwarning

import pytest
from api.user_api import get_current_user, get_users, create_user, update_user, delete_user, get_user_by_id
from utils.assert_utils import assert_status_code, assert_business_code, assert_data_not_none, assert_user_in_list, assert_user_not_in_list, assert_data_is_none
from utils.data_utils import build_create_user_data
import allure
from data.user_data import (create_user_missing_required_field_data, create_user_missing_required_field_ids,)
from utils.allure_utils import attach_response
from utils.request_utils import get_json


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

	attach_response(user_response, "获取当前用户接口响应")

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

	attach_response(response,"获取当前用户接口响应")

	with allure.step("断言获取当前用户接口响应"):
		assert_status_code(response, 401)

@allure.feature("用户模块")
@allure.story("查询用户列表")
@allure.title("获取用户列表成功")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
def test_get_users(headers):
	"""获取用户列表接口"""
	with allure.step("发送获取用户列表接口请求"):
		users_response = get_users(headers)

	attach_response(users_response,"获取用户列表接口响应")

	with allure.step("断言获取用户列表接口响应"):
		assert_status_code(users_response, 200)

	users_body = users_response.json()
	assert_data_not_none(users_body)

@pytest.fixture
def created_user(headers):
	"""创建用户，并在用例结束后删除用户"""

	with allure.step("前置：创建测试用户"):
		create_user_data = build_create_user_data()
		create_response = create_user(headers, create_user_data)
		assert_status_code(create_response, 200)

		body = create_response.json()
		user_id = body["data"]["id"]

	#把创建结果交给测试用例使用
	yield body

	with allure.step("后置：用例执行完后，自动删除测试用户"):
		delete_response = delete_user(headers,user_id)

		#assert_status_code(delete_response, 200)
		assert delete_response.status_code in [200, 404]

@allure.feature("用户模块")
@allure.story("创建用户")
@allure.title("创建用户成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.write
def test_create_user(created_user):
	"""创建用户接口"""
	with allure.step("断言创建用户成功"):
		assert created_user["data"] is not None

@pytest.mark.write
def test_created_user_in_user_list(headers, created_user):
	"""创建用户后，用户列表可以查询到该用户"""

	# 1.从created_user 这个fixture 返回的数据里取出 data
	created_user_data = created_user["data"]

	# 2.调用查询用户列表接口
	users_response = get_users(headers)

	# 3.断言状态吗
	assert_status_code(users_response, 200)

	# 4.取出响应 body
	users_body = users_response.json()

	# 5.取出用户列表
	user_list = users_body["data"]["list"]

	assert_user_in_list(user_list, created_user_data)


@pytest.mark.parametrize(
	"case_title, missing_field, expected_status, expected_code",
	create_user_missing_required_field_data,
	ids = create_user_missing_required_field_ids,
)

@pytest.mark.negative
def test_create_user_missing_required_field(headers, case_title, missing_field, expected_status, expected_code):
	"""创建用户缺少必填字段"""
	allure.dynamic.title(case_title)

	with allure.step("准备创建用户测试数据"):
		create_user_data = build_create_user_data()

	# 删除字段，模拟缺少必填字段
	with allure.step(f"删除字段：{missing_field}"):
		create_user_data.pop(missing_field)

	with allure.step("发送创建用户请求"):
		create_response = create_user(headers, create_user_data)

	attach_response(create_response, "创建用户失败响应")

	with allure.step("断言创建用户失败"):
		assert_status_code(create_response, expected_status)

		#body = create_response.json()
		body = get_json(create_response)
		assert_business_code(body, expected_code)

@pytest.mark.write
def test_create_user_without_email(headers):
	"""创建用户时缺少非必填字段 email，也可以创建成功"""

	try:
		create_user_data = build_create_user_data()

		# 删除 email 字段，模拟缺少非必填字段
		create_user_data.pop("email")

		response = create_user(headers, create_user_data)

		assert_status_code(response, 200)

		body = response.json()
		assert_business_code(body, 200)
		assert_data_not_none(body)

		user_id = body["data"]["id"]

	finally:
		if user_id is not None:
			delete_response = delete_user(headers, user_id)
			assert_status_code(delete_response, 200)

@pytest.mark.negative
@pytest.mark.write
def test_create_user_without_duplicate_username(headers, created_user):
	"""重复 username 创建用户失败"""
	created_user_data = created_user["data"]

	duplicate_user_data = build_create_user_data()
	duplicate_user_data["username"] = created_user_data["username"]

	response = create_user(headers, duplicate_user_data)
	assert_status_code(response, 400)

	body =response.json()
	assert_business_code(body, 400)

@allure.feature("用户模块")
@allure.story("删除用户")
@allure.title("删除存在的用户成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.write
def test_delete_user_success(headers, created_user):
	"""删除存在的用户成功"""
	#1.创建用户，取出响应中的用户id
	create_user_data = created_user["data"]
	user_id = create_user_data["id"]

	#2.删除步骤1中创建的用户
	delete_response = delete_user(headers, user_id)

	#3.断言删除是否成功
	assert_status_code(delete_response, 200)

	#4.获取用户列表
	user_response = get_users(headers)
	assert_status_code(user_response,200)

	user_body = user_response.json()
	user_list = user_body["data"]["list"]

	#5.判断步骤1的用户是否在用户列表中
	assert_user_not_in_list(user_list,create_user_data)

@allure.feature("用户模块")
@allure.story("删除用户")
@allure.title("删除不存在的用户失败")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
@pytest.mark.write
def test_delete_not_exist_user(headers):
	"""删除不存在的用户失败"""

	not_exist_user_id = "not-exist-user-id"

	with allure.step("发送删除不存在用户接口请求"):
		delete_response = delete_user(headers, not_exist_user_id)

	attach_response(delete_response,"删除不存在用户接口响应")

	with allure.step("断言删除不存在用户失败"):
		assert_status_code(delete_response, 404)

		body = get_json(delete_response)
		assert_business_code(body, 404)
		assert_data_is_none(body)



