# WorkInKorea Server
work in korea 한국 취업 정보를 제공하는 FastAPI 기반 백엔드 서버.


## 사전 요구사항
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 패키지 매니저

### uv 설치
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```


## 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd workinkorea-server
```

### 2. .env 파일 생성
```bash
# fronend url
CLIENT_URL={user_url}
COOKIE_DOMAIN={domain_name}

# email
MAIL_USERNAME={mail_username}
MAIL_PASSWORD={mail_passwd}
MAIL_FROM_NAME={mail_from_name}
MAIL_FROM={mail_from}
MAIL_PORT={mail_port}
MAIL_SERVER={mail_server}

# db
DATABASE_ASYNC_URL=postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}
DATABASE_SYNC_URL=postgresql://{user}:{password}@{host}:{port}/{database_name}

# google 
GOOGLE_CLIENT_ID={google_client_id}
GOOGLE_CLIENT_SECRET={google_client_secret}
GOOGLE_REDIRECT_URI={google_redirect_uri}
GOOGLE_AUTHORIZATION_URL={google_authorization_url}
GOOGLE_TOKEN_URL={google_token_url}
GOOGLE_USER_INFO_URL={google_user_info_url}

# JWT
JWT_SECRET={jwt_secret}
JWT_ALGORITHM={jwt_algorithm}
ACCESS_TOKEN_EXPIRE_MINUTES={access_token_expire_minutes}
REFRESH_TOKEN_EXPIRE_MINUTES={refresh_token_expire_minutes}

# MINIO
MINIO_ENDPOINT={minio_endpoint}
MINIO_ACCESS_KEY={minio_access}
MINIO_SECRET_KEY={minio_secret}
MINIO_BUCKET_NAME={minio_bucket}


# ADMIN JWT (어드민 전용 토큰 시스템)
ADMIN_JWT_SECRET={admin_secret}
ADMIN_JWT_ALGORITHM={admin_algo}
ADMIN_ACCESS_TOKEN_EXPIRE_MINUTES={admin_access_token_expire_minutes}
ADMIN_REFRESH_TOKEN_EXPIRE_MINUTES={admin_refresh_token_expire_minutes}
ADMIN_EMAILS={admin_emails}
```

### 3. 가상환경(선택)
```bash
# uv를 통해 가상환경이 필요 없음.
uv venv
source .venv/bin/activate
```

### 4. 의존성 설치
```bash
# 모든 의존성을 정확한 버전으로 설치
uv sync
```

### 5. 서버 시작
```bash
# uvicorn으로 실행
uv run uvicorn app.main:app --reload --port 8000
```

## API 문서
- **Swagger 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc


## 디렉토리 구조
```bash
workinkorea-server/
├── app/                          # 메인 애플리케이션
│   ├── __init__.py               # Python 패키지 초기화
│   ├── main.py                   # FastAPI 앱 및 엔트리포인트
│   ├── database.py               # 데이터베이스 설정
│   ├── auth/                     # 인증 관련 모듈
│   │   ├── __init__.py
│   │   ├── models.py             # 인증 모델 (SQLAlchemy)
│   │   ├── router.py             # 인증 라우터 (FastAPI)
│   │   ├── schemas.py            # 인증 스키마 (Pydantic)
│   │   └── service.py            # 인증 비즈니스 로직
│   ├── users/                    # 사용자 관리 모듈
│   │   └── __init__.py
│   └── posts/                    # 게시글 관리 모듈
│       └── __init__.py
├── pyproject.toml                # 프로젝트 설정 및 의존성
├── uv.lock                       # 정확한 의존성 버전 고정
├── README.md                     
└── .gitignore                     
```

## 데이터베이스 마이그레이션 (alembic 사용)

alembic/env.py 파일에 모델 추가
```bash
# alembic/env.py

# 모델 추가
from app.auth.models import *
```

```bash
# 마이그레이션 생성
uv run alembic revision --autogenerate -m "Creat your message"

# 마이그레이션 적용
uv run alembic upgrade head

# 마이그레이션 롤백
uv run alembic downgrade -1

# 또는 특정 마이그레이션 롤백
uv run alembic history 

uv run alembic downgrade <revision>

```