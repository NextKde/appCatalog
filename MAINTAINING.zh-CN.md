# 目录维护与发布

[English](MAINTAINING.md) · [Português (Brasil)](MAINTAINING.pt-BR.md)

投稿 PR 在 GitHub 托管虚拟机运行格式检查，不运行投稿程序、不下载安装器，也不接触私钥。格式通过不等于安全审核。合并前核对仓库归属、应用 ID 冲突、正式 Release 附件、Flatpak 权限、runtime/扩展可用性、SHA-256 和可选开发者公钥；在可丢弃虚拟机测试安装和更新。翻译修改不能顺带更换身份或信任策略。

## 两种发布方式

私钥可一直留在签名机器，无需上传 GitHub。先在开发虚拟机生成并检查目录，只将 `catalog.json` 送到签名机器，用现有认可密钥签名；将 JSON 和独立签名送回虚拟机验签，最后上传为正式 `catalog-N` GitHub Release。发布前核对全部历史 Release，N 必须高于历史最大序号；目标 commit 必须是已审核的目录仓库提交。不得传输整个 GPG 私钥目录。

也可使用仓库的 **Publish catalog** 工作流：

1. 创建 `catalog-release` environment，设置维护者审核和 main 分支限制。
2. 配置 `CATALOG_SIGNING_PRIVATE_KEY`（ASCII armored 私钥）；需要口令时配置 `CATALOG_SIGNING_PASSPHRASE`。不要写进仓库或日志。
3. 确认公钥与 `catalog-public.gpg`、`catalog-fingerprint.txt` 和客户端固定公钥一致。生成另一把密钥不会自动被现有客户端信任。
4. 在 main 手动运行工作流，填写递增整数 sequence。工作流生成目录、对原始字节签名、验签，然后发布 `catalog.json` 和 `catalog.json.sig`。
5. 在开发虚拟机刷新客户端，确认序号、有效期、应用显示与安装计划后再宣布可用。

默认有效期 30 天，即使没有条目变化也要在到期前发布更高序号。过期目录不能授权安装或更新。不得复用序号、重排已签名 JSON、修改已有目录 Release 或删除历史重置计数。修正需要新序号；发布成功不等于客户端验收通过。

## 第三方目录

复制仓库格式和工具，换成自己的公钥/指纹，把工作流 `--source-id nextkde` 改成唯一标识，与用户添加时填写的 ID 一致。使用自己的发布环境，不复用官方来源标识。稳定 GitHub Release 必须有固定附件名 `catalog.json` 和 `catalog.json.sig`。用户通过独立可信渠道核对指纹并明确接受，托管在 GitHub 本身不建立信任。

暂不支持根密钥自动轮换；第三方换根密钥需新来源 ID 并重新信任。官方密钥更换需要协调客户端发行。

## 开发虚拟机中的命令

```sh
python3 build_catalog.py --check
python3 -m unittest discover -s tests
python3 build_catalog.py --sequence 1
# 签名后，将公开文件送回虚拟机验签：
gpgv --keyring ./catalog-public.gpg dist/catalog.json.sig dist/catalog.json
```

示例 sequence 1 仅用于新目录，已有官方目录必须使用更高序号。签名机器不运行不受信的投稿程序。

schema 2 目录内嵌批准版本清单并固定仓库图标，见[版本审批](docs/PinnedReleases.zh-CN.md)。
