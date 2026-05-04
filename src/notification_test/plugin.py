from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mas.plugins import PluginContext, PluginHttpRequest


class Plugin:
    needs = "notify"

    def __init__(self, ctx: "PluginContext") -> None:
        self.ctx = ctx

    async def on_start(self) -> None:
        self.ctx.server.http(
            "/notification-test/send",
            self.handle_send,
            methods=["POST"],
        )
        self.ctx.server.action(
            id="notification_test_send",
            label="发送测试通知",
            path="/notification-test/send",
            method="POST",
        )
        self.ctx.logger.info("测试通知插件已启动，点击按钮发送测试消息")

    async def on_stop(self, reason: str) -> None:
        self.ctx.logger.info(f"插件停止, reason={reason}")

    async def handle_send(self, request: "PluginHttpRequest") -> dict[str, Any]:
        notify = self.ctx.get("notify")
        if notify is None:
            return {"code": 503, "status": "error", "message": "notify 服务不可用"}

        channels = self._channels(notify)
        if not channels:
            return {"code": 400, "status": "error", "message": "当前没有已注册通知渠道"}

        result = await notify.send_test_notification()
        succeeded = sorted(name for name, ok in result.items() if ok)
        failed = sorted(name for name, ok in result.items() if not ok)

        self.ctx.logger.info(
            f"测试信息发送完成，成功={succeeded or '无'}，失败={failed or '无'}"
        )
        return {
            "code": 200,
            "status": "success",
            "succeeded": succeeded,
            "failed": failed,
        }

    def _channels(self, notify: Any) -> list[str]:
        channels = getattr(notify, "channels", None)
        if callable(channels):
            return list(channels())
        return []
