from datetime import datetime

from beanie import Document, Insert, Replace, Save, SaveChanges, Update, before_event
from bleach import ALLOWED_ATTRIBUTES
from pydantic import ConfigDict, Field


class BaseDocument(Document):
    __abstract__ = True

    created_at: datetime | None = Field(default=None, description="创建时间")
    updated_at: datetime | None = Field(default=None, description="更新时间")

    @before_event(Insert)
    async def set_created_at(self):
        print("set_created_at")
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @before_event(Update, Replace, SaveChanges)
    async def set_updated_at(self):
        print("set_updated_at")
        self.updated_at = datetime.now()

    # @before_event(Insert, Save)
    # def set_created_at(self):
    #     print("set_created_at")
    #     self.created_at = datetime.now()
    #     self.updated_at = datetime.now()
