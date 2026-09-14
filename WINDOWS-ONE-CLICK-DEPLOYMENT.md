# EC v1.0.1 Windows 一键部署

这是 **EC v1.0 Manufacturing Intelligence Reference System** 的 Windows 兼容性修复版。

## 最简单方法

### 要求
- Windows 10/11 x64
- Python **3.12 或 3.13**
- 第一次安装 package 时需要本机 Python/pip 正常工作
- Reference Demo 不需要 Docker、PostgreSQL 或 LLM API Key

### 启动
解压 ZIP 后，直接双击：

```text
START-EC-V1.0.1-WINDOWS.bat
```

脚本会自动：

```text
检测 Python 3.12 / 3.13
→ 创建 .venv（如果不存在）
→ pip install -e .
→ EC doctor
→ 完整测试
→ Manufacturing Intelligence Demo
```

看到：

```text
EC v1.0.1 WINDOWS VALIDATION: PASS
```

即完成 Reference System 验收。

## `.venv` 不要提交 GitHub

`.venv/` 是本机 Python 虚拟环境，不属于源代码。本包 `.gitignore` 已包含：

```gitignore
.venv/
```

因此不要手工把其中几百/几千个文件加入 Git。

## 本版修复内容

v1.0 在 Windows + Python 3.14 测试中暴露了 SQLite `ec.db` 文件句柄未在临时目录清理前显式释放的问题，表现为：

```text
PermissionError: [WinError 32]
```

v1.0.1：
- 为 `SqliteKnowledgeRepository` 增加显式 `close()`
- 增加 context-manager 生命周期：`with SqliteKnowledgeRepository(...) as repo`
- 临时 SQLite 测试在目录清理前确定性关闭数据库
- 增加数据库文件可立即删除的 regression test
- 增加 Windows 一键启动脚本
- 明确 v1.0.1 Windows 验收矩阵为 Python 3.12 / 3.13

Python 3.14 不是本版的 Windows certified profile。不是说 EC 永远不支持 3.14，而是当前不把未经 Windows 实机回归验证的版本标记为已认证。

## 版本定位

```text
EC v1.0.1
Manufacturing Intelligence Reference System
Windows Compatibility Fix
```

仍然是 Reference System，不是 Production Certified。
