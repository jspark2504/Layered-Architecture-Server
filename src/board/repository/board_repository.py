"""게시판 데이터 저장소 - DB/스토리지 접근 담당."""

from typing import List, Optional

from src.board.model import Post, PostCreate, PostUpdate


class BoardRepository:
    """게시글 CRUD를 담당하는 Repository."""

    def __init__(self) -> None:
        self._storage: dict[int, Post] = {}
        self._next_id = 1

    def find_by_id(self, post_id: int) -> Optional[Post]:
        """ID로 게시글 조회."""
        return self._storage.get(post_id)

    def find_all(self) -> List[Post]:
        """전체 게시글 목록 조회 (최신순)."""
        posts = list(self._storage.values())
        posts.sort(key=lambda p: p.created_at, reverse=True)
        return posts

    def save(self, post_create: PostCreate) -> Post:
        """게시글 저장."""
        from datetime import datetime

        now = datetime.utcnow()
        post = Post(
            id=self._next_id,
            title=post_create.title,
            content=post_create.content,
            author=post_create.author,
            created_at=now,
            updated_at=None,
        )
        self._storage[self._next_id] = post
        self._next_id += 1
        return post

    def update(self, post_id: int, post_update: PostUpdate) -> Optional[Post]:
        """게시글 수정."""
        from datetime import datetime

        post = self._storage.get(post_id)
        if not post:
            return None
        title = post_update.title if post_update.title is not None else post.title
        content = post_update.content if post_update.content is not None else post.content
        updated = Post(
            id=post.id,
            title=title,
            content=content,
            author=post.author,
            created_at=post.created_at,
            updated_at=datetime.utcnow(),
        )
        self._storage[post_id] = updated
        return updated

    def delete_by_id(self, post_id: int) -> bool:
        """게시글 삭제."""
        if post_id in self._storage:
            del self._storage[post_id]
            return True
        return False
