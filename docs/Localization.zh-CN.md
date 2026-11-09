# 目录多语言约定

[English](Localization.md) · [Português (Brasil)](Localization.pt-BR.md)

`name` 和 `description` 使用语言映射，两者都必须有非空 `en` 兜底。当前 Settings 界面支持 `en`、`zh-CN`、`pt-BR`，目录可预留其他合法语言标签；缺少翻译时回退英文。文档支持某语言不表示界面也已支持。

```json
"name": {"en": "Calendar", "zh-CN": "日历", "pt-BR": "Calendário"},
"description": {"en": "Plan your days and events", "zh-CN": "安排日程与活动", "pt-BR": "Organize seus dias e eventos"}
```

appId、key、format、repository、manifest、status 和指纹不能翻译。名称最多 120 字符，简介最多 600 字符，每个字段最多 32 个语言；使用纯文本，不放 HTML/Markdown、控制字符或空字符串。翻译经 PR 审核并发布新签名目录生效，不需要重发应用安装包。

应用自身界面翻译由应用打包，独立于目录翻译。首版建议 `separate-locales: false`，不能假设应用独立 Locale 扩展已在可信运行库源存在。见 [Qt runtime 指南](QtRuntime.zh-CN.md)。
