# 调试策略

## 诊断方法

### 1. 二分法定位

将问题代码范围不断缩小。

```
代码范围: 1-100 行
├── 检查 1-50 行: 问题存在
│   ├── 检查 1-25 行: 问题不存在
│   └── 检查 26-50 行: 问题存在
│       └── 定位到 35-40 行
```

### 2. 打印调试

在关键点添加打印语句。

```python
def calculate(data):
    print(f"[DEBUG] Input: {data}")

    result = process(data)
    print(f"[DEBUG] After process: {result}")

    final = transform(result)
    print(f"[DEBUG] Final: {final}")

    return final
```

### 3. 断点调试

使用调试器设置断点。

```python
def buggy_function():
    import pdb; pdb.set_trace()  # Python 调试器
    # 或
    breakpoint()  # Python 3.7+

    # 问题代码
    ...
```

### 4. 日志分析

分析日志寻找异常模式。

```
[2024-01-01 10:00:00] INFO: Request received
[2024-01-01 10:00:01] DEBUG: Processing data...
[2024-01-01 10:00:02] ERROR: NullPointerException at line 42  <-- 问题
[2024-01-01 10:00:02] INFO: Request failed
```

## 常见 Bug 模式

### Off-by-one Error（差一错误）

```python
# 错误
for i in range(len(items) + 1):  # 多了一个
    print(items[i])

# 正确
for i in range(len(items)):
    print(items[i])
```

### Null Reference（空引用）

```python
# 错误
def get_name(user):
    return user.name  # user 可能是 None

# 正确
def get_name(user):
    return user.name if user else None
```

### Race Condition（竞态条件）

```python
# 错误
def increment():
    global counter
    counter += 1  # 非原子操作

# 正确
def increment():
    global counter
    with lock:
        counter += 1
```

### Resource Leak（资源泄漏）

```python
# 错误
def read_file(path):
    f = open(path)
    content = f.read()
    return content  # 忘记关闭

# 正确
def read_file(path):
    with open(path) as f:
        return f.read()
```

## 诊断检查清单

1. [ ] 错误信息是否明确？
2. [ ] 能否稳定复现？
3. [ ] 最近有什么变更？
4. [ ] 输入数据是否有效？
5. [ ] 边界条件是否处理？
6. [ ] 依赖是否正常？
7. [ ] 环境是否一致？

## 修复验证

1. **单元测试**: 针对 bug 写测试
2. **回归测试**: 确保不破坏其他功能
3. **代码审查**: 同行审查修复
4. **监控**: 部署后监控相关指标

## 根因分析模板

```markdown
## Bug 报告

**问题描述**:
简述问题现象...

**复现步骤**:
1. 步骤 1
2. 步骤 2
3. 观察到错误

**期望行为**:
应该发生什么...

**实际行为**:
实际发生了什么...

**根因分析**:
问题的根本原因是...

**修复方案**:
修复方法是...

**预防措施**:
为防止类似问题...
```
