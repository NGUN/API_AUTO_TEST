import pytest
from api.user_api import get_current_user, get_users, create_user, update_user, delete_user, get_user_by_id
from utils.assert_utils import assert_status_code, assert_business_code, assert_data_not_none, assert_user_in_list, assert_user_not_in_list, assert_data_is_none
from utils.data_utils import build_create_user_data
import allure
from data.user_data import (create_user_invalid_field_data, create_user_invalid_field_ids, not_exist_user_id,
							update_not_exist_user_data, update_not_exist_user_ids, delete_not_exist_user_data, delete_not_exist_user_ids,
							get_not_exist_user_by_id_data, get_not_exist_user_by_id_ids, create_user_duplicate_username_data, create_user_duplicate_username_ids,
							update_username_ignored_data, update_username_ignored_ids,)
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
		user_body = get_json(user_response)
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

	users_body = get_json(users_response)
	assert_data_not_none(users_body)

@pytest.fixture
def created_user(headers):
	"""创建用户，并在用例结束后删除用户"""

	with allure.step("前置：创建测试用户"):
		create_user_data = build_create_user_data()
		create_response = create_user(headers, create_user_data)
		assert_status_code(create_response, 200)

		body = get_json(create_response)
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

@allure.feature("用户模块")
@allure.story("创建用户")
@allure.title("创建用户后列表可以查到该用户")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.write
def test_created_user_in_user_list(headers, created_user):
	"""创建用户后，用户列表可以查询到该用户"""

	with allure.step("获取已创建用户数据"):
		created_user_data = created_user["data"]

	with allure.step("发送查询用户列表接口请求"):
		users_response = get_users(headers)

	attach_response(users_response,"查询用户列表接口响应")

	with allure.step("断言查询用户列表成功"):
		assert_status_code(users_response, 200)

		users_body = get_json(users_response)
		user_list = users_body["data"]["list"]

	with allure.step("断言用户列表包含新创建的用户"):
		assert_user_in_list(user_list, created_user_data)



@allure.feature("用户模块")
@allure.story("创建用户")
@allure.title("创建用户缺少必填字段")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "case",
    create_user_invalid_field_data,
    ids=create_user_invalid_field_ids,
)
@pytest.mark.negative
def test_create_user_invalid_field(headers, case):
	"""创建用户字段非法"""
	allure.dynamic.title(case["case_desc"])

	with allure.step("准备创建用户测试数据"):
		create_user_data = build_create_user_data()

	# 根据测试数据修改请求体
	with allure.step(case["case_desc"]):
		if case["action"] == "pop":
			create_user_data.pop(case["field"])
		elif case["action"] == "set":
			create_user_data[case["field"]] = case["value"]
		else:
			raise ValueError(f"不支持的 action：{case["action"]}")

	with allure.step("发送创建用户请求"):
		create_response = create_user(headers, create_user_data)

	attach_response(create_response, "创建用户失败响应")

	with allure.step("断言创建用户失败"):
		assert_status_code(create_response, case["expected_status"])

		#body = create_response.json()
		body = get_json(create_response)
		assert_business_code(body, case["expected_code"])

@allure.feature("用户模块")
@allure.story("创建用户")
@allure.title("创建用户时缺少非必填字段email，也可以创建成功")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.write
def test_create_user_without_email(headers):
	"""创建用户时缺少非必填字段 email，也可以创建成功"""

	user_id = None

	try:
		with allure.step("准备创建用户测试数据"):
			create_user_data = build_create_user_data()

		with allure.step("删除非必填字段 email"):
			create_user_data.pop("email")

		with allure.step("发送创建用户接口请求"):
			response = create_user(headers, create_user_data)

		attach_response(response, "缺少 email 创建用户接口响应")

		with allure.step("断言缺少 email 时创建用户成功"):
			assert_status_code(response, 200)

			body = get_json(response)
			assert_business_code(body, 200)
			assert_data_not_none(body)

			user_id = body["data"]["id"]

	finally:
		if user_id is not None:
			with allure.step("后置：删除测试用户"):
				delete_response = delete_user(headers, user_id)
				attach_response(delete_response, "删除测试用户接口响应")
				assert_status_code(delete_response, 200)

@allure.feature("用户模块")
@allure.story("创建用户")
@allure.title("重复 username 创建用户失败")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
	"case_title, expected_status, expected_code",
	create_user_duplicate_username_data,
	ids=create_user_duplicate_username_ids,
)
@pytest.mark.negative
@pytest.mark.write
def test_create_user_duplicate_username(headers, created_user, case_title, expected_status, expected_code):
	"""重复 username 创建用户失败"""

	allure.dynamic.title(case_title)

	with allure.step("获取已创建用户数据"):
		created_user_data = created_user["data"]

	with allure.step("准备重复 username 的创建用户数据"):
		duplicate_user_data = build_create_user_data()
		duplicate_user_data["username"] = created_user_data["username"]

	with allure.step("发送重复 username 创建用户请求"):
		response = create_user(headers, duplicate_user_data)

	attach_response(response, "重复 username 创建用户响应")

	with allure.step("断言重复 username 创建用户失败"):
		assert_status_code(response, expected_status)

		body =get_json(response)
		assert_business_code(body, expected_code)

@allure.feature("用户模块")
@allure.story("删除用户")
@allure.title("删除存在的用户成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.write
def test_delete_user_success(headers, created_user):
	"""删除存在的用户成功"""
	with allure.step("获取已创建用户数据"):
		create_user_data = created_user["data"]
		user_id = create_user_data["id"]

	with allure.step("发送删除用户接口请求"):
		delete_response = delete_user(headers, user_id)

	attach_response(delete_response, "删除用户接口响应")

	with allure.step("断言删除用户成功"):
		assert_status_code(delete_response, 200)

	with allure.step("查询用户列表"):
		user_response = get_users(headers)

	attach_response(user_response, "删除后查询用户列表响应")

	with allure.step("断言用户列表中不存在已删除用户"):
		assert_status_code(user_response, 200)

		user_body = get_json(user_response)
		user_list = user_body["data"]["list"]

		assert_user_not_in_list(user_list,create_user_data)

@allure.feature("用户模块")
@allure.story("删除用户")
@allure.title("删除不存在的用户失败")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "case",
    delete_not_exist_user_data,
    ids=delete_not_exist_user_ids,
)
@pytest.mark.negative
@pytest.mark.write
def test_delete_not_exist_user(headers, case):
	"""删除不存在的用户失败"""

	allure.dynamic.title(case["case_title"])

	with allure.step("发送删除不存在用户接口请求"):
		delete_response = delete_user(headers, case["user_id"])

	attach_response(delete_response,"删除不存在用户接口响应")

	with allure.step("断言删除不存在用户失败"):
		assert_status_code(delete_response, case["expected_status"])

		body = get_json(delete_response)
		assert_business_code(body, case["expected_code"])
		assert_data_is_none(body)

@allure.feature("用户模块")
@allure.story("查询用户详情")
@allure.title("根据用户 id 查询用户详情成功")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.write
def test_get_user_by_id_success(headers, created_user):
	"""根据用户 id 查询用户详情成功"""
	create_user_data = created_user["data"]
	user_id = create_user_data["id"]

	with allure.step("发送查询用户详情接口请求"):
		response = get_user_by_id(headers, user_id)

	attach_response(response, "查询用户详情接口响应")

	with allure.step("断言查询用户详情成功"):
		assert_status_code(response, 200)

		body = get_json(response)
		assert_business_code(body, 200)
		assert_data_not_none(body)

		user_data = body["data"]
		assert user_data["id"] == create_user_data["id"]
		assert user_data["username"] == create_user_data["username"]
		assert user_data["email"] == create_user_data["email"]

@allure.feature("用户模块")
@allure.story("查询用户详情")
@allure.title("查询不存在的用户详情失败")
@pytest.mark.parametrize(
    "case",
    get_not_exist_user_by_id_data,
    ids=get_not_exist_user_by_id_ids,
)
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_get_not_exist_user_by_id(headers, case):
	"""查询不存在的用户详情失败"""

	allure.dynamic.title(case["case_title"])

	with allure.step("发送查询不存在用户详情接口请求"):
		response = get_user_by_id(headers, case["user_id"])

	attach_response(response, "查询不存在用户详情接口响应")

	with allure.step("断言查询不存在用户详情失败"):
		assert_status_code(response, case["expected_status"])

		body = get_json(response)
		assert_business_code(body, case["expected_code"])
		assert_data_is_none(body)

@allure.feature("用户模块")
@allure.story("更新用户")
@allure.title("更新用户邮箱和密码成功")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.write
def test_update_user_email_and_password_success(headers, created_user):
	"""更新用户邮箱和密码成功"""

	created_user_data = created_user["data"]
	user_id = created_user_data["id"]
	old_username = created_user_data["username"]

	new_email = build_create_user_data()["email"]

	update_user_data = {
		"email": new_email,
		"password": "Bb123456"
	}

	with allure.step("发送更新用户接口请求"):
		update_response = update_user(headers, user_id, update_user_data)

	attach_response(update_response, "更新用户接口响应")

	with allure.step("断言更新用户接口响应"):
		assert_status_code(update_response, 200)

		body = get_json(update_response)
		assert_business_code(body, 200)
		assert_data_not_none(body)

		updated_user = body["data"]
		assert updated_user["id"] == user_id
		assert updated_user["username"] == old_username
		assert updated_user["email"] == new_email

		with allure.step("查询更新后的用户详情"):
			detail_response = get_user_by_id(headers, user_id)

		attach_response(detail_response, "更新后用户详情接口响应")

		with allure.step("断言用户详情中的邮箱已更新，用户名未变化"):
			assert_status_code(detail_response, 200)

			detail_body = get_json(detail_response)
			assert_business_code(detail_body, 200)
			assert_data_not_none(detail_body)

			detail_user = detail_body["data"]
			assert detail_user["id"] == user_id
			assert detail_user["username"] == old_username
			assert detail_user["email"] == new_email

@allure.feature("用户模块")
@allure.story("更新用户")
@allure.title("更新用户名不生效")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "case",
    update_username_ignored_data,
    ids=update_username_ignored_ids,
)
@pytest.mark.write
def test_update_username_failed(headers, created_user, case):
	"""更新用户名不生效"""
	allure.dynamic.title(case["case_title"])

	create_user_data = created_user["data"]
	user_id = create_user_data["id"]
	old_username = create_user_data["username"]

	update_user_data = {
		"username": case["new_username"],
	}

	with allure.step("发送更新用户名请求接口"):
		update_response = update_user(headers, user_id, update_user_data)

	attach_response(update_response, "更新用户名接口响应")

	with allure.step("断言更新用户名请求返回成功"):
		assert_status_code(update_response, case["expected_status"])

		body = get_json(update_response)
		assert_business_code(body, case["expected_code"])

	with allure.step("查询用户详情，确认用户名未变化"):
		detail_response = get_user_by_id(headers, user_id)

	attach_response(detail_response, "更新用户名后用户详情响应")

	with allure.step("断言用户名没有被修改"):
		assert_status_code(detail_response, 200)

		detail_body = get_json(detail_response)
		assert_business_code(detail_body, 200)

		detail_user = detail_body["data"]
		assert detail_user["username"] == old_username

@allure.feature("用户模块")
@allure.story("更新用户")
@allure.title("更新不存在的用户失败")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
	"case",
	update_not_exist_user_data,
	ids=update_not_exist_user_ids,
)
@pytest.mark.negative
@pytest.mark.write
def test_update_not_exist_user_failed(headers, case):
	"""更新不存在的用户失败"""

	allure.dynamic.title(case["case_title"])

	new_email = build_create_user_data()["email"]

	update_user_data = {
		"email": new_email,
		"password": case["password"],
	}

	with allure.step("发送更新不存在用户接口请求"):
		update_response = update_user(headers, case["user_id"], update_user_data)

	attach_response(update_response, "更新不存在用户接口响应")

	with allure.step("断言更新不存在用户失败"):
		assert_status_code(update_response, case["expected_status"])

		body = get_json(update_response)
		assert_business_code(body, case["expected_code"])
		assert_data_is_none(body)

