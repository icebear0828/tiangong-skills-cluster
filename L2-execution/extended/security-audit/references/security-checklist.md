# 安全检查清单

## 注入攻击

### SQL 注入

**检查项**:
- [ ] 使用参数化查询
- [ ] 不拼接 SQL
- [ ] 输入验证

**危险模式**:
```python
# 危险
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# 安全
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 命令注入

**检查项**:
- [ ] 避免 shell=True
- [ ] 不使用 os.system
- [ ] 输入白名单验证

**危险模式**:
```python
# 危险
os.system(f"ping {host}")

# 安全
subprocess.run(["ping", host], shell=False)
```

## 认证授权

### 密码存储

- [ ] 使用 bcrypt/argon2
- [ ] 适当的 cost factor
- [ ] 不存储明文

```python
# 正确
from passlib.hash import bcrypt
hashed = bcrypt.hash(password)
bcrypt.verify(password, hashed)
```

### 会话管理

- [ ] 安全的会话 ID
- [ ] 会话过期
- [ ] 登出时销毁会话
- [ ] 防止会话固定

### JWT

- [ ] 使用强密钥
- [ ] 验证签名
- [ ] 检查过期
- [ ] 不在 payload 存敏感数据

## 敏感数据

### 传输安全

- [ ] 使用 HTTPS
- [ ] HSTS 头
- [ ] 证书验证

### 存储安全

- [ ] 加密敏感数据
- [ ] 安全密钥管理
- [ ] 不记录敏感数据到日志

### 配置

- [ ] 不硬编码密钥
- [ ] 使用环境变量
- [ ] 不提交敏感配置

## XSS 防护

### 输出编码

```python
# 模板自动转义
{{ user_input | e }}

# 手动转义
from markupsafe import escape
safe_output = escape(user_input)
```

### CSP 头

```
Content-Security-Policy: default-src 'self'; script-src 'self'
```

## 访问控制

### 检查项

- [ ] 每个端点验证权限
- [ ] 不信任客户端数据
- [ ] 最小权限原则
- [ ] 记录访问日志

### IDOR 防护

```python
# 危险
@app.get("/users/{user_id}/orders")
def get_orders(user_id: int):
    return db.get_orders(user_id)  # 未检查权限

# 安全
@app.get("/users/{user_id}/orders")
def get_orders(user_id: int, current_user: User):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403)
    return db.get_orders(user_id)
```

## 安全配置

### 生产环境

- [ ] 关闭调试模式
- [ ] 移除开发依赖
- [ ] 最小化暴露信息
- [ ] 安全的错误处理

### 依赖安全

- [ ] 定期更新依赖
- [ ] 检查已知漏洞
- [ ] 锁定版本

## 漏洞严重级别

| 级别 | CVSS | 示例 |
|-----|------|------|
| Critical | 9.0-10.0 | RCE, SQL 注入 |
| High | 7.0-8.9 | 认证绕过 |
| Medium | 4.0-6.9 | XSS, CSRF |
| Low | 0.1-3.9 | 信息泄露 |
| Info | 0 | 最佳实践建议 |

## 常见 CWE

| CWE | 名称 |
|-----|------|
| CWE-89 | SQL 注入 |
| CWE-79 | XSS |
| CWE-78 | 命令注入 |
| CWE-22 | 路径遍历 |
| CWE-798 | 硬编码凭证 |
| CWE-327 | 弱加密 |
