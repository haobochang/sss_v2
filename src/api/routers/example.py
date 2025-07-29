"""
示例路由，展示统一响应格式的使用
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..exceptions import ApiException
from ..response import ApiResponse, error_response, success_response

router = APIRouter()


class UserInfo(BaseModel):
    """用户信息模型"""

    id: int
    name: str
    email: str


class CreateUserRequest(BaseModel):
    """创建用户请求"""

    name: str
    email: str


# 方法1：直接返回ApiResponse对象
@router.get("/users/{user_id}", response_model=ApiResponse[UserInfo])
async def get_user(user_id: int):
    """获取用户信息 - 直接返回ApiResponse"""
    if user_id <= 0:
        raise ApiException("用户ID无效", 400)

    if user_id > 100:
        raise ApiException("用户不存在", 404)

    user = UserInfo(id=user_id, name=f"用户{user_id}", email=f"user{user_id}@example.com")
    return success_response(user, "获取用户信息成功")


# 方法2：使用便捷函数
@router.get("/users", response_model=ApiResponse[list[UserInfo]])
async def get_users():
    """获取用户列表 - 使用便捷函数"""
    users = [
        UserInfo(id=1, name="张三", email="zhangsan@example.com"),
        UserInfo(id=2, name="李四", email="lisi@example.com"),
    ]
    return success_response(users, "获取用户列表成功")


# 方法3：使用装饰器风格（需要自定义装饰器）
@router.post("/users", response_model=ApiResponse[UserInfo])
async def create_user(request: CreateUserRequest):
    """创建用户 - 使用便捷函数"""
    try:
        # 模拟创建用户
        if request.email == "error@example.com":
            return error_response("邮箱已存在", 400)

        user = UserInfo(id=999, name=request.name, email=request.email)
        return success_response(user, "创建用户成功")
    except Exception as e:
        return error_response(f"创建用户失败: {str(e)}", 500)


# 方法4：抛出异常，由异常处理器处理
@router.delete("/users/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: int):
    """删除用户 - 抛出异常由处理器处理"""
    if user_id <= 0:
        raise ApiException("用户ID无效", 400)

    if user_id > 100:
        raise ApiException("用户不存在", 404)

    # 模拟删除成功，返回用户信息
    return success_response(None, "删除用户成功")


# 方法5：使用HTTPException（会被异常处理器包装）
@router.put("/users/{user_id}", response_model=ApiResponse[UserInfo])
async def update_user(user_id: int, request: CreateUserRequest):
    """更新用户 - 使用HTTPException"""
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="用户ID无效")

    if user_id > 100:
        raise HTTPException(status_code=404, detail="用户不存在")
    user = UserInfo(id=user_id, name=request.name, email=request.email)
    # 模拟更新成功
    return success_response(user)


# 方法6：返回原始数据，由中间件自动包装（如果启用）
@router.get("/simple", response_model=ApiResponse[dict[str, str]])
async def simple_response():
    """简单响应 - 返回原始数据"""
    return success_response({"message": "这是一个简单的响应"})


# 方法7：返回列表数据
@router.get("/numbers", response_model=ApiResponse[list[int]])
async def get_numbers():
    """获取数字列表"""
    return success_response([1, 2, 3, 4, 5])


# 方法8：返回None
@router.get("/empty", response_model=ApiResponse)
async def empty_response():
    """空响应"""
    return success_response(None)
