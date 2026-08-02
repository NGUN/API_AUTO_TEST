from utils.yaml_utils import load_yaml

#公共测试数据
not_exist_user_id = "not-exist-user-id"

# 创建用户相关数据
yaml_data = load_yaml("data/user_data.yaml")

create_user_invalid_field_data = yaml_data["create_user_invalid_field"]

create_user_invalid_field_ids = [
    case["id"] for case in create_user_invalid_field_data
]

create_user_duplicate_username_data = yaml_data["create_user_duplicate_username"]

create_user_duplicate_username_ids = [
    case["id"] for case in create_user_duplicate_username_data
]

# 查询用户相关数据
get_not_exist_user_by_id_data = yaml_data["get_not_exist_user_by_id"]

get_not_exist_user_by_id_ids = [
    case["id"] for case in get_not_exist_user_by_id_data
]

# 更新用户相关数据
update_username_ignored_data = yaml_data["update_username_ignored"]

update_username_ignored_ids = [
    case["id"] for case in update_username_ignored_data
]

update_not_exist_user_data = yaml_data["update_not_exist_user"]

update_not_exist_user_ids = [
    case["id"] for case in update_not_exist_user_data
]

update_user_without_token_data = yaml_data["update_user_without_token"]

update_user_without_token_ids = [
    case["id"] for case in update_user_without_token_data
]

# 删除用户相关数据
delete_not_exist_user_data = yaml_data["delete_not_exist_user"]

delete_not_exist_user_ids = [
    case["id"] for case in delete_not_exist_user_data
]
