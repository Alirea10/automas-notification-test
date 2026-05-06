from typing import Any

from app.plugins.fields import PluginField
from pydantic import BaseModel, ConfigDict


class Config(BaseModel):
    model_config = ConfigDict(extra="allow")

    send_test_button: Any = PluginField(
        default=None,
        title="发送测试通知",
        description="点击按钮向所有已注册通知渠道发送测试消息",
        ui_type="button",
        configurable=False,
        action={
            "label": "发送测试通知",
            "path": "/notification-test/send",
            "method": "POST",
        },
    )
