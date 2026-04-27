from pydantic import BaseModel, ConfigDict, Field


class Config(BaseModel):
    model_config = ConfigDict(extra="allow")

    enabled: bool = Field(
        default=True,
        description="启动时发送测试信息",
    )
    delay_seconds: int = Field(
        default=2,
        ge=0,
        description="启动后延迟秒数",
    )
