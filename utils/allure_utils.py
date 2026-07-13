import allure

def attach_response(response, name="接口响应"):
    """把接口响应内容附加到 Allure 报告"""

    allure.attach(
        response.text,
        name=name,
        attachment_type=allure.attachment_type.JSON
    )