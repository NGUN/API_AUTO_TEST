# API_AUTO_TEST

基于 Python + Pytest + Requests 的接口自动化测试练习项目。

项目覆盖登录鉴权、Token 复用、接口分层、统一请求封装、动态测试数据、fixture 前后置清理、数据驱动、pytest marker 分类运行、Allure 报告等接口自动化核心能力。

## 技术栈

- Python
- Pytest
- Requests
- Allure
- pytest-html
- logging

## 项目结构

```text
API_AUTO_TEST/
├── api/                    # 接口请求层
│   ├── auth_api.py          # 登录接口
│   └── user_api.py          # 用户相关接口
├── data/                   # 测试数据层
│   ├── login_data.py        # 登录参数化数据
│   └── user_data.py         # 用户模块参数化数据
├── testcases/              # 测试用例层
│   ├── test_login.py        # 登录接口用例
│   └── test_user.py         # 用户接口用例
├── utils/                  # 公共工具层
│   ├── allure_utils.py      # Allure 附件工具
│   ├── assert_utils.py      # 公共断言方法
│   ├── data_utils.py        # 动态测试数据生成
│   ├── log_utils.py         # 日志工具
│   └── request_utils.py     # 统一请求封装
├── reports/                # 测试报告目录
├── config.py               # 环境地址和接口路径配置
├── conftest.py             # pytest 公共 fixture
├── pytest.ini              # pytest 配置
├── requirements.txt        # 项目依赖
├── run_allure.bat          # Allure 报告启动脚本
└── README.md
```

## 已覆盖接口

### 登录模块

- 登录接口

### 用户模块

- 获取当前用户接口
- 查询用户列表接口
- 根据用户 id 查询用户详情接口
- 创建用户接口
- 更新用户接口
- 删除用户接口

## 已覆盖测试场景

### 登录模块

- 正确账号密码登录成功
- 错误密码登录失败
- 空账号登录失败

### 用户模块

- 获取当前用户成功
- 无 Token 获取当前用户失败
- 查询用户列表成功
- 根据用户 id 查询用户详情成功
- 查询不存在用户详情失败
- 创建用户成功
- 创建用户后列表可查询到
- 创建用户缺少必填字段失败
- 创建用户字段为空失败
- 创建用户缺少非必填字段 email 成功
- 重复 username 创建失败
- 更新用户 email 和 password 成功
- 更新 username 不生效
- 更新不存在用户失败
- 删除用户成功
- 删除不存在用户失败

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

## 环境配置

环境地址在 `config.py` 中维护。

默认使用本地环境：

```powershell
pytest
```

指定测试环境：

```powershell
$env:ENV="test"
pytest
```

支持的环境示例：

```text
local
test
pre
```

账号密码支持通过环境变量配置：

```powershell
$env:API_USERNAME="admin"
$env:API_PASSWORD="admin123"
pytest
```

## 运行用例

运行全部用例：

```powershell
pytest
```

只运行冒烟用例：

```powershell
pytest -m smoke
```

只运行反向用例：

```powershell
pytest -m negative
```

跳过写数据用例：

```powershell
pytest -m "not write"
```

只运行写数据用例：

```powershell
pytest -m write
```

只收集用例，不执行接口请求：

```powershell
pytest --collect-only -q
```

按关键字运行：

```powershell
pytest -k login
pytest -k create_user
pytest -k update
pytest -k delete
```

## pytest marker 说明

项目在 `pytest.ini` 中维护 marker：

```ini
markers =
    smoke: 冒烟用例，核心主流程
    negative: 反向用例，异常场景
    write: 会新增、修改、删除数据的用例
```

marker 使用规则：

- `smoke`：核心正向主流程
- `negative`：异常场景、反向场景
- `write`：执行过程中会新增、修改或删除数据的用例

注意：

- 如果用例依赖 `created_user` fixture，即使用例主体是 GET，也应该标记为 `write`
- 纯查询且不依赖创建数据的 GET 用例，不需要标记 `write`

## 测试报告

### pytest-html 报告

生成 HTML 报告：

```powershell
pytest --html=reports/report.html --self-contained-html
```

报告位置：

```text
reports/report.html
```

### Allure 报告

生成 Allure 原始结果：

```powershell
pytest --alluredir=reports/allure-results
```

启动 Allure 报告：

```powershell
allure serve reports/allure-results
```

也可以运行脚本：

```powershell
.\run_allure.bat
```

## 项目设计说明

### 接口分层

接口请求统一封装在 `api/` 目录中。

测试用例不直接拼接 URL，也不直接调用 `requests.get()` 或 `requests.post()`。

示例：

```python
def get_users(headers):
    return send_request(method="GET", url=users_url, headers=headers)
```

### 统一请求封装

`utils/request_utils.py` 中的 `send_request()` 负责：

- 统一发送请求
- 统一设置 timeout
- 统一打印请求日志
- 统一打印响应日志
- 统一捕获 `requests.exceptions.RequestException`
- 统一对敏感数据脱敏
- 返回原始 response 对象

请求封装不负责业务断言。

业务断言放在测试用例或 `utils/assert_utils.py` 中。

### Token 复用

`conftest.py` 中通过 session 级 fixture 获取并复用 Token。

```python
@pytest.fixture(scope="session")
def token():
    return get_token()

@pytest.fixture(scope="session")
def headers(token):
    return {"Authorization": f"Bearer {token}"}
```

### 测试数据清理

写数据用例通过 fixture 创建测试用户，并在用例结束后自动删除。

删除接口相关用例可能会在用例中主动删除用户，因此 fixture 后置清理允许返回 `200` 或 `404`。

```text
200：清理成功
404：用户已经被用例删除，也视为清理完成
```

### 数据驱动

项目使用 `pytest.mark.parametrize` 管理多组测试数据。

简单数据可以使用元组格式：

```python
[
    ("重复 username 创建用户失败", 400, 400),
]
```

字段较多的数据使用字典格式：

```python
[
    {
        "case_title": "创建用户失败-缺少用户名",
        "action": "pop",
        "field": "username",
        "value": None,
        "case_desc": "删除 username 字段",
        "expected_status": 400,
        "expected_code": 400,
    }
]
```

参数化用例使用 `ids` 提升可读性：

```python
@pytest.mark.parametrize(
    "case",
    create_user_invalid_field_data,
    ids=create_user_invalid_field_ids,
)
```

运行时可以清楚看到失败的是哪一组数据：

```text
test_create_user_invalid_field[missing_username]
test_create_user_invalid_field[empty_password]
```

## 日志与敏感数据

项目会打印请求和响应日志，方便排查问题。

敏感字段会脱敏：

- password
- token
- Authorization

日志示例：

```text
请求头 headers:{'Authorization': '******'}
请求体 json:{'username': 'admin', 'password': '******'}
```

注意：

- 真实 token 不应打印到日志中
- 真实密码不应打印到日志中
- 脱敏只用于日志，不影响真实请求数据

## 提交前检查清单

提交代码前建议执行：

```powershell
pytest --collect-only -q
```

确认用例能正常收集。

再执行：

```powershell
pytest -q
```

确认全量用例通过。

也可以按 marker 分组检查：

```powershell
pytest -q -m smoke
pytest -q -m negative
pytest -q -m "not write"
pytest -q -m write
```

检查点：

- 参数化数据字段数量正确
- 参数化用例都有 ids
- 写数据用例都有 `@pytest.mark.write`
- 查询类用例没有误标 `write`
- fixture 创建的数据能被清理
- 日志中没有明文 password、token
- 全量用例执行通过

## 项目亮点

- 使用接口层封装请求，测试用例不直接拼接 URL
- 使用统一请求工具管理请求、日志、超时和异常
- 使用 session 级 fixture 实现 Token 复用
- 使用 fixture 实现测试数据创建和自动清理
- 使用 data 目录集中管理参数化测试数据
- 使用字典格式维护复杂测试数据，可读性更高
- 使用 pytest marker 实现用例分组运行
- 使用 Allure step 和附件提升报告可读性
- 对敏感字段进行日志脱敏
- 覆盖用户接口 CRUD 正向链路和关键反向场景

## 注意事项

- 运行用例前，需要确保被测接口服务已启动
- 本地环境默认地址配置在 `config.py`
- 写数据用例会创建、更新或删除测试数据
- 生产环境不建议执行 `write` 类用例
- 如果接口契约变化，需要同步调整 `data/user_data.py` 中的预期状态码和业务 code