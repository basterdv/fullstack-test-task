from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

class FileItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    original_name: str
    mime_type: str
    size: int
    processing_status: str
    scan_status: str | None
    scan_details: str | None
    metadata_json: dict | None
    requires_attention: bool
    created_at: datetime
    updated_at: datetime


class FileUpdate(BaseModel):
    title: str
    action:str


class AlertItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    file_id: str
    level: str
    message: str
    created_at: datetime
    file: FileItem | None = None
