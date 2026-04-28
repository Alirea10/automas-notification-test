from mas.plugin_config import PluginField
from pydantic import BaseModel, ConfigDict


class Config(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool = PluginField(
        default=True,
        description="启动时发送测试信息",
    )
    delay_seconds: int = PluginField(
        default=2,
        ge=0,
        description="启动后延迟秒数",
    )
