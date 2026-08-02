import time

def build_create_user_data():
    """生成创建用户接口需要的动态数据"""
    now = time.time_ns()

    return {
        "username": f"xiaoyitest{now}",
        "password": "Aa123456",
        "email": f"1661640776{now}@qq.com"
    }
