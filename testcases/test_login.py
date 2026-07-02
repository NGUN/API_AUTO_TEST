import pytest
from api.auth_api import login
from utils.assert_utils import assert_status_code,assert_business_code,assert_data_not_none, assert_data_is_none
from data.login_data import login_cases
from utils.log_utils import get_logger
import allure

logger = get_logger()

@allure.feature("登录模块")
@allure.story("登录校验")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
	"case_title,username,password,expected_status,expected_code",
	login_cases
)

@pytest.mark.smoke
def test_login_params(case_title,username,password,expected_status,expected_code):
	"""登录接口参数化测试"""
	allure.dynamic.title(case_title)

	with allure.step("发送登录接口请求"):
		login_response = login(username,password)

	with allure.step("断言登录接口响应"):
		assert_status_code(login_response,expected_status)

		login_body = login_response.json()
		assert_business_code(login_body,expected_code)

		if expected_status == 200:
			assert_data_not_none(login_body)
		else:
			assert_data_is_none(login_body)
