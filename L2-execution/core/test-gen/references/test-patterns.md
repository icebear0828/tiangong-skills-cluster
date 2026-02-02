# 测试模式

## 测试结构

### Arrange-Act-Assert (AAA)

```python
def test_example():
    # Arrange - 准备
    user = User(name="test", email="test@example.com")

    # Act - 执行
    result = user.validate()

    # Assert - 断言
    assert result is True
```

### Given-When-Then (BDD)

```python
def test_user_login():
    # Given - 前置条件
    user = create_test_user()

    # When - 执行操作
    response = client.post("/login", json={"email": user.email, "password": "test"})

    # Then - 验证结果
    assert response.status_code == 200
    assert "token" in response.json()
```

## 单元测试模式

### Happy Path

测试正常输入的预期行为。

```python
def test_add_numbers():
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
```

### Edge Cases

测试边界条件。

```python
def test_add_edge_cases():
    # 大数
    assert add(sys.maxsize, 1) == sys.maxsize + 1

    # 浮点数
    assert abs(add(0.1, 0.2) - 0.3) < 1e-9

    # 类型边界
    with pytest.raises(TypeError):
        add("a", 1)
```

### Error Cases

测试错误处理。

```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_input():
    with pytest.raises(ValueError) as exc_info:
        parse_date("invalid")
    assert "Invalid date format" in str(exc_info.value)
```

## Mock 模式

### Mock 外部服务

```python
@patch('module.external_api.call')
def test_with_mock_api(mock_call):
    mock_call.return_value = {"status": "success"}

    result = process_data()

    assert result == "success"
    mock_call.assert_called_once()
```

### Mock 数据库

```python
@pytest.fixture
def mock_db(mocker):
    mock = mocker.patch('module.database.query')
    mock.return_value = [{"id": 1, "name": "test"}]
    return mock

def test_get_users(mock_db):
    users = get_users()
    assert len(users) == 1
```

## 参数化测试

```python
@pytest.mark.parametrize("input,expected", [
    (1, "one"),
    (2, "two"),
    (3, "three"),
    (11, "eleven"),
    (21, "twenty-one"),
])
def test_number_to_words(input, expected):
    assert number_to_words(input) == expected
```

## Fixture 模式

### 工厂 Fixture

```python
@pytest.fixture
def user_factory():
    def create_user(**kwargs):
        defaults = {
            "name": "Test User",
            "email": "test@example.com",
        }
        defaults.update(kwargs)
        return User(**defaults)
    return create_user

def test_user_creation(user_factory):
    user = user_factory(name="Custom Name")
    assert user.name == "Custom Name"
```

### 数据库 Fixture

```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()
```

## 测试覆盖率目标

| 层级 | 目标覆盖率 |
|-----|----------|
| 核心逻辑 | > 90% |
| 业务逻辑 | > 80% |
| 辅助代码 | > 60% |
| 配置/启动 | > 40% |

## 测试命名规范

```
test_<function_name>_<scenario>_<expected_result>

test_add_positive_numbers_returns_sum
test_divide_by_zero_raises_exception
test_parse_date_invalid_format_raises_value_error
```
