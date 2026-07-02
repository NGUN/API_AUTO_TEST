from config import username, password

login_cases = 	[
	("正确账号密码登录成功",username, password, 200, 200),
	("错误密码登录失败","admin", "wrong123", 401, 401),
	("空账号登录失败","","admin123", 400, 400)
]