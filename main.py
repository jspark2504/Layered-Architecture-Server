"""게시판 API 진입점."""

from fastapi import FastAPI

from src.board.controller import board_router

app = FastAPI(title="게시판 API", version="1.0.0")
app.include_router(board_router)


@app.get("/")
def root() -> dict:
    """헬스 체크."""
    return {"message": "게시판 API", "docs": "/docs"}
