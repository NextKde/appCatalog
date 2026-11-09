# NextKde appCatalog

[English](README.md) · **简体中文** · [Português (Brasil)](README.pt-BR.md)

NextKde「应用与服务」的应用投稿目录。**此目录的客户端改造尚待虚拟机验收，不能据此声明现有发行版已支持。**

应用安装包保存在开发者自己的 **GitHub Releases**。本仓库只维护应用身份、介绍和发行仓库，不托管或执行第三方安装脚本。

投稿者请同时阅读 [Qt runtime 与打包指南](docs/QtRuntime.zh-CN.md)、[多语言约定](docs/Localization.zh-CN.md)和[发行协议](RELEASE-CONTRACT.zh-CN.md)。客户端架构见 [NextKde 主仓库](https://github.com/NextKde/NextKde/blob/main/docs/app-store/SignedCatalog.zh-CN.md)。

## 开发者如何上架

1. 准备稳定的应用 ID 和 Flatpak 单文件包，在自己的 GitHub 仓库创建正式 Release，tag 使用 `vX.Y.Z`，不使用草稿或预发行。
2. 上传 `.flatpak` 包及对应发行清单（见 [发行协议](RELEASE-CONTRACT.md)）。SHA-256 必填，开发者签名可选。
3. 在 `apps/` 新建 `<appId>.json`，按下面的条目格式提交 PR。
4. 维护者核对仓库归属、应用身份、安装权限和发行附件，合并后发布签名目录。客户端刷新后即可显示。

```json
{
  "appId": "org.example.Notes",
  "key": "notes",
  "format": "flatpak",
  "name": {"en": "Notes", "zh-CN": "笔记"},
  "description": {"en": "A small notes application", "zh-CN": "轻量笔记应用"},
  "repository": "example-org/notes",
  "manifest": "flatpak-release.json",
  "status": "active"
}
```

`repository` 必须是 GitHub 的 `owner/repository`。当前只安装 Flatpak；其他包格式需要客户端对应后端，不能通过目录绕过。

可选 `publisher` 包含 `fingerprint`（完整主密钥指纹）及 `publicKey`（二进制公钥的 Base64）。一旦配置，客户端严格要求 `.sig` 和包内 commit 签名，不会因签名缺失或失败退回无签名模式。没有配置时依赖已批准的 GitHub 仓库、HTTPS 和 SHA-256；仓库被盗后同时替换包和摘要不在该模式的防护范围内。

发布应用新版通常不改本目录。下架可将 `status` 改为 `withdrawn` 或删除条目；停止信任可用 `revoked`。这些操作阻止后续安装/更新，不删除用户已有应用或资料。

## 维护者发布目录

PR 工作流只检查数据结构，不下载或运行投稿者的程序，不接触签名私钥。

1. 审核并合并投稿。在 GitHub 设置 `catalog-release` environment，由维护者配置审批人员。
2. environment secret `CATALOG_SIGNING_PRIVATE_KEY` 保存 ASCII armored 签名私钥；需要口令时配置 `CATALOG_SIGNING_PASSPHRASE`。
3. 手动运行 Publish catalog，填写高于历史所有发布的整数序号。默认有效期 30 天，过期前重新发布。
4. 工作流生成 `catalog.json`，对其原始字节签名，创建正式 GitHub Release，附件为 `catalog.json` 和 `catalog.json.sig`。

首次发布前必须配置信任根对应的私钥。仓库中的 `catalog-public.gpg` 及 `catalog-fingerprint.txt` 是当前客户端 bootstrap 信任根的公开信息；私钥不在仓库中。当前沿用核心已内置的发布公钥作为启动信任根，不自动生成或偷偷替换密钥。若改用独立目录密钥，首次客户端发行前必须同步 pin 新公钥。

初始五款应用保留现有开发者签名要求。目录发布不会自动替这些应用创建可安装的 Release。

本地准备（在开发虚拟机执行）：

```sh
python3 build_catalog.py --check
python3 build_catalog.py --sequence 1
# 用真实维护者密钥签原始文件，签完不得重新格式化 JSON。
gpg --batch --armor --detach-sign --output dist/catalog.json.sig dist/catalog.json
```

## 第三方目录

可以复制此仓库的格式，在自己的 GitHub 仓库发布签名目录。`sourceId` 必须与用户添加时填写的来源标识一致，使用自己的公钥和完整指纹。

用户在 Settings → 应用与服务 → 管理应用来源中，填写来源标识、GitHub 仓库、公钥文件路径及完整指纹，明确选择信任后添加。公钥文件为 `gpg --export KEY > catalog-public.gpg` 产生的二进制文件。

不同目录不能静默覆盖相同应用 ID。下架或移除目录后仍保留已安装应用的打开/卸载入口。

目录签名证明目录由受信维护者发布；摘要证明下载与发行清单一致。这些均不保证应用没有恶意行为或漏洞。
