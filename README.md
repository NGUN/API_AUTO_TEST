# API_AUTO_TEST

Python + Pytest + Requests 接口自动化练习项目。

## 项目简介

本项目用于学习接口自动化测试基础，覆盖登录鉴权、Token 复用、接口分层、参数化、断言封装、动态数据、日志、测试报告等内容。

## 项目结构

```text
API_AUTO_TEST/
├── api/                    # 接口请求层
│   ├── auth_api.py          # 登录接口
│   └── user_api.py          # 用户相关接口
├── data/                   # 测试数据
│   └── login_data.py        # 登录参数化数据
├── testcases/              # 测试用例
│   ├── test_login.py        # 登录接口用例
│   └── test_user.py         # 用户接口用例
├── utils/                  # 工具方法
│   ├── assert_utils.py      # 公共断言方法
│   ├── data_utils.py        # 动态测试数据
│   └── log_utils.py         # 日志工具
├── reports/                # 测试报告目录
│   └── report.html
├── config.py               # 环境地址和接口路径配置
├── conftest.py             # pytest 公共 fixture，如 token、headers
├── pytest.ini              # pytest 配置
├── requirements.txt        # 项目依赖
└── README.md
```

## 安装依赖

```powershell
pip install -r requirements.txt
```

`requirements.txt` 示例：

```text
pytest
requests
pytest-html
allure-pytest
```

## 运行全部用例

```powershell
pytest
```

## 环境切换

默认运行本地环境：

```powershell
pytest
```

指定测试环境：

```powershell
$env:ENV="test"
pytest
```

环境配置在 `config.py` 中维护。

## 按标记运行

只运行冒烟用例：

```powershell
pytest -m smoke
```

只运行反向用例：

```powershell
pytest -m negative
```

不运行写数据用例：

```powershell
pytest -m "not write"
```

## 统一请求封装

项目通过 `utils/request_utils.py` 中的 `send_request()` 统一发送接口请求。

主要作用：

- 统一处理 `GET`、`POST` 等请求
- 统一使用 `timeout`
- 统一记录请求和响应日志
- 统一捕获请求异常
- 避免每个接口函数重复写 `requests.get()`、`requests.post()`

## 生成pytest-html测试报告

```powershell
pytest --html=reports/report.html --self-contained-html
```

报告生成后位置：

```text
reports/report.html
```

## Allure 报告

安装依赖：

```powershell
pip install allure-pytest
```

生成 Allure 原始结果：

```powershell
pytest --alluredir=reports/allure-results
```

打开 Allure 报告：

```powershell
allure serve reports/allure-results
```

也可以直接运行脚本：

```powershell
.\run_allure.bat
```

## Allure 用例信息

项目中使用了以下 Allure 能力：

- `@allure.feature`：模块分类
- `@allure.story`：功能场景
- `@allure.title`：用例标题
- `allure.dynamic.title()`：参数化用例动态标题
- `with allure.step()`：展示用例执行步骤
- `@allure.severity`：标记用例严重级别

## 当前已实现

- 登录接口参数化测试
- session 级 Token 复用
- headers 统一管理
- 查询当前用户接口
- 查询用户列表接口
- 创建用户接口
- 无 Token 反向用例
- 创建用户动态数据
- 测试数据独立管理
- 公共断言方法封装
- logging 日志输出
- pytest marker 用例标记
- pytest-html 测试报告
- 环境变量切换 base_url

## 注意事项

- 运行用例前，需要确保被测接口服务已启动。
- 日志中不要打印密码、Token 等敏感信息。
- 创建、修改、删除类接口建议标记为 `write`。
- 生产环境不建议执行写数据类用例。