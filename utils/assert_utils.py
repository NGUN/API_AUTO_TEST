from doctest import NORMALIZE_WHITESPACE


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

def assert_user_in_list(user_list, expected_user):
    """断言用户列表中存在指定用户"""

    user_id = expected_user["id"]

    found_user = None

    for user in user_list:
        if user["id"] == user_id:
            found_user = user
            break

    assert found_user is not None, f"用户列表中没有找到 id 为 {user_id} 的用户"
    assert found_user["username"] == expected_user["username"], (
        f"用户名不一致，期望：{expected_user['username']}，实际：{found_user['username']}"
    )


    assert found_user["email"] == expected_user["email"], (
        f"邮箱不一样，期望：{expected_user['email']}，实际：{found_user['email']}"
    )

def assert_user_not_in_list(user_list, expected_user):
    """断言用户列表中不存在指定用户"""

    user_id = expected_user["id"]

    for user in user_list:
        assert user["id"] != user_id, f"用户列表中仍存在 id 为 {user_id} 的用户"
