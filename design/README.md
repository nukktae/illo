# design: 프로토타입 화면 원본

여기 있는 건 **디자인 확인과 시연용 프로토타입**이에요. 실제 서비스 코드는 PRD와 Spec이 확정된 뒤 따로 만들어요. 그래서 이 코드는 "화면을 빨리 그리고 고치는 도구"로 짜여 있어요.

## 흐름

```
design/data/*.json        화면에 들어가는 데이터
design/screens/*.py       화면 정의 (페이지별 파일)
        │  ./design/build.sh
        ▼
design/canvas/*.dc.html   Claude 디자인 캔버스 원본 (canvas.json에 보드 배치)
        │  (같은 명령)
        ▼
prototype/*.html          Vercel에 올라가는 정적 HTML (dc-lite.js로 동작)
```

`prototype/` 과 `design/canvas/` 는 직접 고치지 마세요. `design/screens/` 를 고치고 `./design/build.sh` 를 실행하면 둘 다 다시 만들어져요.

## 폴더

| 경로 | 내용 |
|---|---|
| `build.sh` | 화면 전체 다시 만들기 |
| `screens/00_mobile_parts.py` | 모바일 공통 부품: 색, 하단 탭 바, 페이지 틀, 칩, 버튼, 회사 로고 |
| `screens/01_base.py` | 모든 화면 공통: 로그인과 저장 (브라우저 localStorage), 상단 메뉴, 페이지 틀, AI 배지, 트렌드 팝업, 목록 스타일 |
| `screens/10_home.py` | P01 홈 |
| `screens/20_job_search.py` | P02 직무 찾기 (7개 직무, 검색, 필터, 정렬, 페이지) |
| `screens/30_compare.py` | P03 공고 비교 (원문에 AI 결과 표시) |
| `screens/40_next_actions.py` | P03 다음 행동 4가지, 관련 과정 목록, 강북5기 과정 상세 |
| `screens/50_education.py` | P04 교육과정 (SeSAC 210, 청년 정책 213), 정책 상세 |
| `screens/60_mypage.py` | P05 마이페이지 (한눈에 보기, 저장함, 이력서 등록, 취업 수기) |
| `screens/70_auth.py` | P06 로그인, 회원가입 |
| `screens/90_canvas.py` | 파일 쓰기, 캔버스 보드 위치와 메모 |
| `scripts/build_screens.py` | `screens/` 파일을 이름 순서로 실행 (한 이름 공간을 같이 씀) |
| `scripts/export_static.py` | 캔버스 원본을 `prototype/` 정적 HTML로 바꿈. 폰은 `m-` 화면으로 자동 이동 |
| `scripts/dc-lite.js` | 캔버스 형식 (`{{ }}`, `<sc-if>`, `<sc-for>`)을 브라우저에서 그리는 작은 런타임 |
| `scripts/data_tools/` | 데이터 다시 만들기: `fetch_policies.py` (온통청년 API, 키는 `.env`), `build_data.py`, `sns_trend.py` |
| `data/` | 화면 데이터 JSON, `board_heights.json` (보드 높이), `source/` (취업 수기 원본 화면) |
| `assets/` | SeSAC 과정 이미지 |
| `canvas/` | 생성된 캔버스 원본 |

## 화면 고치는 법

1. 고칠 페이지 파일을 `screens/` 에서 찾는다 (위 표).
2. 화면 HTML은 파이썬 f-string 안에 있다. 값 자리 표시는 `@@이름@@` 으로 쓰고, 빌드할 때 `{{ 이름 }}` 으로 바뀐다.
3. 버튼 동작은 각 화면의 `*_JS` 문자열 (`pageVals()` 가 화면 값을 돌려줌).
4. `./design/build.sh` 실행 후 `prototype/` 을 브라우저로 열어 확인한다.
5. 높이가 바뀌면 `data/board_heights.json` 의 보드 높이를 맞춘다 (캔버스에서 잘리지 않게).

## 데이터 다시 만들기

```sh
python3 design/scripts/data_tools/fetch_policies.py      # 청년 정책 원본 다시 받기 (.env 키 필요)
python3 design/scripts/data_tools/build_data.py          # 전부, 또는 policies courses posts jobs 중 골라서
./design/build.sh
```

`jobs` 는 팀원 PC의 `~/Documents/job-board-anu` 원본이 있어야 해요. 기준일이 오늘이라 다시 만들면 신청 상태와 D-day가 바뀌어요.

## 알아 둘 점

- 로그인과 저장은 서버 없이 브라우저에만 남아요 (localStorage). 기기가 바뀌면 사라져요.
- 비교 결과, 이력서 내용은 예시 페르소나 (김하늘, 미디어커뮤니케이션학과) 고정값이에요. 실제 AI 비교는 P03 구현에서 만들어요.
- 데스크톱 1280px, 모바일 390px 기준이에요.
