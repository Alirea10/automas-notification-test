# automas_plugin_notification_test

启动时通过 `notify` 服务向所有已注册通知渠道发送一条测试信息。

该插件只负责触发测试发送，不提供新的通知渠道。请先启用 `notification` 核心插件，并按需启用 `notification_mail`、`notification_system`、`notification_serverchan`、`notification_webhook`、`notification_koishi` 等通道插件。
