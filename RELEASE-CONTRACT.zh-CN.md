# GitHub Release / Flatpak 发行协议

[English / 完整 JSON 示例](RELEASE-CONTRACT.md) · [Qt runtime](docs/QtRuntime.zh-CN.md)

客户端访问登记仓库的 `https://api.github.com/repos/OWNER/REPOSITORY/releases/latest`，只接受正式、非预发行的 `vX.Y.Z`。每个必需附件名称必须唯一，下载限于登记 GitHub 仓库及其 Release CDN 跳转。

目录 `manifest` 指定发行清单附件名。清单 `schemaVersion` 为 2，appId 与目录一致，version 与 tag 去掉 v 一致，revision 是 40 位源码 commit。bundles 按架构索引，每项包含：

| 字段 | 含义 |
| --- | --- |
| asset | 当前 Release 中的 `.flatpak` 附件名 |
| ref / commit | `app/<appId>/<arch>/stable` 与实际 64 位 OSTree commit |
| sha256 / size | 最终 bundle 原始字节的 SHA-256 和字节数 |
| metadata | 包内原始应用元数据的 Base64，保留末尾换行 |
| metadataSha256 | 解码后原始 metadata 的 SHA-256 |
| installedSize | Flatpak bundle 声明的安装大小，不是去重后的磁盘增量 |
| runtime | 必需 runtime 的完整 ref |
| requiredExtensions | 必需扩展 ref 对象数组，没有时为空数组 |

实际值必须从最终包提取，不能照抄示例占位符，也不能用源码包 hash。包不能嵌入在线 origin 或 runtime-repo URL。客户端独立核对依赖计划与可信运行库来源。

目录配置 publisher 时，另附对清单原始字节签名的 `<manifest>.sig`，包内 OSTree commit 也必须由该开发者密钥签名。没有 publisher 时可不签，但仍强制校验 SHA-256、身份、GitHub 路由、元数据、版本和安装来源。任何格式都必须通过 GitHub Releases；当前只实现 Flatpak。
