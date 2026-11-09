# Qt runtime 与 Flatpak 打包

[English](QtRuntime.md) · [Português (Brasil)](QtRuntime.pt-BR.md)

Qt 6 / Qt Quick 应用推荐用 **`org.kde.Platform`** 运行、用同分支同架构的 **`org.kde.Sdk`** 构建。这是可共享的 Flatpak 运行库，不需要另建一个 NextKde QtRuntime 包。宿主机装了 Qt、Plasma 或 Quickshell，也不能代替沙箱里的依赖。

目前 `NextKde/kos-apps` 使用 **6.11** 分支。这是现有项目的参考配置，并不表示所有应用必须用它或它永远是最新版。选择仍维护、包含所需 Qt 模块的分支，在开发虚拟机确认兼容性。参考 [Flatpak 官方运行库说明](https://docs.flatpak.org/en/latest/available-runtimes.html)与 [KDE manifest 指南](https://develop.kde.org/docs/packaging/flatpak/manifest/)。

## 怎样打包

[英文指南](QtRuntime.md#manifest-starting-point)提供完整 manifest 起点。核心配置为：

```json
{
  "runtime": "org.kde.Platform",
  "runtime-version": "6.11",
  "sdk": "org.kde.Sdk",
  "separate-locales": false
}
```

这只是 manifest 的部分字段，需填写真实 app-id、command、源码 commit 和构建模块。网络、音频、文件和 D-Bus 权限按实际需要添加；文件选择优先使用 portal。运行库没有的应用专用依赖放到 `/app`，不要混用宿主 Qt 或覆盖运行库 Qt。QML 模块、插件、桌面文件、图标和翻译均需正确安装进应用。

第一版推荐 `separate-locales: false`，把应用翻译留在主包。仅上传一个 bundle 不会自动发布独立 `.Locale` 扩展；客户端也不从任意开发者源获取扩展。运行库语言数据、应用自身翻译和目录名称翻译是三件不同的事，见[多语言约定](Localization.zh-CN.md)。

只在虚拟机或 CI 构建和验收：准备同架构 SDK/runtime，用 `flatpak-builder` 构建并导出 `stable` app ref，再用 `flatpak build-bundle` 导出单文件包。不要传入 `--repo-url` 或 `--runtime-repo`，包不能夹带在线来源。

从最终包与 OSTree 元数据生成 [schema 2 发行清单](../RELEASE-CONTRACT.zh-CN.md)：ref、commit、实际大小、SHA-256、runtime、扩展。metadata 必须按原始字节保留末尾换行后编码和计算摘要。不能拿源码压缩包的摘要代替安装包摘要。[kos-apps 打包脚本](https://github.com/NextKde/kos-apps/blob/main/packaging/flatpak/prepare-bundle.py)可作提取与签名参考，但它只支持该仓库的应用，不是通用打包器。

在虚拟机验收首装、升级、保留数据卸载、离线启动和每个声明的架构，然后上传到正式 `vX.Y.Z` GitHub Release。上传包、清单及已配置的开发者签名，再提交目录 PR。

## 用户安装时会发生什么

应用包始终从登记的 GitHub Release 下载。缺失的运行库由客户端独立批准、固定公钥的 Flathub runtime 源提供；应用本身不必上架 Flathub。用户明确安装/更新时，客户端可准备这个运行库源。信任第三方目录并不等于批准它添加任意运行库源。

同 ID、架构、分支和可信来源的运行库可复用，多个应用无需各带一份完整 Qt。首次下载可能较大，确认界面会展示依赖与下载计划。取消安装后，已准备的运行库源可能保留。依赖不可用就停止安装，不回退宿主 Qt。
