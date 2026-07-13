import requests
from config import timeout
from utils.log_utils import get_logger

logger = get_logger()

def mask_sensitive_data(data):
    """原始敏感数据"""

    if data is None:
        return None

    if not isinstance(data, dict):
        return data

    safe_data = data.copy()

    for key in safe_data:
        if key.lower() in ["password", "token", "authorization"]:
            safe_data[key] = "******"

    return safe_data

def send_request(method,url,headers=None,json=None,params=None):
    """统一发送请求接口"""
    logger.info("===========接口请求开始============")
    logger.info(f"请求方法：{method}")
    logger.info(f"请求地址：{url}")
    logger.info(f"请求头 headers:{mask_sensitive_data(headers)}")
    logger.info(f"请求参数 param:{params}")
    #本地环境练习：登录接口先打印账号、密码，生成环境不能打印
    # logger.info(f"请求体 json:{json}")
    logger.info(f"请求体 json:{mask_sensitive_data(json)}")

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            params=params,
            timeout=timeout
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"请求接口失败：{e}")
        raise

    logger.info("-----------接口响应---------------")
    logger.info(f"响应状态码：{response.status_code}")
    logger.info(f"响应耗时：{response.elapsed.total_seconds()}秒")
    logger.info(f"响应内容{response.text}")
    logger.info("===========接口请求结束============")

    return response

def get_json(response):
    """安全获取响应 JSON"""

    try:
        return response.json()
    except ValueError:
        logger.error(f"响应不是合法 JSON，响应内容：{response.text}")
        raise
