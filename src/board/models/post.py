"""게시글 모델 정의."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Post:
    """게시글 엔티티."""

    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: Optional[datetime] = None


@dataclass
class PostCreate:
    """게시글 생성 DTO."""

    title: str
    content: str
    author: str


@dataclass
class PostUpdate:
    """게시글 수정 DTO."""

    title: Optional[str] = None
    content: Optional[str] = None
