# EC v1.0 — Manufacturing Intelligence Reference System
# 一键部署与验收指南

> 适用包：`EC-v1.0-Manufacturing-Intelligence-Reference-System.zip`  
> 定位：**可执行 Manufacturing Intelligence Reference System**，不是 Production Certified 生产系统。  
> 核心原则：**EC thinks and learns. EVO executes. Eidos interacts.**

---

## 1. 最推荐的第一次部署方式

第一次运行 **不需要 Docker、不需要 PostgreSQL、不需要向量数据库，也不需要任何 LLM API Key**。

你只需要：

- Windows 10/11、macOS 或 Linux
- Python **3.12+**
- 解压工具

这条路径会验证：

1. EC 运行环境是否正常；
2. 25 个参考测试是否通过；
3. Manufacturing Intelligence Demo 是否可以运行；
4. EC 是否能够输出一个面向 Eidos 的制造业 Decision Workspace / Experience Proposal。

---

# 2. Windows 一键体验

## 2.1 解压

解压：

```text
EC-v1.0-Manufacturing-Intelligence-Reference-System.zip
```

进入目录：

```text
EC-v1.0-Manufacturing-Intelligence-Reference-System
```

## 2.2 检查 Python

打开 PowerShell：

```powershell
python --version
```

应为：

```text
Python 3.12+
```

如果电脑同时安装多个 Python，可以试：

```powershell
py -3.12 --version
```

---

## 2.3 最短启动命令

在项目根目录打开 PowerShell，执行：

```powershell
$env:PYTHONPATH="src"
python -m ec doctor
python -m unittest discover -s tests -v
python -m ec demo-manufacturing
```

如果全部正常，你应该看到：

```text
status: ok
```

以及：

```text
Ran 25 tests
OK
```

最后会输出 Manufacturing Intelligence Demo，其中包括：

- 制造业订单交付风险；
- `$280,000` revenue at risk；
- Promise Date；
- Evidence；
- alternate supplier 等决策选项；
- `decision-panel`
- `evidence-stack`
- `impact-preview`
- `timeline`
- Experience Proposal。

这代表 **EC v1.0 Reference Runtime 已经成功启动**。

---

# 3. Windows 真正“一键”脚本

如果你希望以后双击运行，可以在项目根目录新建：

```text
START-EC-V1-WINDOWS.bat
```

内容：

```bat
@echo off
title EC v1.0 Manufacturing Intelligence Reference System

echo ==========================================
echo EC v1.0 Manufacturing Intelligence
echo ==========================================

set PYTHONPATH=src

echo.
echo [1/3] Environment check...
python -m ec doctor
if errorlevel 1 goto error

echo.
echo [2/3] Running reference tests...
python -m unittest discover -s tests -v
if errorlevel 1 goto error

echo.
echo [3/3] Running manufacturing demo...
python -m ec demo-manufacturing
if errorlevel 1 goto error

echo.
echo ==========================================
echo EC v1.0 STARTUP / VALIDATION: PASS
echo ==========================================
pause
exit /b 0

:error
echo.
echo ==========================================
echo EC v1.0 STARTUP / VALIDATION: FAILED
echo ==========================================
pause
exit /b 1
```

以后直接双击：

```text
START-EC-V1-WINDOWS.bat
```

即可完成：

```text
Doctor
  ↓
25 Tests
  ↓
Manufacturing Demo
```

---

# 4. macOS / Linux 一键体验

进入解压目录：

```bash
cd EC-v1.0-Manufacturing-Intelligence-Reference-System
```

执行：

```bash
export PYTHONPATH=src

python3 -m ec doctor
python3 -m unittest discover -s tests -v
python3 -m ec demo-manufacturing
```

也可以创建：

```text
start-ec-v1.sh
```

内容：

```bash
#!/usr/bin/env bash
set -e

export PYTHONPATH=src

echo "[1/3] EC doctor"
python3 -m ec doctor

echo "[2/3] Reference tests"
python3 -m unittest discover -s tests -v

echo "[3/3] Manufacturing demo"
python3 -m ec demo-manufacturing

echo
echo "EC v1.0 STARTUP / VALIDATION: PASS"
```

然后：

```bash
chmod +x start-ec-v1.sh
./start-ec-v1.sh
```

---

# 5. 更标准的安装方式

上面的 `PYTHONPATH=src` 模式最适合第一次验证。

如果准备持续开发 EC，推荐使用虚拟环境并安装为 editable package。

## Windows PowerShell

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e .

ec doctor
python -m unittest discover -s tests -v
ec demo-manufacturing
```

安装完成后就不再需要：

```text
PYTHONPATH=src
```

---

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e .

ec doctor
python -m unittest discover -s tests -v
ec demo-manufacturing
```

---

# 6. Demo 到底验证了什么

当前 v1.0 Demo 的重点不是 UI，而是验证 EC 的“大脑链路”。

参考流程：

```text
Persistent Knowledge
        ↓
Evidence / Provenance
        ↓
Retrieval
        ↓
Context Compiler
        ↓
Reasoning Boundary
        ↓
Manufacturing Decision
        ↓
Experience Proposal
        ↓
Eidos
```

默认 Manufacturing Demo 中，一个生产订单出现关键物料交付风险。

EC 会构造类似：

```text
Sales Order
SO-20260913-0182

Promised delivery
2026-09-18

Revenue at risk
USD 280,000
```

然后生成：

```text
Decision Workspace
├── Exception Queue
├── Decision Panel
├── Evidence Stack
├── Impact Preview
└── Timeline
```

这是以后接入 Eidos 的输入。

---

# 7. 当前版本不需要真实 LLM 也能运行

这是有意设计。

EC 的核心原则是：

```text
EC intelligence belongs to EC,
not to a specific model.
```

因此 Reference Runtime 可以在没有 OpenAI、Claude、Gemini 或本地模型 API 的情况下验证：

- Knowledge Model
- Context Compilation
- Learning Strategy
- Governance
- Manufacturing Reasoning Structure
- Experience Proposal
- EVO / Eidos Boundary

真实 LLM 属于可替换 Adapter。

以后可以接：

```text
EC
 ↓
Model Gateway
 ├── OpenAI
 ├── Anthropic
 ├── Gemini
 ├── Local Model
 └── Future Model
```

而不是把某个模型写死到 EC 核心。

---

# 8. Docker 是第二阶段，不是第一次启动必需条件

EC v1.0 包中已经包含：

```text
deploy/docker-compose.yml
```

其目的是搭建开发/集成数据平面，包括：

```text
PostgreSQL 18
Qdrant
OpenSearch
ClickHouse
```

但这些目前是 **Integration Convenience**，并不意味着 Production Certified。

---

## 8.1 只启动 PostgreSQL

要求：

- Docker Desktop / Docker Engine
- Docker Compose

运行：

```bash
docker compose -f deploy/docker-compose.yml up -d postgres
```

检查：

```bash
docker compose -f deploy/docker-compose.yml ps
```

---

## 8.2 启动 Search Stack

```bash
docker compose -f deploy/docker-compose.yml --profile search up -d
```

包含：

```text
PostgreSQL
Qdrant
OpenSearch
```

---

## 8.3 启动 Analytics

```bash
docker compose -f deploy/docker-compose.yml --profile analytics up -d
```

包含 ClickHouse。

---

## 8.4 全部停止

```bash
docker compose -f deploy/docker-compose.yml down
```

删除开发数据卷：

```bash
docker compose -f deploy/docker-compose.yml down -v
```

注意：

> `down -v` 会删除本地开发数据，只用于明确需要重置环境时。

---

# 9. PostgreSQL 18 注意事项

当前 EC v1.0 包中的 Docker Compose 属于参考集成配置。

对于长期运行和未来升级，我们建议后续像 EVO 一样统一采用 PostgreSQL 18+ 的版本化数据目录策略，并单独处理：

- 升级；
- pg_upgrade；
- backup / restore；
- HA；
- failover；
- WAL；
- PITR；
- volume layout。

因此：

> 第一次体验 EC v1.0 时，不建议把 Docker PostgreSQL 当成“正式数据库部署”。

Reference Demo 使用 Python Reference Runtime 即可。

---

# 10. 推荐的目录理解

解压后重点目录：

```text
EC-v1.0-Manufacturing-Intelligence-Reference-System/
│
├── src/ec/
│   └── EC 核心代码
│
├── industry-packs/
│   └── Manufacturing Intelligence 数据资产
│
├── learning/
│   └── Learning Strategy / 方法
│
├── schemas/
│   └── 版本化 Contract / Schema
│
├── examples/
│   └── EVO / Eidos 边界示例
│
├── deploy/
│   └── 开发集成基础设施
│
├── tests/
│   └── Reference Tests
│
├── docs/
│   └── 架构、运维、扩展路线
│
├── CONSTITUTION.md
├── ARCHITECTURE.md
├── pyproject.toml
└── README.md
```

---

# 11. 最重要的阅读顺序

第一次不必把所有文档读完。

建议：

```text
1. README.md
2. docs/00-START-HERE.md
3. CONSTITUTION.md
4. ARCHITECTURE.md
5. docs/10-V1.0-MANUFACTURING-REFERENCE-SYSTEM.md
6. docs/30-EVO-INTEGRATION.md
7. docs/31-EIDOS-INTEGRATION.md
8. docs/11-PRODUCTION-CERTIFICATION.md
```

之后再看：

```text
docs/10-DATA-AND-SCALE.md
docs/12-LEARNING-ARCHITECTURE.md
docs/13-CONTEXT-COMPILER.md
docs/14-PROVENANCE-AND-LINEAGE.md
docs/15-INDUSTRY-PACKS.md
docs/20-HARDWARE-AND-CAPACITY.md
docs/40-LLM-REPLACEMENT.md
docs/50-ACTIVE-LEARNING-AND-RESEARCH.md
docs/90-TWENTY-YEAR-ROADMAP.md
```

---

# 12. 如何判断“部署成功”

最低验收标准：

## Doctor

```text
status = ok
```

## Tests

```text
Ran 25 tests
OK
```

## Manufacturing Demo

必须产生：

```text
context
experienceProposal
decision-panel
evidence-stack
impact-preview
timeline
```

并且存在制造业交付风险场景。

满足这三个条件，即代表：

> **EC v1.0 Manufacturing Intelligence Reference System 已成功部署并通过 Reference Validation。**

---

# 13. 我们当前验证过的状态

本部署说明基于实际 EC v1.0 ZIP 验证。

已验证：

```text
EC doctor: PASS
Manufacturing demo: PASS
Reference tests: 25 / 25 PASS
```

测试命令必须满足以下之一：

### 方法 A

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

### 方法 B

先安装：

```bash
pip install -e .
```

再运行：

```bash
python -m unittest discover -s tests -v
```

原因是源码采用：

```text
src/ec/
```

布局。

如果没有安装 package，也没有设置 `PYTHONPATH=src`，Python 无法定位 `ec` module。

---

# 14. 当前 v1.0 仍然不是 Production Certified

必须明确：

```text
Reference System
≠
Production Certified System
```

v1.0 已经证明：

```text
Architecture
Knowledge Model
Learning Model
Context
Manufacturing Reference
Governance
Integration Boundaries
Executable Reference Lifecycle
```

但尚未证明：

```text
Real PostgreSQL HA
Real production backup / restore
Production-grade event ingestion
Large-scale retrieval
Multi-region
Load / stress SLO
Disaster Recovery
Real EVO contract certification
Real Eidos contract certification
Production tenant isolation certification
Production model-provider security/data residency
```

所以当前正确说法是：

> **EC v1.0 Manufacturing Intelligence Reference System**

而不是：

> Production-ready EC v1.0。

---

# 15. EC × EVO × Eidos 下一阶段部署形态

我们现在正在进入的 Architecture Convergence 应最终让部署变成：

```text
Enterprise Intelligence Pack
             │
             ▼
             EC
             │
      compile / publish
        ┌────┴────┐
        ▼         ▼
       EVO       Eidos
   Operational   Experience
      Pack          Pack
```

之后理想的一键启动会进一步变成：

```text
install
   ↓
start
   ↓
publish enterprise pack
   ↓
EVO ready
   ↓
Eidos ready
   ↓
EC intelligence ready
   ↓
Manufacturing Demo ready
```

最终用户不应该需要了解三个仓库内部如何工作。

---

# 16. 现在最简单的操作

如果你只是想确认 EC v1.0：

### Windows PowerShell

```powershell
$env:PYTHONPATH="src"
python -m ec doctor
python -m unittest discover -s tests -v
python -m ec demo-manufacturing
```

### macOS / Linux

```bash
export PYTHONPATH=src
python3 -m ec doctor
python3 -m unittest discover -s tests -v
python3 -m ec demo-manufacturing
```

看到：

```text
status: ok
Ran 25 tests
OK
```

以及 Manufacturing Experience Proposal，就完成了第一阶段验收。

---

## 结论

对于 EC v1.0，当前推荐部署原则是：

> **第一次体验：Python-only Reference Runtime。**  
> **持续开发：venv + `pip install -e .`。**  
> **集成验证：Docker PostgreSQL / Search / Analytics。**  
> **生产部署：等待经过 EVO/Eidos 真实契约、HA、DR、Security、Load 和 Data Plane Certification 的 Production Profile。**

这样既能做到低门槛，又不会把 Reference System 错误包装成生产系统。
