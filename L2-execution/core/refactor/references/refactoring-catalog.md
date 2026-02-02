# 重构手法目录

## 组合重构

### Extract Method（提取方法）

**问题**: 代码块太长或逻辑可复用

**重构前**:
```python
def print_owning(self):
    # print banner
    print("*" * 20)
    print("Customer Owes")
    print("*" * 20)

    # calculate outstanding
    outstanding = 0
    for order in self.orders:
        outstanding += order.amount

    # print details
    print(f"name: {self.name}")
    print(f"amount: {outstanding}")
```

**重构后**:
```python
def print_owning(self):
    self._print_banner()
    outstanding = self._calculate_outstanding()
    self._print_details(outstanding)

def _print_banner(self):
    print("*" * 20)
    print("Customer Owes")
    print("*" * 20)

def _calculate_outstanding(self):
    return sum(order.amount for order in self.orders)

def _print_details(self, outstanding):
    print(f"name: {self.name}")
    print(f"amount: {outstanding}")
```

### Inline Method（内联方法）

**问题**: 方法体与名字一样清晰

**重构前**:
```python
def get_rating(self):
    return 2 if self._more_than_five_late_deliveries() else 1

def _more_than_five_late_deliveries(self):
    return self.late_deliveries > 5
```

**重构后**:
```python
def get_rating(self):
    return 2 if self.late_deliveries > 5 else 1
```

## 简化条件

### Decompose Conditional（分解条件）

**重构前**:
```python
if date < SUMMER_START or date > SUMMER_END:
    charge = quantity * self.winter_rate + self.winter_service_charge
else:
    charge = quantity * self.summer_rate
```

**重构后**:
```python
if self._is_winter(date):
    charge = self._winter_charge(quantity)
else:
    charge = self._summer_charge(quantity)

def _is_winter(self, date):
    return date < SUMMER_START or date > SUMMER_END

def _winter_charge(self, quantity):
    return quantity * self.winter_rate + self.winter_service_charge

def _summer_charge(self, quantity):
    return quantity * self.summer_rate
```

### Replace Nested Conditional with Guard Clauses

**重构前**:
```python
def get_payment_amount(self):
    if self.is_dead:
        result = dead_amount()
    else:
        if self.is_separated:
            result = separated_amount()
        else:
            if self.is_retired:
                result = retired_amount()
            else:
                result = normal_amount()
    return result
```

**重构后**:
```python
def get_payment_amount(self):
    if self.is_dead:
        return dead_amount()
    if self.is_separated:
        return separated_amount()
    if self.is_retired:
        return retired_amount()
    return normal_amount()
```

## 消除重复

### Extract Superclass（提取超类）

当两个类有相似特性时。

### Pull Up Method（上移方法）

将子类中相同的方法移到父类。

### Form Template Method（形成模板方法）

相似算法用模板方法统一。

## 代码度量

### 圈复杂度 (Cyclomatic Complexity)

```
复杂度 = 分支数 + 1
```

| 复杂度 | 级别 |
|-------|------|
| 1-10 | 简单 |
| 11-20 | 中等 |
| 21-50 | 复杂 |
| > 50 | 不可维护 |

### 函数长度

- 建议: < 30 行
- 最大: < 50 行

### 参数数量

- 建议: ≤ 4
- 最大: ≤ 7

## 重构安全检查

1. 运行现有测试
2. 小步修改
3. 频繁提交
4. 使用 IDE 重构工具
