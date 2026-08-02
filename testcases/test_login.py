import pytest
from api.auth_api import login
from utils.assert_utils import assert_status_code,assert_business_code, assert_data_by_expected, assert_response_basic
from data.login_data import login_cases, login_case_ids
from utils.log_utils import get_logger
import allure

logger = get_logger()

@allure.feature("登录模块")
@allure.story("登录校验")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
	"case",
	login_cases,
	ids = login_case_ids,
)
@pytest.mark.smoke
def test_login_params(case):
	"""登录接口参数化测试"""
	allure.dynamic.title(case["case_title"])

	with allure.step("发送登录接口请求"):
		login_response = login(case["username"],case["password"])

	with allure.step("断言登录接口响应"):
		login_body = assert_response_basic(
			login_response,
			case["expected_status"],
			case["expected_code"],
			case["expected_data"]
		)
