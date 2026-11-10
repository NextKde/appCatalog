# 批准版本与图标

[English](PinnedReleases.md) · [Português (Brasil)](PinnedReleases.pt-BR.md)

正常模式每个来源只获取一份签名目录，与本地安装版本比较，不扫描各应用仓库。开发者发布新版 Release 后，还需提交目录 PR 并发布新签名目录，新版才对正常客户端上架。

## 投稿文件

同一个 PR 提交 `apps/<appId>.json`、`icons/<appId>.png`，以及从 Release 下载的原始清单 `releases/<appId>.flatpak-release.json`。配置了 `publisher` 时还需提交对应的 `.json.sig` 签名。不要重新格式化已签名清单；安装包仍放在 GitHub Release。

条目增加：

```json
"icon": "icons/org.example.Notes.png",
"release": {
  "version": "1.2.0",
  "tag": "v1.2.0",
  "manifestFile": "releases/org.example.Notes.flatpak-release.json"
}
```

配置开发者公钥时，在 `release` 中增加 `signatureFile`。暂时没有批准的兼容安装包时明确写 `"release": null`，不虚构版本、不自动回退查询上游 latest。清单包含各架构安装包文件名、SHA-256、大小、commit、权限元数据和运行库依赖；应用 ID、版本必须与条目一致。审核时核对真实发布标签和附件。

图标使用 PNG，最大 1024 × 1024、512 KiB，建议 256 × 256；在 `icons/` 保留来源和许可证。发布工具自动计算摘要，并生成固定到完整 Git commit 的 `raw.githubusercontent.com/<目录仓库>/<commit>/icons/<appId>.png` 地址。客户端检查来源、大小、尺寸和摘要后缓存；缺失或错误显示默认图标。图标下载有时间预算，后续刷新可重试。

## 发布与兼容

在虚拟机/CI 执行 `python3 build_catalog.py --check`，再执行 `python3 build_catalog.py --sequence N --repository OWNER/REPO --revision FULL_COMMIT`。commit 必须包含审核后的图标，不能对未提交或与该 commit 不同的图标字节签发目录。工作流自动使用检出的 commit；第三方源同时修改仓库名和来源 ID。

生成的 **schema 2 目录**以 Base64 内嵌原始清单和可选开发者签名，同时保留可读的 `release.version`、`release.tag`。安装包摘要因此受到目录签名保护；即使不配置开发者签名，上游同时替换包和清单也不能改变已经批准的目录摘要。安全仍依赖目录维护者审核和密钥，不代表应用行为一定安全。

客户端需要支持 schema 2。旧客户端拒绝新格式，在有效期内保留旧的已验证快照；迁移来源时应更新 Settings。新客户端保留 schema 1 的防回滚历史，但不会为正常安装扫描旧条目的上游仓库。已安装应用仍可管理。测试模式仍允许直接发现指定/Latest GitHub Release，用于上架前调试。
