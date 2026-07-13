import requests
from config import current_user_url,users_url
from utils.request_utils import send_request

def get_current_user(headers):
	"""获取当前用户信息接口"""
	return send_request(method="GET",url=current_user_url,headers=headers)

def get_users(headers):
	"""获取用户列表接口"""
	return send_request(method="GET",url=users_url,headers=headers)

def create_user(headers,create_user_data):
	"""创建用户接口"""
	return send_request(method="POST",url=users_url,headers=headers,json=create_user_data)

def update_user(headers,user_id,update_user_data):
	"""更新用户接口"""
	return send_request(method="PUT",url=f"{users_url}/{user_id}",headers=headers,json=update_user_data)

def delete_user(headers,user_id):
	"""删除用户接口"""
	return send_request(method="DELETE",url=f"{users_url}/{user_id}",headers=headers)

def get_user_by_id(headers,user_id):
	"""根据用户 id 查询用户详情"""
	return send_request(method="GET",url=f"{users_url}/{user_id}",headers=headers)
