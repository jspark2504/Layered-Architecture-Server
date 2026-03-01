"""게시판 비즈니스 로직 - Service 레이어."""

from typing import List, Optional

from src.board.models import Post, PostCreate, PostUpdate
from src.board.repositories import BoardRepository


class BoardService:
    """게시글 관련 비즈니스 로직 담당."""

    def __init__(self, board_repository: BoardRepository) -> None:
        self._repository = board_repository

    def get_post(self, post_id: int) -> Optional[Post]:
        """게시글 단건 조회."""
        return self._repository.find_by_id(post_id)

    def get_posts(self) -> List[Post]:
        """게시글 목록 조회."""
        return self._repository.find_all()

    def create_post(self, post_create: PostCreate) -> Post:
        """게시글 등록."""
        if not post_create.title or not post_create.title.strip():
            raise ValueError("제목은 필수입니다.")
        if not post_create.author or not post_create.author.strip():
            raise ValueError("작성자는 필수입니다.")
        return self._repository.save(post_create)

    def update_post(self, post_id: int, post_update: PostUpdate) -> Optional[Post]:
        """게시글 수정."""
        if not self._repository.find_by_id(post_id):
            return None
        return self._repository.update(post_id, post_update)

    def delete_post(self, post_id: int) -> bool:
        """게시글 삭제."""
        return self._repository.delete_by_id(post_id)
