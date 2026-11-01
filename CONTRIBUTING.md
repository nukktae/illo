# 팀원 시작 가이드

처음 들어온 팀원이 30분 안에 작업을 시작할 수 있게 정리했어요. 순서대로 따라와 주세요.

## 1. 처음 한 번만 설정

1. **GitHub 초대 수락**: 메일로 온 `nukktae/illo` 초대를 수락해요.
2. **내려받기**
   ```sh
   git clone https://github.com/nukktae/illo.git
   cd illo
   ```
3. **Claude Code 설치**: 데스크톱 앱이나 `npm install -g @anthropic-ai/claude-code`. 폴더를 열면 `CLAUDE.md`를 자동으로 읽어요.
4. **키가 필요하면** (`.env`): 팀장에게 직접 받아 `.env.example`을 복사해 `.env`로 만들고 채워요. 키는 카톡, 노션, GitHub, 채팅에 붙이지 않아요. `.env`는 git에 올라가지 않아요.
5. **Python 3**: 프로토타입 화면을 다시 만들 때만 필요해요 (`./design/build.sh`).

## 2. 먼저 읽을 것 (20분)

| 순서 | 문서 | 왜 |
|---|---|---|
| 1 | [CLAUDE.md](CLAUDE.md) | 원칙, 폴더, ID 규칙. AI도 이걸 읽고 일해요 |
| 2 | [docs/prd/00-root.md](docs/prd/00-root.md) | 서비스 전체 그림과 페이지 지도 |
| 3 | 내가 맡은 페이지 PRD (`docs/prd/P0x-*.md`) | 내가 만들 것 |
| 4 | [docs/guides/03-vibe-coding.md](docs/guides/03-vibe-coding.md) | AI로 일하는 방법 |
| 5 | 프로토타입 https://illo-prototype.vercel.app | 화면을 직접 눌러 보기 |

## 3. 일하는 순서

```
PRD 고치기  >  PRD 리뷰 (팀원 1명)  >  Spec 쓰기  >  코드 생성과 테스트  >  PR  >  리뷰  >  main 병합 (자동 배포)
```

- PRD 쓰는 법: [docs/guides/01-prd.md](docs/guides/01-prd.md)
- Spec 쓰는 법: [docs/guides/02-spec.md](docs/guides/02-spec.md)
- AI 코딩: [docs/guides/03-vibe-coding.md](docs/guides/03-vibe-coding.md)
- 프로토타입 화면 고치기: [design/README.md](design/README.md)

## 4. Git 규칙

- **main에 직접 push하지 않아요.** 항상 브랜치를 만들고 PR을 올려요. main에 병합되면 바로 실제 사이트에 배포돼요.
- **브랜치 이름**: 기능 ID를 앞에. `p03-f02-ai-compare`, `p05-f02-resume-form`, 문서만 고치면 `docs-p02-prd`.
- **커밋 메시지**: 한국어로, 무엇을 왜 바꿨는지. 기능 ID를 앞에.
  ```
  P03-F02 공고 문장별 근거 찾기 API 추가

  이력서에 없는 문장을 근거로 돌려주면 없음으로 처리
  ```
- **PR**: 템플릿이 자동으로 떠요. 기능 ID, 바꾼 것, 확인한 방법, 화면 캡처를 채워요. PR을 올리면 Vercel 미리보기 링크가 댓글로 달려요.
- **리뷰**: 팀원 1명이 보고 승인하면 병합해요. 리뷰어는 PRD 수용 기준을 하나씩 눌러 봐요.
- **충돌 줄이기**: 페이지별로 담당을 나눴으니 남의 페이지 파일은 건드리지 않아요. 공통 파일 (`01_base.py`, 공통 컴포넌트, DB 스키마)을 바꿀 때는 단톡에 먼저 말해요.

## 5. 하지 말 것

- 키, 비밀번호, 토큰을 코드나 문서에 쓰기
- 팀원이나 사용자 개인정보 (전화번호, 학번, 생년월일, 주소)를 저장소에 올리기
- `prototype/` 폴더를 손으로 고치기 (`design/`을 고치고 다시 만들어요)
- PRD에 없는 기능을 코드부터 만들기 (PRD에 먼저 넣고 리뷰)
- 화면에 "합격", "합격 확률" 같은 말 쓰기

## 6. 막히면

- 먼저 Claude에게 `CLAUDE.md와 관련 PRD를 읽고 설명해 줘`라고 물어봐요.
- 30분 넘게 막히면 단톡에 화면 캡처와 함께 올려요.
- 개발 멘토링(11/3 23시)에 물어볼 건 `docs/prd/00-root.md` 미결 사항에 적어 둬요.
