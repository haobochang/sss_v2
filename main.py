"""
主入口文件
保持向后兼容性，重定向到新的API主入口
"""

from src.api.main import app

# 为了保持向后兼容性，直接导出app实例
# 新的启动方式应该使用 src.api.main:app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
