"""게시판 API 진입점."""

import os

from dotenv import load_dotenv
import pymysql
from fastapi import FastAPI, HTTPException

from src.board.controller import board_router

load_dotenv()

app = FastAPI(title="게시판 API", version="1.0.0")
app.include_router(board_router)


@app.get("/")
def root() -> dict:
    """헬스 체크."""
    return {"message": "게시판 API", "docs": "/docs"}


@app.get("/api/test/users")
def get_users_from_mysql() -> list[dict]:
    """
    테스트용: MySQL의 users 테이블을 조회해서 반환합니다.

    필요한 환경변수:
    - MYSQL_HOST
    - MYSQL_PORT
    - MYSQL_USER
    - MYSQL_PASSWORD
    - MYSQL_DATABASE
    """

    host = os.getenv("MYSQL_HOST", "127.0.0.1")
    port_raw = os.getenv("MYSQL_PORT", "3307")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    database = os.getenv("MYSQL_DATABASE")

    if not user or not password or not database:
        raise HTTPException(
            status_code=500,
            detail="MySQL 설정이 필요합니다: MYSQL_USER/MYSQL_PASSWORD/MYSQL_DATABASE",
        )

    try:
        port = int(port_raw)
    except ValueError:
        raise HTTPException(status_code=500, detail="MYSQL_PORT는 정수여야 합니다.")

    try:
        with pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name FROM users;")
                rows = cursor.fetchall()
                # users 테이블이 없거나 컬럼이 다르면 여기서 에러가 납니다.
                return rows
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {e}")
