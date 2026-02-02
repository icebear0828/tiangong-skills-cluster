# API 设计指南

## RESTful API 原则

### 1. 资源命名

| 规则 | 好 | 差 |
|-----|----|----|
| 使用名词 | /users | /getUsers |
| 使用复数 | /users | /user |
| 小写连字符 | /user-profiles | /userProfiles |
| 层级清晰 | /users/123/orders | /getUserOrders?id=123 |

### 2. HTTP 方法

| 方法 | 用途 | 幂等 | 安全 |
|-----|------|-----|------|
| GET | 读取 | 是 | 是 |
| POST | 创建 | 否 | 否 |
| PUT | 完整更新 | 是 | 否 |
| PATCH | 部分更新 | 否 | 否 |
| DELETE | 删除 | 是 | 否 |

### 3. 状态码

| 状态码 | 含义 | 使用场景 |
|-------|------|---------|
| 200 | OK | 成功 |
| 201 | Created | 创建成功 |
| 204 | No Content | 删除成功 |
| 400 | Bad Request | 参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 冲突 |
| 422 | Unprocessable | 验证失败 |
| 500 | Server Error | 服务器错误 |

### 4. 响应格式

```json
{
  "data": {
    "id": 1,
    "name": "example"
  },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

错误响应:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### 5. 分页

```
GET /users?page=2&per_page=20
GET /users?cursor=abc123&limit=20
```

### 6. 过滤和排序

```
GET /users?status=active&role=admin
GET /users?sort=created_at:desc,name:asc
GET /users?fields=id,name,email
```

### 7. 版本控制

```
# URL 版本
GET /v1/users

# Header 版本
GET /users
Accept: application/vnd.api+json; version=1
```

## GraphQL 指南

### Schema 设计

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts(first: Int, after: String): PostConnection!
}

type PostConnection {
  edges: [PostEdge!]!
  pageInfo: PageInfo!
}

type PostEdge {
  cursor: String!
  node: Post!
}
```

### Query 设计

```graphql
type Query {
  user(id: ID!): User
  users(filter: UserFilter, first: Int, after: String): UserConnection!
}

input UserFilter {
  status: UserStatus
  search: String
}
```

### Mutation 设计

```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}

input CreateUserInput {
  name: String!
  email: String!
}

type CreateUserPayload {
  user: User
  errors: [Error!]
}
```

## 安全考虑

- 使用 HTTPS
- 实现认证（JWT, OAuth）
- 实施授权检查
- 速率限制
- 输入验证
- 敏感数据脱敏
