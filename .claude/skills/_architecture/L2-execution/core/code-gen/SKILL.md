---
name: code-gen
description: >
  代码生成 Skill。根据需求描述生成高质量代码。当需要：(1) 实现新功能，(2) 创建函数/类/模块，
  (3) 根据 API 规范生成实现，(4) 从原型转为生产代码时触发。支持多种语言和框架，
  遵循项目代码风格和最佳实践。作为核心 Skill，具有严格契约。
---

# Code Gen — 代码生成

## 触发条件

- 需求描述中包含"实现"、"创建"、"生成代码"等关键词
- 由 code-orchestrator 或 multi-agent-orchestrator 调度
- 复杂度 S/M 级的代码编写任务

## 输入契约 (Strict)

```json
{
  "type": "object",
  "required": ["requirement", "language"],
  "properties": {
    "requirement": {
      "type": "string",
      "description": "需求描述，清晰说明要实现的功能"
    },
    "language": {
      "type": "string",
      "enum": ["python", "javascript", "typescript", "java", "go", "rust"],
      "description": "目标编程语言"
    },
    "framework": {
      "type": "string",
      "description": "使用的框架（如 fastapi, react, spring）"
    },
    "context": {
      "type": "object",
      "description": "上下文信息",
      "properties": {
        "existing_code": { "type": "string" },
        "api_spec": { "type": "object" },
        "style_guide": { "type": "string" }
      }
    },
    "output_path": {
      "type": "string",
      "description": "输出文件路径"
    }
  }
}
```

## 输出契约 (Strict)

```json
{
  "type": "object",
  "required": ["code", "files"],
  "properties": {
    "code": {
      "type": "string",
      "description": "生成的代码内容"
    },
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": { "type": "string" },
          "content": { "type": "string" },
          "language": { "type": "string" }
        }
      }
    },
    "imports": {
      "type": "array",
      "items": { "type": "string" },
      "description": "需要的导入/依赖"
    },
    "functions": {
      "type": "array",
      "description": "生成的函数签名列表"
    },
    "classes": {
      "type": "array",
      "description": "生成的类定义列表"
    },
    "quality_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    }
  }
}
```

## 执行流程

1. **解析需求**
   - 识别功能点
   - 确定输入/输出类型
   - 提取约束条件

2. **设计结构**
   - 确定函数/类组织
   - 设计接口签名
   - 规划模块划分

3. **生成代码**
   - 编写核心逻辑
   - 添加类型注解
   - 添加文档注释
   - 处理边界条件

4. **后处理**
   - 格式化代码
   - 检查语法正确性
   - 提取元数据（imports, functions, classes）

## 质量标准

参考 `references/best-practices.md`：

| 维度 | 标准 |
|-----|------|
| 正确性 | 实现需求描述的功能 |
| 可读性 | 命名清晰、结构合理 |
| 健壮性 | 处理边界条件和异常 |
| 可维护性 | 模块化、低耦合 |
| 类型安全 | 完整的类型注解 |

## 语言特定规则

### Python
- 使用 type hints
- 遵循 PEP 8
- 使用 docstring (Google style)
- 优先使用标准库

### JavaScript/TypeScript
- 使用 ES6+ 语法
- TypeScript 优先
- 使用 async/await
- 遵循 ESLint 规则

### Java
- 使用 Java 11+ 特性
- 遵循 Google Java Style
- 使用 Optional 处理 null

### Go
- 遵循 Go 惯例
- 优先返回 error
- 使用 context.Context

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| api-design | 接收 API 规范作为输入 |
| db-schema | 接收数据模型作为输入 |
| test-gen | 为生成的代码创建测试 |
| code-review | 审查生成的代码 |
| doc-gen | 为代码生成文档 |

## 脚本

- `scripts/generate.py` - 代码生成主脚本
- `scripts/validate.py` - 代码验证脚本
