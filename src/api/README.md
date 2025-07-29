# 统一API响应格式

本项目实现了统一的API响应格式，所有API接口都会返回标准化的响应结构。

## 响应格式

### 成功响应
```json
{
    "code": 0,
    "msg": "success",
    "data": {...}
}
```

### 错误响应
```json
{
    "code": 1,
    "msg": "error message",
    "data": null
}
```

## 使用方法

### 方法1：直接返回ApiResponse对象（推荐）

```python
from fastapi import APIRouter
from pydantic import BaseModel
from ..response import ApiResponse, success_response
from ..exceptions import ApiException

router = APIRouter()

class UserInfo(BaseModel):
    id: int
    name: str
    email: str

@router.get("/users/{user_id}")
async def get_user(user_id: int) -> ApiResponse[UserInfo]:
    if user_id <= 0:
        raise ApiException("用户ID无效", 400)
    
    user = UserInfo(id=user_id, name="张三", email="zhangsan@example.com")
    return success_response(user, "获取用户信息成功")
```

### 方法2：使用便捷函数

```python
from ..response_wrapper import api_success, api_error

@router.get("/users")
async def get_users() -> dict[str, Any]:
    users = [{"id": 1, "name": "张三"}, {"id": 2, "name": "李四"}]
    return api_success(users, "获取用户列表成功")

@router.post("/users")
async def create_user(request: CreateUserRequest) -> dict[str, Any]:
    try:
        # 业务逻辑
        return api_success({"id": 999}, "创建成功")
    except Exception as e:
        return api_error(f"创建失败: {str(e)}", 500)
```

### 方法3：抛出异常（自动处理）

```python
from ..exceptions import ApiException
from fastapi import HTTPException

@router.delete("/users/{user_id}")
async def delete_user(user_id: int) -> UserInfo:
    if user_id <= 0:
        raise ApiException("用户ID无效", 400)
    
    if user_id > 100:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return UserInfo(id=user_id, name="已删除", email="deleted@example.com")
```

### 方法4：返回原始数据（需要中间件支持）

```python
@router.get("/simple")
async def simple_response() -> dict[str, str]:
    return {"message": "这是一个简单的响应"}
```

## 异常处理

### 自定义异常
```python
from ..exceptions import ApiException

# 抛出业务异常
raise ApiException("业务错误信息", 400)
```

### HTTP异常
```python
from fastapi import HTTPException

# 抛出HTTP异常
raise HTTPException(status_code=404, detail="资源不存在")
```

### 参数验证异常
当请求参数验证失败时，会自动返回422错误响应：
```json
{
    "code": 422,
    "msg": "请求参数验证失败: name: field required; email: invalid email",
    "data": null
}
```

## 响应模型

### ApiResponse[T]
```python
class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(description="响应状态码，0表示成功，非0表示失败")
    msg: str = Field(description="响应消息")
    data: T | None = Field(default=None, description="响应数据")
```

## 便捷函数

### success_response(data, msg="success")
创建成功响应对象

### error_response(msg, code=1, data=None)
创建错误响应对象

### api_success(data, msg="success")
创建成功响应字典

### api_error(msg, code=1, data=None)
创建错误响应字典

## 示例

访问 `/api/example` 路径查看各种使用方法的示例：

- `GET /api/example/users/{user_id}` - 直接返回ApiResponse
- `GET /api/example/users` - 使用便捷函数
- `POST /api/example/users` - 错误处理示例
- `DELETE /api/example/users/{user_id}` - 异常处理
- `PUT /api/example/users/{user_id}` - HTTPException处理
- `GET /api/example/simple` - 原始数据返回
- `GET /api/example/numbers` - 列表数据
- `GET /api/example/empty` - 空响应

## 最佳实践

1. **推荐使用方法1**：直接返回`ApiResponse[T]`对象，类型安全且清晰
2. **异常处理**：使用`ApiException`抛出业务异常，使用`HTTPException`抛出HTTP异常
3. **参数验证**：依赖FastAPI的自动参数验证，异常会被自动处理
4. **错误码**：使用有意义的错误码，0表示成功，非0表示失败
5. **消息**：提供清晰、用户友好的错误消息 