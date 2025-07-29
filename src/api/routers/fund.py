from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.api.response import ApiResponse
from src.database.orm import Fund

router = APIRouter()


class CreateFundRequest(BaseModel):
    """创建基金请求模型"""

    fund_id: int = Field(..., description="基金ID")
    fund_name: str = Field(..., min_length=1, description="基金名称")
    fund_code: str = Field(..., min_length=1, description="基金代码")


class UpdateFundRequest(BaseModel):
    """更新基金请求模型"""

    fund_name: str = Field(..., min_length=1, description="基金名称")
    fund_code: str = Field(..., min_length=1, description="基金代码")


class FundResponse(BaseModel):
    """基金响应模型"""

    fund_id: int = Field(..., description="基金ID")
    fund_name: str = Field(..., description="基金名称")
    fund_code: str = Field(..., description="基金代码")


class FundListResponse(BaseModel):
    """基金列表响应模型"""

    funds: list[FundResponse] = Field(..., description="基金列表")


class MessageResponse(BaseModel):
    """消息响应模型"""

    message: str = Field(..., description="响应消息")


@router.get(
    "/list",
    response_model=ApiResponse[FundListResponse],
    summary="获取基金列表",
    operation_id="get_funds",
)
async def get_funds() -> ApiResponse[FundListResponse]:
    """获取基金列表"""
    try:
        funds = await Fund.find().to_list()
        fund_responses = [
            FundResponse(fund_id=fund.fund_id, fund_name=fund.fund_name, fund_code=fund.fund_code)
            for fund in funds
        ]

        return ApiResponse(
            code=0, msg="获取基金列表成功", data=FundListResponse(funds=fund_responses)
        )
    except Exception as e:
        return ApiResponse(code=500, msg=f"获取基金列表失败: {str(e)}", data=None)


@router.get(
    "/{fund_id}",
    response_model=ApiResponse[FundResponse],
    description="获取基金详情",
    summary="获取基金详情",
)
async def get_fund(fund_id: str) -> ApiResponse[FundResponse]:
    """获取基金详情"""
    if not fund_id:
        return ApiResponse(code=400, msg="基金ID不能为空", data=None)

    try:
        fund = await Fund.find_one({"fund_id": int(fund_id)})
        if not fund:
            return ApiResponse(code=404, msg=f"基金不存在: {fund_id}", data=None)

        fund_response = FundResponse(
            fund_id=fund.fund_id, fund_name=fund.fund_name, fund_code=fund.fund_code
        )

        return ApiResponse(code=0, msg="获取基金详情成功", data=fund_response)
    except ValueError:
        return ApiResponse(code=400, msg="基金ID格式不正确", data=None)
    except Exception as e:
        return ApiResponse(code=500, msg=f"获取基金详情失败: {str(e)}", data=None)


@router.post(
    "/create", response_model=ApiResponse[FundResponse], description="创建基金", summary="创建基金"
)
async def create_fund(fund_request: CreateFundRequest) -> ApiResponse[FundResponse]:
    """创建基金"""
    try:
        # 检查基金是否已存在
        existing_fund = await Fund.find_one({"fund_id": fund_request.fund_id})
        if existing_fund:
            return ApiResponse(code=400, msg=f"基金已存在: {fund_request.fund_id}", data=None)

        # 创建新基金
        fund = Fund(
            fund_id=fund_request.fund_id,
            fund_name=fund_request.fund_name,
            fund_code=fund_request.fund_code,
        )
        await fund.insert()

        fund_response = FundResponse(
            fund_id=fund.fund_id, fund_name=fund.fund_name, fund_code=fund.fund_code
        )

        return ApiResponse(code=0, msg="基金创建成功", data=fund_response)
    except Exception as e:
        return ApiResponse(code=500, msg=f"创建基金失败: {str(e)}", data=None)


@router.put(
    "/{fund_id}",
    response_model=ApiResponse[FundResponse],
    description="更新基金",
    summary="更新基金",
)
async def update_fund(fund_id: str, fund_request: UpdateFundRequest) -> ApiResponse[FundResponse]:
    """更新基金"""
    if not fund_id:
        return ApiResponse(code=400, msg="基金ID不能为空", data=None)

    try:
        fund_id_int = int(fund_id)
        # 检查基金是否存在
        existing_fund = await Fund.find_one({"fund_id": fund_id_int})
        if not existing_fund:
            return ApiResponse(code=404, msg=f"基金不存在: {fund_id}", data=None)

        # 更新基金信息
        existing_fund.fund_name = fund_request.fund_name
        existing_fund.fund_code = fund_request.fund_code
        await existing_fund.save()

        fund_response = FundResponse(
            fund_id=existing_fund.fund_id,
            fund_name=existing_fund.fund_name,
            fund_code=existing_fund.fund_code,
        )

        return ApiResponse(code=0, msg="基金更新成功", data=fund_response)
    except ValueError:
        return ApiResponse(code=400, msg="基金ID格式不正确", data=None)
    except Exception as e:
        return ApiResponse(code=500, msg=f"更新基金失败: {str(e)}", data=None)


@router.delete(
    "/{fund_id}",
    response_model=ApiResponse[MessageResponse],
    description="删除基金",
    summary="删除基金",
)
async def delete_fund(fund_id: str) -> ApiResponse[MessageResponse]:
    """删除基金"""
    if not fund_id:
        return ApiResponse(code=400, msg="基金ID不能为空", data=None)

    try:
        fund_id_int = int(fund_id)
        # 检查基金是否存在
        existing_fund = await Fund.find_one({"fund_id": fund_id_int})
        if not existing_fund:
            return ApiResponse(code=404, msg=f"基金不存在: {fund_id}", data=None)

        await existing_fund.delete()

        return ApiResponse(code=0, msg="基金删除成功", data=MessageResponse(message="基金删除成功"))
    except ValueError:
        return ApiResponse(code=400, msg="基金ID格式不正确", data=None)
    except Exception as e:
        return ApiResponse(code=500, msg=f"删除基金失败: {str(e)}", data=None)
