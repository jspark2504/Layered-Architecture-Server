# 게시판 API (Layered Architecture)!

Python + FastAPI 기반 **레이어드 아키텍처** 게시판 서버 프로젝트입니다.

## 목차

- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [레이어 설명](#레이어-설명)
- [API 명세](#api-명세)
- [실행 방법](#실행-방법)

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| 언어 | Python 3.10+ |
| 웹 프레임워크 | FastAPI |
| ASGI 서버 | Uvicorn |
| 검증/직렬화 | Pydantic |

---

## 프로젝트 구조

```
Layered-Architecture-Server/
├── main.py                 # 앱 진입점, 라우터 등록
├── requirements.txt
├── README.md
└── src/
    └── board/
        ├── __init__.py
        ├── model/               # 도메인 모델
        │   ├── __init__.py
        │   └── post.py          # Post, PostCreate, PostUpdate
        ├── repository/          # Repository 레이어 (데이터 접근)
        │   ├── __init__.py
        │   └── board_repository.py
        ├── service/             # Service 레이어 (비즈니스 로직)
        │   ├── __init__.py
        │   └── board_service.py
        └── controller/          # Controller 레이어 (HTTP API)
            ├── __init__.py
            └── board_controller.py
```

---

## 레이어 설명

### 1. Controller (컨트롤러)

- **위치**: `src/board/controller/board_controller.py`
- **역할**: HTTP 요청 수신, 파라미터/바디 검증, Service 호출, HTTP 응답 반환
- **네이밍**: `*_controller.py`, 라우터는 `*_router` 또는 `board_router`

### 2. Service (서비스)

- **위치**: `src/board/service/board_service.py`
- **역할**: 비즈니스 로직 (유효성 검사, 트랜잭션 경계 등). Repository를 통해 데이터 접근
- **네이밍**: `*_service.py`, 클래스는 `BoardService`

### 3. Repository (리포지토리)

- **위치**: `src/board/repository/board_repository.py`
- **역할**: 데이터 저장/조회/수정/삭제. DB 또는 인메모리 스토리지 접근만 담당
- **네이밍**: `*_repository.py`, 클래스는 `BoardRepository`

### 4. Model (모델)

- **위치**: `src/board/model/post.py`
- **역할**: 도메인 엔티티(Post)와 DTO(PostCreate, PostUpdate) 정의

**데이터 흐름**: `Controller → Service → Repository → (DB/Storage)`

---

## API 명세

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/board/posts` | 게시글 목록 조회 (최신순) |
| GET | `/api/board/posts/{post_id}` | 게시글 단건 조회 |
| POST | `/api/board/posts` | 게시글 등록 |
| PATCH | `/api/board/posts/{post_id}` | 게시글 수정 |
| DELETE | `/api/board/posts/{post_id}` | 게시글 삭제 |

### 요청/응답 예시

**POST /api/board/posts** (등록)

```json
{
  "title": "제목",
  "content": "본문",
  "author": "작성자"
}
```

**PATCH /api/board/posts/{post_id}** (수정, 필드 선택)

```json
{
  "title": "새 제목",
  "content": "새 본문"
}
```

---

## 실행 방법

### 1. 가상환경 및 의존성 설치

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
uvicorn main:app --reload
```

### 3. 접속

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

---

## 참고

- 현재 Repository는 **인메모리 딕셔너리**로 구현되어 있어, 서버 재시작 시 데이터가 초기화됩니다.
- 실제 DB 연동 시 `BoardRepository` 내부만 DB 클라이언트로 교체하면 되며, Service/Controller는 그대로 사용할 수 있습니다.
