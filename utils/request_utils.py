import requests
from config import timeout
from utils.log_utils import get_logger

logger = get_logger()

def send_request(method,url,headers=None,json=None,params=None):
    """统一发送请求接口"""
    logger.info(f"请求方法：{method}")
    logger.info(f"请求地址：{url}")
    logger.info(f"请求参数 param:{params}")
    #本地环境练习：登录接口先打印账号、密码，生成环境不能打印
    # logger.info(f"请求体 json:{json}")

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

    logger.info(f"响应状态码：{response.status_code}")
    logger.info(f"响应内容{response.text}")

    return response