from __future__ import annotations

import asyncio
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mas.plugins import PluginContext

from .schema import Config


class Plugin:
    needs = "notify"

    def __init__(self, ctx: "PluginContext") -> None:
        self.ctx = ctx
        self._task: asyncio.Task[None] | None = None

    async def on_start(self) -> None:
        raw_config = self.ctx.config.to_dict() if hasattr(self.ctx.config, "to_dict") else dict(self.ctx.config)
        config = Config.model_validate(raw_config)
        if not config.enabled:
            self.ctx.logger.info("测试信息发送已关闭")
            return

        self._task = asyncio.create_task(self._send_after_channels_ready(config.delay_seconds))
        self.ctx.logger.info(
            f"已计划在 {config.delay_seconds} 秒后发送通知测试信息"
        )

    async def on_stop(self, reason: str) -> None:
        if self._task is not None and not self._task.done():
            self._task.cancel()
        self.ctx.logger.info(f"插件停止, reason={reason}")

    async def _send_after_channels_ready(self, delay_seconds: int) -> None:
        if delay_seconds > 0:
            await asyncio.sleep(delay_seconds)

        notify = self.ctx.get("notify")
        if notify is None:
            self.ctx.logger.warning("notify 服务不可用，跳过测试信息")
            return

        channels = self._channels(notify)
        if not channels:
            self.ctx.logger.warning("当前没有已注册通知渠道，测试信息未发送")
            return

        result = await notify.send_test_notification()
        succeeded = sorted(name for name, ok in result.items() if ok)
        failed = sorted(name for name, ok in result.items() if not ok)
        self.ctx.logger.info(
            f"测试信息发送完成，成功={succeeded or '无'}，失败={failed or '无'}"
        )

    def _channels(self, notify: Any) -> list[str]:
        channels = getattr(notify, "channels", None)
        if callable(channels):
            return list(channels())
        return []
