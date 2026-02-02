# 文档质量门禁

## 门禁定义

### doc-gen 门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 格式正确 | BLOCKER | Markdown/RST 解析无错误 |
| 标题结构 | CRITICAL | 检查是否有层级标题 |
| 内容非空 | CRITICAL | 检查各章节有内容 |
| 无占位符 | MAJOR | 搜索 TODO, TBD, XXX |
| 代码块完整 | MAJOR | 检查代码块闭合 |
| 链接格式 | MINOR | 检查链接语法 |

**通过标准**: 无 BLOCKER，CRITICAL = 0

### 审查门禁

| 检查项 | 严重级别 | 检查方法 |
|-------|---------|---------|
| 与代码一致 | CRITICAL | 对比函数签名 |
| 术语一致 | MAJOR | 检查术语使用 |
| 示例可运行 | MAJOR | 提取代码示例验证 |
| 拼写正确 | MINOR | 拼写检查 |

## 评分维度

### 完整性 (Completeness)

- 所有必需章节存在
- 所有公共 API 有文档
- 示例覆盖主要场景

### 准确性 (Accuracy)

- 与代码行为一致
- 参数描述正确
- 返回值描述正确

### 可读性 (Readability)

- 句子简洁
- 段落长度适中
- 逻辑清晰

### 格式规范 (Format)

- 符合项目风格
- 代码高亮正确
- 表格对齐

## 评分公式

```
doc_quality = 0.35 * completeness + 0.30 * accuracy + 0.20 * readability + 0.15 * format
```

## 自动检查工具

| 工具 | 检查内容 |
|-----|---------|
| markdownlint | Markdown 格式 |
| vale | 写作风格 |
| link-checker | 链接有效性 |
| code-runner | 示例代码 |
