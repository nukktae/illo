# P03 프로토타입 검증

```sh
sh design/build.sh
python3 -m unittest discover -s tests -v
python3 tests/compare_fixtures.py /tmp/illo-compare-fixtures
```

브라우저 검증은 Node 24 이상과 로컬 OmOWright 로더, Chromium 실행 파일이 필요하다. 각 경로는 환경에 맞게 지정한다. 사용자 프로필을 사용하지 않고 임시 프로필을 만들고 종료 시 삭제한다.

```sh
OMOWRIGHT_LOADER=/path/to/omowright.mjs \
CHROME_PATH=/path/to/chromium \
QA_FIXTURES=/tmp/illo-compare-fixtures \
QA_OUTPUT=/tmp/illo-p03-qa \
node tests/compare_browser.mjs
```

- `test_compare.py`: 없음 구절 박스·밑줄 제거, 목차에만 청회색 적용, 기본 팝업 문구 보존, 빈 목차 네 개, 기존 데이터/링크 보존, 수정 링크 교체.
- `compare_browser.mjs`: 실제 클릭으로 F13 팝업 복귀 및 홈/목록/기존 주소 회귀, F14 크기·이력서 이동·재비교, F15 카드 순서·간격·배경·원문 내부 표시. 1440/390/320px에서 검증한다.
- `compare_fixtures.py`: 원본 데이터 변경 없이 `/tmp`에 빈/긴 내용 테스트 화면을 생성한다. 긴 경험 요약은 테스트 화면에만 삽입한다.
- 결과 JSON과 화면 캡처는 `QA_OUTPUT`에 저장한다. 자동 생성 캡처·개인 프로필은 저장소에 추가하지 않는다.
- 실제 AI·P05 저장이 없어 T16, T19의 진행 중, T22, T23, T27, T30은 실행 불가다. 기존 범위의 T29·T31은 이번 자동 테스트 대상이 아니다. 전체 P03 서비스가 완료됐다는 뜻이 아니다.
- 기존 생성기가 파일을 `open()` 후 명시적으로 닫지 않아 unittest에서 ResourceWarning이 출력될 수 있다. 이번 기능 테스트의 실패와 구분한다.

## P02 직무 찾기

```sh
python3 -m unittest discover -s tests -v
python3 tests/job_search_fixtures.py /tmp/illo-p02-fixtures
OMOWRIGHT_LOADER=/path/to/omowright.mjs \
CHROME_PATH=/path/to/chromium \
QA_FIXTURES=/tmp/illo-p02-fixtures \
node tests/job_search_browser.mjs
```

`test_job_search.py`는 실제 생성용 JS의 역량 계산·안정 정렬·입력 불변·날짜 누락·미등록·7직무·페이지 초기화를 Node로 검증한다. `job_search_browser.mjs`는 실제 목록과 별도 가상 자료에서 직무 전환·추천순 시연 고정·최신순/마감순·검색/필터 제외·등록 상태별 표시·P05 시연 저장 후 복귀·P03 이동·북마크를 확인한다. 결과는 `/tmp/illo-p02-qa/`에 기록한다. 실제 P05 저장·역량 분석은 연결하지 않는다.

P02 v1.3 정정: 기본 화면은 마이페이지의 사전 이력서 내용 있음 상태로 SNS 기존 역량 수를 표시한다. 빈 내용은 `empty` 테스트 화면으로 검증한다. 다른 프로필에는 사전 겹침 값을 재사용하지 않으며, 실제 P05 편집·전체 삭제의 페이지 간 전달은 아직 미구현이다.
