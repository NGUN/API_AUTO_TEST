# API_AUTO_TEST

基于 Python + Pytest + Requests + Allure 的接口自动化测试学习项目。

项目覆盖登录接口、用户接口 CRUD、Token 复用、YAML 数据驱动、统一请求封装、统一断言封装、日志脱敏、Allure 报告、pytest-html 报告、多环境配置等接口自动化核心能力。

## 技术栈

- Python
- Pytest
- Requests
- PyYAML
- Allure
- pytest-html
- logging

## 项目结构

```text
API_AUTO_TEST/
├── api/                    # 接口请求层
│   ├── auth_api.py          # 登录接口封装
│   └── user_api.py          # 用户接口封装
├── data/                   # 测试数据层
│   ├── login_data.py        # 登录测试数据读取与加工
│   ├── login_data.yaml      # 登录 YAML 测试数据
│   ├── user_data.py         # 用户测试数据读取与加工
│   └── user_data.yaml       # 用户 YAML 测试数据
├── testcases/              # 测试用例层
│   ├── test_login.py        # 登录模块用例
│   └── test_user.py         # 用户模块用例
├── utils/                  # 公共工具层
│   ├── allure_utils.py      # Allure 附件、环境信息、执行信息工具
│   ├── assert_utils.py      # 公共断言方法
│   ├── data_utils.py        # 动态测试数据生成
│   ├── log_utils.py         # 日志工具
│   ├── request_utils.py     # 统一请求封装
│   └── yaml_utils.py        # YAML 读取工具
├── reports/                # 测试报告目录
├── config.py               # 环境、接口地址、账号、报告配置
├── conftest.py             # pytest 公共 fixture
├── pytest.ini              # pytest 配置
├── requirements.txt        # 项目依赖
├── run_allure.bat          # 生成并打开 Allure 报告
├── run_html_report.bat     # 生成 pytest-html 报告
└── README.md
```

## 已覆盖模块

### 登录模块

- 正确账号密码登录成功
- 错误密码登录失败
- 空账号登录失败
- 空密码登录失败
- 错误账号登录失败

### 用户模块

- 获取当前用户信息成功
- 无 Token 获取当前用户信息失败
- 查询用户列表成功
- 根据用户 id 查询用户详情成功
- 查询不存在用户详情失败
- 创建用户成功
- 创建用户后列表可查询到该用户
- 创建用户缺少必填字段失败
- 创建用户字段为空失败
- 创建用户缺少非必填字段 email 成功
- 重复 username 创建用户失败
- 重复 username 创建失败后未新增脏数据
- 更新用户邮箱和密码成功
- 更新用户名不生效
- 更新不存在用户失败
- 无 Token / 无效 Token / Token 格式错误更新用户失败
- 更新失败后原用户数据不变
- 删除用户成功
- 删除不存在用户失败
- 删除同一个用户两次，第二次失败
- 用户 CRUD 完整链路

## 核心设计

### 接口分层

接口请求统一封装在 `api/` 目录。

测试用例不直接调用 `requests.get()`、`requests.post()`，也不直接拼接接口 URL，而是调用接口层方法。

示例：

```python
def get_users(headers):
    return send_request(method="GET", url=users_url, headers=headers)
```

这样测试用例可以更关注业务流程和断言，接口路径变更时也更容易维护。

### 统一请求封装

`utils/request_utils.py` 中的 `send_request()` 负责统一发送接口请求。

主要能力：

- 统一发送 HTTP 请求
- 统一设置 timeout
- 统一打印请求日志
- 统一打印响应日志
- 统一捕获 requests 请求异常
- 对 password、token、Authorization 进行日志脱敏
- 返回原始 response 对象，方便后续断言

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

所有需要鉴权的用例都可以直接使用 `headers` fixture。

### 测试数据自动清理

用户模块通过 fixture 创建测试用户，并在用例执行结束后自动删除。

核心流程：

```text
前置：创建测试用户
用例：查询 / 更新 / 删除该用户
后置：自动清理测试用户
```

对于删除类用例，用例中可能已经主动删除用户，因此后置清理允许返回：

```text
200：清理成功
404：用户已经被用例删除，也视为清理完成
```

### YAML 数据驱动

项目使用 YAML 管理测试数据。

示例：

```yaml
login_cases:
  - id: login_success
    case_title: 正确账号密码登录成功
    username: ${API_USERNAME}
    password: ${API_PASSWORD}
    expected_status: 200
    expected_code: 200
    expected_data: not_none
```

`data/*.py` 负责读取 YAML，并生成参数化用例需要的数据和 ids。

```python
login_case_ids = [
    case["id"] for case in login_cases
]
```

测试用例中使用：

```python
@pytest.mark.parametrize(
    "case",
    login_cases,
    ids=login_case_ids,
)
```

### 统一断言封装

`utils/assert_utils.py` 中封装了公共断言方法。

包括：

- HTTP 状态码断言
- 业务 code 断言
- data 为空断言
- data 不为空断言
- 根据 `expected_data` 自动断言 data
- 用户是否存在于列表
- 用户是否不存在于列表
- 基础响应统一断言 `assert_response_basic()`

示例：

```python
body = assert_response_basic(
    response,
    case["expected_status"],
    case["expected_code"],
    case["expected_data"],
)
```

公共断言方法中加入了明确的失败信息，失败时可以直接看到期望值、实际值和响应内容，方便排查问题。

### Allure 报告

项目使用 Allure 展示测试报告。

用例中通过：

```python
@allure.feature("用户模块")
@allure.story("用户 CRUD 链路")
@allure.title("用户 CRUD 完整链路成功")
```

组织报告层级。

项目还会写入 Allure 报告环境信息和执行信息：

```text
Environment:
- ENV
- base_url

Executors:
- executor name
- build name
```

方便区分不同环境、不同执行来源的测试结果。

## 环境配置

环境配置统一维护在 `config.py` 中。

默认环境：

```text
local
```

默认本地地址：

```text
http://127.0.0.1:11011
```

支持环境：

```text
local
test
pre
```

### PowerShell 设置环境

```powershell
$env:ENV="local"
$env:API_USERNAME="admin"
$env:API_PASSWORD="admin123"
pytest -q
```

### CMD 设置环境

```cmd
set ENV=local
set API_USERNAME=admin
set API_PASSWORD=admin123
pytest -q
```

## 报告配置

Allure 原始结果目录支持通过环境变量配置。

默认目录：

```text
reports/allure-results
```

CMD 示例：

```cmd
set ALLURE_RESULTS_DIR=reports\allure-results
pytest --alluredir=%ALLURE_RESULTS_DIR% --clean-alluredir
allure serve %ALLURE_RESULTS_DIR%
```

执行信息也支持通过环境变量配置：

```cmd
set EXECUTOR_NAME=local-cmd
set EXECUTOR_TYPE=local
set BUILD_NAME=API_AUTO_TEST_001
set REPORT_NAME=API自动化测试报告-本地调试
```

## 安装依赖

```cmd
pip install -r requirements.txt
```

`requirements.txt` 建议包含：

```text
pytest
requests
pytest-html
allure-pytest
pyyaml
```

Allure 报告需要单独安装 Allure Commandline，并确保 `allure` 命令已加入系统 PATH。

检查命令：

```cmd
allure --version
```

## 快速运行

生成并打开 Allure 报告：

```cmd
run_allure.bat
```

生成 pytest-html 单文件报告：

```cmd
run_html_report.bat
```

手动运行全部用例：

```cmd
pytest -q
```

只收集用例：

```cmd
pytest --collect-only -q
```

## 常用命令

运行全部用例：

```cmd
pytest
```

简洁模式运行全部用例：

```cmd
pytest -q
```

运行登录模块：

```cmd
pytest -k test_login_params -s -v
```

运行用户模块：

```cmd
pytest testcases/test_user.py -s -v
```

按关键字运行：

```cmd
pytest -k login
pytest -k create_user
pytest -k update
pytest -k delete
```

## Marker 说明

项目在 `pytest.ini` 中维护 marker。

```ini
markers =
    smoke: 冒烟用例，核心主流程
    negative: 反向用例，异常场景
    write: 会新增、修改或删除数据的用例
```

运行冒烟用例：

```cmd
pytest -m smoke -s -v
```

运行反向用例：

```cmd
pytest -m negative -s -v
```

运行写数据用例：

```cmd
pytest -m write -s -v
```

跳过写数据用例：

```cmd
pytest -m "not write" -s -v
```

## 测试报告

### Allure 报告

生成 Allure 原始结果：

```cmd
pytest --alluredir=reports\allure-results --clean-alluredir
```

打开 Allure 报告：

```cmd
allure serve reports\allure-results
```

或者直接运行：

```cmd
run_allure.bat
```

### pytest-html 报告

生成 HTML 报告：

```cmd
pytest --html=reports\report.html --self-contained-html
```

或者直接运行：

```cmd
run_html_report.bat
```

报告位置：

```text
reports/report.html
```

## 当前用例统计

当前项目共覆盖：

```text
29 条自动化测试用例
```

模块分布：

```text
登录模块：5 条
用户模块：24 条
```

## 提交前检查

提交代码前建议执行：

```cmd
pytest --collect-only -q
pytest -q
run_allure.bat
run_html_report.bat
```

检查点：

- 用例可以正常收集
- 全量用例全部通过
- YAML 数据字段完整
- 参数化用例 ids 清晰
- 写数据用例已标记 `write`
- 反向用例已标记 `negative`
- 冒烟主流程已标记 `smoke`
- 测试用户能自动清理
- 日志中没有明文 password、token、Authorization
- Allure 报告中没有 failed 或 broken
- pytest-html 报告可以正常打开

## 项目亮点

- 使用接口层封装请求，测试用例不直接拼接 URL
- 使用统一请求工具管理请求、日志、超时和异常
- 使用 session 级 fixture 实现 Token 复用
- 使用 fixture 实现测试数据创建和自动清理
- 使用 YAML 管理登录和用户模块测试数据
- 使用 `pytest.mark.parametrize` 实现数据驱动
- 使用 `ids` 提升参数化用例可读性
- 使用公共断言方法减少重复代码
- 使用统一基础响应断言校验 HTTP 状态码、业务 code 和 data
- 断言失败时提供清晰错误信息
- 使用 Allure step 和附件提升报告可读性
- 支持 Allure 环境信息和执行信息展示
- 同时支持 Allure 和 pytest-html 两种报告
- 对敏感字段进行日志脱敏
- 覆盖用户接口 CRUD 主链路和关键反向场景

## 面试说明

可以这样介绍本项目：

```text
这是一个基于 Python + Pytest + Requests 的接口自动化测试项目。
项目使用 api 层封装接口请求，使用 YAML 管理测试数据，通过 pytest 参数化实现数据驱动。
项目中使用 fixture 实现 Token 复用和测试用户自动清理，使用统一请求封装处理日志、超时和异常。
断言层封装了状态码、业务 code、data 字段和基础响应断言，并增加了失败信息，方便问题定位。
报告方面同时支持 Allure 和 pytest-html，Allure 中展示了测试步骤、接口响应附件、运行环境和执行信息。
```

## 注意事项

- 运行用例前，需要确保被测接口服务已启动
- 本地默认接口地址为 `http://127.0.0.1:11011`
- 写数据用例会创建、更新或删除测试数据
- 不建议在生产环境执行 `write` 类用例
- 如果接口契约变化，需要同步调整 YAML 中的预期状态码、业务 code 和 data 预期
- Allure 报告如果出现历史失败记录，需要使用 `--clean-alluredir` 清理旧结果
- CMD 使用 `%变量名%` 读取环境变量，PowerShell 使用 `$env:变量名`