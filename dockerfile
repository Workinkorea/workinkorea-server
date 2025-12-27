FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치
RUN uv sync --frozen --no-dev

# 소스 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 실행 스크립트 복사
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 실행
ENTRYPOINT ["/entrypoint.sh"]