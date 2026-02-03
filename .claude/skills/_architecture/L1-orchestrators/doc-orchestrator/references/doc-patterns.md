# 文档生成模式

## 文档类型矩阵

| 文档类型 | 目标读者 | 关键章节 | 参考 Skill |
|---------|---------|---------|-----------|
| README | 新用户 | 简介、安装、快速开始 | doc-gen |
| API Reference | 开发者 | 端点、参数、示例 | doc-gen, code-review |
| Architecture | 架构师 | 概览、组件、数据流 | arch-explore, doc-gen |
| User Guide | 终端用户 | 功能、步骤、FAQ | doc-gen |
| Contributing | 贡献者 | 环境、规范、流程 | doc-gen |
| Changelog | 所有人 | 版本、变更、迁移 | doc-gen |

## README 模板

```markdown
# 项目名称

一句话描述项目。

## 特性

- 特性 1
- 特性 2

## 快速开始

### 安装

```bash
pip install project-name
```

### 使用

```python
from project import main
main()
```

## 文档

详细文档请参考 [docs/](./docs/)

## 贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 许可证

MIT License
```

## API 文档模板

```markdown
# API Reference

## 认证

描述认证方式...

## 端点

### GET /api/resource

获取资源列表。

**参数**

| 名称 | 类型 | 必填 | 描述 |
|-----|------|-----|------|
| page | int | 否 | 页码 |

**响应**

```json
{
  "data": [...],
  "total": 100
}
```

**示例**

```bash
curl -X GET https://api.example.com/resource
```
```

## 架构文档模板

```markdown
# 系统架构

## 概述

系统整体架构描述...

## 组件

### 组件 A

职责、接口、依赖...

### 组件 B

职责、接口、依赖...

## 数据流

```mermaid
graph LR
    A[客户端] --> B[API 网关]
    B --> C[服务层]
    C --> D[数据库]
```

## 部署架构

描述部署拓扑...

## 技术选型

| 领域 | 技术 | 理由 |
|-----|------|-----|
| 语言 | Python | ... |
| 框架 | FastAPI | ... |
```

## 分解策略

### 大型文档分解

当文档过大时，按章节分解：

```
doc-gen (章节1)
    ∥
doc-gen (章节2)  → merge
    ∥
doc-gen (章节3)
```

### 多语言文档

```
doc-gen (英文)
    ↓
doc-gen (中文翻译)
    ↓
review (一致性检查)
```
