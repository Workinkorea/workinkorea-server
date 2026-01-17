FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Redis 설치
RUN apt-get update && \
    apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Redis 설정 (localhost만 접근 가능하도록)
RUN sed -i 's/bind 127.0.0.1 ::1/bind 127.0.0.1/' /etc/redis/redis.conf && \
    sed -i 's/protected-mode yes/protected-mode no/' /etc/redis/redis.conf

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