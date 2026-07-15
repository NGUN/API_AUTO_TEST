#公共测试数据
not_exist_user_id = "not-exist-user-id"

# 创建用户相关数据
create_user_invalid_field_data = [
    {
        "case_title":"创建用户失败-缺少用户名",
        "action":"pop",
        "field":"username",
        "value":None,
        "case_desc":"删除 username 字段",
        "expected_status":400,
        "expected_code":400,
    },
    {
        "case_title": "创建用户失败-缺少密码",
        "action": "pop",
        "field": "password",
        "value": None,
        "case_desc": "删除 password 字段",
        "expected_status": 400,
        "expected_code": 400,
    },    {
        "case_title":"创建用户失败-用户名为空",
        "action":"set",
        "field":"username",
        "value":"",
        "case_desc":"将 username 设置为空字符串",
        "expected_status":400,
        "expected_code":400,
    },    {
        "case_title":"创建用户失败-密码为空",
        "action":"set",
        "field":"password",
        "value":"",
        "case_desc":"将 password 设置为空字符串",
        "expected_status":400,
        "expected_code":400,
    },
]

create_user_invalid_field_ids = [
    "missing_username",
    "missing_password",
    "empty_username",
    "empty_password",
]

create_user_duplicate_username_data = [
    ("重复 username 创建用户失败", 400, 400)
]

create_user_duplicate_username_ids = [
    "duplicate_username",
]

# 查询用户相关数据
get_not_exist_user_by_id_data =[
    {
        "case_title":"查询不存在的用户详情失败",
        "user_id":not_exist_user_id,
        "expected_status":404,
        "expected_code":404,
    }
]


get_not_exist_user_by_id_ids = [
    "get_not_exist_user_by_id",
]

# 更新用户相关数据
update_username_ignored_data = [
    {
        "case_title":"更新用户名不生效",
        "new_username":"new_username_not_allowed",
        "expected_status":200,
        "expected_code":200,
    }
]

update_username_ignored_ids = [
    "update_username_ignored",
]

update_not_exist_user_data = [
    {
        "case_title":"更新不存在的用户失败",
        "user_id":not_exist_user_id,
        "password":"Bb123456",
        "expected_status":404,
        "expected_code":404,
    }
]

update_not_exist_user_ids = [
    "update_not_exist_user",
]

# 删除用户相关数据
delete_not_exist_user_data = [
    {
        "case_title":"删除不存在的用户失败",
        "user_id":not_exist_user_id,
        "expected_status":404,
        "expected_code":404,
    }
]

delete_not_exist_user_ids = [
    "delete_not_exist_user",
]