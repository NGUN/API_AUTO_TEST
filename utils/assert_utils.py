from utils.request_utils import get_json
from utils.db_utils import query_one, query_all

def assert_status_code(response, expected_status):
    """断言 HTTP 状态码"""
    assert response.status_code == expected_status, (
        f"HTTP 状态码不一致，期望：{expected_status}，"
        f"实际：{response.status_code}，响应内容：{response.text}"
    )

def assert_business_code(body, expected_code):
    """断言业务 code"""
    assert body["code"] == expected_code, (
        f"业务 code 不一致，期望：{expected_code}，"
        f"实际：{body["code"]}，响应体：{body}"
    )

def assert_data_not_none(body):
    """断言数据不为空"""
    assert body["data"] is not None, f"data 期望不为空，实际响应体：{body}"

def assert_data_is_none(body):
    """断言数据为空"""
    assert body["data"] is None, f"data 期望为空，实际响应体：{body}"

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

def assert_response_basic(response, expected_status, expected_code, expected_data):
    assert_status_code(response, expected_status)
    body = get_json(response)
    assert_business_code(body, expected_code)
    assert_data_by_expected(body, expected_data)
    return body

def assert_data_by_expected(body, expected_data):
    """根据 expected_data 断言 data 字段"""

    if expected_data == "not_none":
        assert_data_not_none(body)
    elif expected_data == "none":
        assert_data_is_none(body)
    else:
        raise ValueError(f"不支持的 expected_data: {expected_data}")

def assert_user_in_db(expected_user):
    """断言用户已存在于数据库，并且关键字段一致"""
    db_user = query_one(
        "select id, username, email from users where id = %s",
        (expected_user["id"],)
    )

    assert db_user is not None, f"数据库中没有找到 id 为 {expected_user['id']} 的用户"
    assert db_user["id"] == expected_user["id"]
    assert db_user["username"] == expected_user["username"]
    assert db_user["email"] == expected_user["email"]


def assert_user_not_in_db(user_id):
    """断言用户不存在于数据库"""
    db_user = query_one(
        "select id from users where id = %s",
        (user_id,)
    )

    assert db_user is None, f"数据库中仍然存在 id 为 {user_id} 的用户"

def assert_user_count_by_username(username, expected_count):
    """断言数据库中指定 username 的用户数量"""
    users = query_all(
        "select id, username, email from users where username = %s",
        (username,)
    )

    actual_count = len(users)

    assert actual_count == expected_count, (
        f"数据库中 username 为 {username} 的用户数量不正确，"
        f"期望：{expected_count}，实际：{actual_count}，查询结果：{users}"
    )