# 프로토타입 검증

저장소 루트에서 실행한다. 페이지별 테스트·검증표는 이 브랜치에 포함된 `P02-cases.md`, `P03-cases.md`를 따른다. 페이지가 분리된 PR에는 해당 페이지의 파일만 포함된다.

```sh
sh design/build.sh
python3 -m unittest discover -s tests -v
```

브라우저 테스트는 Node 24 이상과 OmOWright 로더·Chromium이 필요하다. 사용자 프로필 대신 임시 프로필을 만들고 종료 시 삭제한다.

```sh
export OMOWRIGHT_LOADER=/path/to/omowright.mjs
export CHROME_PATH=/path/to/chromium
# P02 파일이 있는 경우
python3 tests/job_search_fixtures.py /tmp/illo-p02-fixtures
QA_FIXTURES=/tmp/illo-p02-fixtures node tests/job_search_browser.mjs
# P03 파일이 있는 경우
python3 tests/compare_fixtures.py /tmp/illo-compare-fixtures
QA_FIXTURES=/tmp/illo-compare-fixtures node tests/compare_browser.mjs
node tests/compare_keyboard_browser.mjs
```

높이·첫 공고 위치는 수정 전에 기준을 기록하고 수정 후 같은 환경에서 비교한다. P02만 검증할 때는 `QA_PAGE=list`, P03만은 `QA_PAGE=compare`를 지정한다.

```sh
QA_MEASURE=/tmp/before.json node tests/review_layout_browser.mjs
# 변경 후
QA_MEASURE=/tmp/after.json QA_BASELINE=/tmp/before.json node tests/review_layout_browser.mjs
```

결과·캡처는 `/tmp/illo-p02-qa/`, `/tmp/illo-p03-qa/` 또는 지정 경로에만 저장한다. 임시 이미지·브라우저 프로필은 커밋하지 않는다. 기존 생성기에서 ResourceWarning이 나올 수 있으며 실패와 구분한다. 실제 P05 편집·삭제 전달과 실제 AI 생성은 현재 UI 테스트의 검증 범위가 아니다.
