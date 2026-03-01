"""게시판 API 컨트롤러 - HTTP 엔드포인트 담당."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.board.model import PostCreate, PostUpdate
from src.board.service import BoardService


class PostCreateRequest(BaseModel):
    """게시글 등록 요청 스키마."""

    title: str
    content: str
    author: str


class PostUpdateRequest(BaseModel):
    """게시글 수정 요청 스키마."""

    title: str | None = None
    content: str | None = None

board_router = APIRouter(prefix="/api/board", tags=["board"])


def get_board_service() -> BoardService:
    """BoardService 의존성 (실제 앱에서는 DI 컨테이너 사용 권장)."""
    from src.board.repository import BoardRepository

    return BoardService(BoardRepository())


@board_router.get("/posts")
def list_posts() -> list:
    """게시글 목록 조회."""
    service = get_board_service()
    posts = service.get_posts()
    return [_post_to_dict(p) for p in posts]


@board_router.get("/posts/{post_id}")
def get_post(post_id: int) -> dict:
    """게시글 단건 조회."""
    service = get_board_service()
    post = service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return _post_to_dict(post)


@board_router.post("/posts")
def create_post(body: PostCreateRequest) -> dict:
    """게시글 등록."""
    service = get_board_service()
    try:
        post = service.create_post(
            PostCreate(title=body.title, content=body.content, author=body.author)
        )
        return _post_to_dict(post)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@board_router.patch("/posts/{post_id}")
def update_post(post_id: int, body: PostUpdateRequest) -> dict:
    """게시글 수정."""
    service = get_board_service()
    post = service.update_post(
        post_id, PostUpdate(title=body.title, content=body.content)
    )
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return _post_to_dict(post)


@board_router.delete("/posts/{post_id}")
def delete_post(post_id: int) -> dict:
    """게시글 삭제."""
    service = get_board_service()
    if not service.delete_post(post_id):
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return {"message": "삭제되었습니다."}


def _post_to_dict(post) -> dict:
    """Post 엔티티를 API 응답용 dict로 변환."""
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at.isoformat(),
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
    }
