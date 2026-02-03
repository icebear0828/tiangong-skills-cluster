# 代码生成最佳实践

## 通用原则

### 1. SOLID 原则

| 原则 | 应用 |
|-----|------|
| 单一职责 | 每个函数/类只做一件事 |
| 开闭原则 | 对扩展开放，对修改关闭 |
| 里氏替换 | 子类可替换父类 |
| 接口隔离 | 小接口优于大接口 |
| 依赖倒置 | 依赖抽象而非具体 |

### 2. 命名规范

| 类型 | Python | JavaScript | Java | Go |
|-----|--------|------------|------|-----|
| 类 | PascalCase | PascalCase | PascalCase | PascalCase |
| 函数 | snake_case | camelCase | camelCase | PascalCase (exported) |
| 变量 | snake_case | camelCase | camelCase | camelCase |
| 常量 | UPPER_CASE | UPPER_CASE | UPPER_CASE | PascalCase |

### 3. 注释规范

**何时注释**:
- 复杂算法的解释
- 非显而易见的设计决策
- 公共 API 的文档

**何时不注释**:
- 代码本身已经清晰
- 重复代码所做的事情

### 4. 错误处理

```python
# Good: 具体的异常类型
try:
    result = parse_config(path)
except FileNotFoundError:
    logger.error(f"Config file not found: {path}")
    raise ConfigurationError(f"Missing config: {path}")
except json.JSONDecodeError as e:
    logger.error(f"Invalid JSON in config: {e}")
    raise ConfigurationError(f"Invalid config format")

# Bad: 捕获所有异常
try:
    result = parse_config(path)
except Exception:
    pass  # 忽略所有错误
```

## 语言特定最佳实践

### Python

```python
# 1. 使用类型注解
def calculate_total(items: list[Item], tax_rate: float = 0.1) -> Decimal:
    """计算含税总价"""
    subtotal = sum(item.price for item in items)
    return Decimal(str(subtotal * (1 + tax_rate)))

# 2. 使用 dataclass
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True

# 3. 使用 context manager
with open(path, 'r') as f:
    content = f.read()

# 4. 使用 pathlib
from pathlib import Path
config_path = Path(__file__).parent / 'config.json'
```

### JavaScript/TypeScript

```typescript
// 1. 使用 TypeScript 类型
interface User {
  id: number;
  name: string;
  email: string;
}

// 2. 使用 async/await
async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`);
  }
  return response.json();
}

// 3. 使用解构和默认值
function createUser({ name, email, role = 'user' }: CreateUserInput): User {
  return { id: generateId(), name, email, role };
}

// 4. 使用 nullish coalescing
const displayName = user.nickname ?? user.name ?? 'Anonymous';
```

### Java

```java
// 1. 使用 Optional
public Optional<User> findUserById(Long id) {
    return userRepository.findById(id);
}

// 2. 使用 Stream API
List<String> activeUserNames = users.stream()
    .filter(User::isActive)
    .map(User::getName)
    .collect(Collectors.toList());

// 3. 使用 try-with-resources
try (var reader = new BufferedReader(new FileReader(path))) {
    return reader.lines().collect(Collectors.joining("\n"));
}

// 4. 使用 record (Java 14+)
public record UserDTO(Long id, String name, String email) {}
```

### Go

```go
// 1. 错误处理
func ReadConfig(path string) (*Config, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("read config: %w", err)
    }

    var config Config
    if err := json.Unmarshal(data, &config); err != nil {
        return nil, fmt.Errorf("parse config: %w", err)
    }

    return &config, nil
}

// 2. 使用 context
func FetchUser(ctx context.Context, id int) (*User, error) {
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }
    // ...
}

// 3. 接口定义
type UserRepository interface {
    FindByID(ctx context.Context, id int) (*User, error)
    Save(ctx context.Context, user *User) error
}
```

## 常见反模式

| 反模式 | 问题 | 改进 |
|-------|------|------|
| God Class | 类太大，职责太多 | 拆分为多个小类 |
| Magic Number | 硬编码数字 | 使用命名常量 |
| Copy-Paste | 重复代码 | 提取为函数 |
| Deep Nesting | 嵌套太深 | 提前返回、提取函数 |
| Long Parameter List | 参数太多 | 使用对象/配置类 |
