# 文档模板

## README 模板

```markdown
# 项目名称

简短的项目描述（一行）。

## 特性

- 特性 1: 描述
- 特性 2: 描述
- 特性 3: 描述

## 安装

### 前置要求

- 要求 1
- 要求 2

### 安装步骤

```bash
# 安装命令
pip install project-name
```

## 快速开始

```python
# 快速开始示例代码
from project import main

result = main()
print(result)
```

## 使用方法

### 基本用法

描述基本用法...

```python
# 示例代码
```

### 高级用法

描述高级用法...

## 配置

| 配置项 | 说明 | 默认值 |
|-------|------|-------|
| CONFIG_1 | 描述 | default |

## API 参考

详见 [API 文档](./docs/api.md)

## 贡献

欢迎贡献！请阅读 [贡献指南](./CONTRIBUTING.md)

## 许可证

[MIT](./LICENSE)
```

## API 文档模板

```markdown
# API 参考

## 概述

API 简介...

## 认证

描述认证方式...

## 端点

### GET /api/resource

获取资源。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| id | integer | 是 | 资源 ID |

**响应**

```json
{
  "id": 1,
  "name": "example",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**状态码**

| 状态码 | 说明 |
|-------|------|
| 200 | 成功 |
| 404 | 未找到 |

**示例**

```bash
curl -X GET "https://api.example.com/resource?id=1"
```
```

## Docstring 模板 (Google Style)

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """简短描述。

    更详细的描述（可选）。可以跨多行。

    Args:
        param1: 参数1的描述。
        param2: 参数2的描述。

    Returns:
        返回值的描述。

    Raises:
        ExceptionType: 异常描述。

    Examples:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output
    """
    pass
```

## 架构文档模板

```markdown
# 系统架构文档

## 1. 概述

### 1.1 目的

系统的目的和范围...

### 1.2 架构目标

- 目标 1
- 目标 2

## 2. 系统上下文

描述系统与外部系统的关系...

## 3. 组件架构

### 3.1 组件 A

**职责**: 描述...

**接口**: 描述...

**依赖**: 描述...

### 3.2 组件 B

...

## 4. 数据架构

### 4.1 数据模型

描述主要数据实体...

### 4.2 数据流

描述数据如何流动...

## 5. 部署架构

描述部署拓扑...

## 6. 安全架构

描述安全措施...

## 7. 技术选型

| 领域 | 技术 | 理由 |
|-----|------|-----|
| 语言 | Python | ... |
| 数据库 | PostgreSQL | ... |

## 8. 附录

### 8.1 术语表

| 术语 | 定义 |
|-----|------|
| 术语1 | 定义 |
```
