# 性能优化技术

## 算法优化

### 时间复杂度改进

| 原复杂度 | 优化后 | 方法 |
|---------|--------|------|
| O(n²) | O(n log n) | 使用排序+二分 |
| O(n²) | O(n) | 使用哈希表 |
| O(n) | O(1) | 预计算/缓存 |
| O(2^n) | O(n·2^n) | 动态规划 |

### 示例：查找优化

```python
# O(n²) - 双重循环
def find_pair_slow(arr, target):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] + arr[j] == target:
                return (i, j)
    return None

# O(n) - 哈希表
def find_pair_fast(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return (seen[complement], i)
        seen[num] = i
    return None
```

## 内存优化

### 生成器代替列表

```python
# 高内存
def get_all_items():
    return [process(i) for i in range(1000000)]

# 低内存
def get_all_items():
    for i in range(1000000):
        yield process(i)
```

### 使用 __slots__

```python
# 普通类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 使用 __slots__ 减少内存
class PointOptimized:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

## I/O 优化

### 批量操作

```python
# 慢：逐条插入
for item in items:
    db.insert(item)

# 快：批量插入
db.insert_many(items)
```

### 缓存

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n):
    # 耗时计算
    return result
```

### 异步 I/O

```python
import asyncio
import aiohttp

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

## 数据库优化

### 查询优化

```sql
-- 慢：SELECT *
SELECT * FROM users WHERE status = 'active';

-- 快：只选需要的列
SELECT id, name FROM users WHERE status = 'active';

-- 使用索引
CREATE INDEX idx_users_status ON users(status);
```

### 避免 N+1

```python
# N+1 问题
for user in users:
    posts = get_posts(user.id)  # N 次查询

# 预加载
users = get_users_with_posts()  # 1 次查询
```

## 性能分析工具

| 语言 | 工具 |
|-----|------|
| Python | cProfile, py-spy, memory_profiler |
| JavaScript | Chrome DevTools, Node --prof |
| Java | JProfiler, VisualVM |
| Go | pprof |

## 性能指标

| 指标 | 说明 | 目标 |
|-----|------|------|
| 响应时间 | 请求处理时间 | < 200ms (P95) |
| 吞吐量 | 单位时间处理请求数 | 根据需求 |
| CPU 使用率 | CPU 占用 | < 70% |
| 内存使用 | 内存占用 | 稳定无泄漏 |
| GC 时间 | 垃圾回收时间 | < 5% |
