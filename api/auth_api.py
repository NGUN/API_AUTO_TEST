import requests
from config import login_url
from utils.request_utils import send_request

def login(username,password):
	"""登录接口"""
	login_data = {
		"username": username,
		"password": password
	}
	return send_request(method="POST",url=login_url,json=login_data)
