# 快速原型指南

## 原型类型

### 1. 纸上原型 (Paper Prototype)

- 最快
- 用于 UI/UX 验证
- 无需编码

### 2. 可点击原型 (Clickable Prototype)

- Figma, Sketch
- 用于交互验证
- 低代码

### 3. 功能原型 (Functional Prototype)

- 实际代码
- 核心功能可用
- 用于技术验证

## 快速原型技术栈

### Web 应用

| 需求 | 推荐 | 理由 |
|-----|------|------|
| 静态页面 | HTML + Tailwind | 快速样式 |
| 简单交互 | Vue/React + CDN | 无需构建 |
| 全栈 | Next.js / Nuxt | 一体化 |
| 后端 | FastAPI / Express | 简单快速 |

### CLI 工具

```python
# 使用 click 快速构建
import click

@click.command()
@click.argument('name')
@click.option('--count', default=1, help='Number of greetings.')
def hello(name, count):
    for _ in range(count):
        click.echo(f'Hello, {name}!')

if __name__ == '__main__':
    hello()
```

### API 服务

```python
# FastAPI 最小示例
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

## 原型清单

### 开始前
- [ ] 明确验证目标
- [ ] 定义核心功能
- [ ] 选择技术栈
- [ ] 设定时间盒

### 开发中
- [ ] 先实现核心流程
- [ ] 使用硬编码数据
- [ ] 跳过边缘情况
- [ ] 频繁运行测试

### 完成后
- [ ] 记录限制和假设
- [ ] 收集反馈
- [ ] 评估是否继续
- [ ] 规划下一步

## 常见捷径

### 数据存储

```python
# 原型阶段用 JSON 文件代替数据库
import json

def save_data(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data(filename='data.json'):
    try:
        with open(filename) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

### 认证

```python
# 原型阶段简单 API Key
def require_auth(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != 'prototype-key':
            return {"error": "Unauthorized"}, 401
        return func(*args, **kwargs)
    return wrapper
```

### 配置

```python
# 原型阶段硬编码配置
CONFIG = {
    "database_url": "sqlite:///prototype.db",
    "api_key": "demo-key",
    "debug": True,
}
```

## 从原型到产品

### 评估维度

1. **可行性**: 技术上能实现吗？
2. **可用性**: 用户能理解和使用吗？
3. **价值**: 解决了真正的问题吗？
4. **成本**: 完整实现需要多少资源？

### 演进策略

| 原型结果 | 下一步 |
|---------|--------|
| 验证成功 | 重构为生产代码 |
| 部分成功 | 调整方向，新原型 |
| 失败 | 放弃或重新思考 |

### 重构优先级

1. 安全问题
2. 数据持久化
3. 错误处理
4. 性能优化
5. 代码质量
