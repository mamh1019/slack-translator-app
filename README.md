# Slack Translator App

Slack 채널에서 메시지를 자동으로 번역해 주는 봇입니다.

## 개요

- **API**: FastAPI 기반. Slack Events API, Slash Command(`/locale`) 처리
- **Worker**: Redis 큐에서 메시지를 가져와 OpenAI(GPT-4)로 번역 후 Slack에 전송
- **지원 언어**: 한국어(KO), 영어(EN), 일본어(JP), 중국어(ZH)

## 구조

```
├── api/          # FastAPI 서버 (Slack 웹훅 수신)
└── worker/       # 번역 Worker (Redis → OpenAI → Slack)
```

## 주요 기능

- 채널에 봇 초대 시 자동으로 번역 대상 설정
- `/locale JP` (또는 EN, ZH) Slash Command로 채널별 번역 언어 변경
- 파일 공유 메시지 감지 시 자동 번역 후 스레드로 답글

## 필요 환경

- Python 3.x
- Redis
- OpenAI API Key
- Slack Bot Token (Events API, Slash Command 설정 필요)
- Slack Bot User ID (봇 자신의 메시지 필터링용, 선택)

## 환경 변수 예시

```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
OPENAI_API_KEY=sk-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_BOT_USER_ID=U0XXXXXXX  # Slack 앱 정보에서 확인
```
