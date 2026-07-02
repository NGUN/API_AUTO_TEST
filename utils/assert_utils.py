def assert_status_code(response, expected_status):
    """断言 HTTP 状态码"""
    assert response.status_code == expected_status

def assert_business_code(body, expected_code):
    """断言业务 code"""
    assert body["code"] == expected_code

def assert_data_not_none(body):
    """断言数据不为空"""
    assert body["data"] is not None

def assert_data_is_none(body):
    """断言数据为空"""
    assert body["data"] is None