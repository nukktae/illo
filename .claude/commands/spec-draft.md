---
description: 리뷰를 통과한 PRD로 Spec 초안을 만든다 (예: /spec-draft P03)
argument-hint: P01~P06
---

$ARGUMENTS 페이지의 Spec을 `docs/spec/` 에 만든다. 한국어로 쓴다.

1. 읽기: `CLAUDE.md`, 해당 PRD, `docs/spec/_template.md`, `docs/spec/00-common.md` (없으면 먼저 없다고 알려 주고 공통 Spec부터 정하자고 제안), `docs/guides/02-spec.md`.
2. PRD의 기능 ID마다 화면, 데이터, API, 상태, 오류 처리를 채운다. 빠진 ID가 없어야 한다.
3. 수용 기준 하나당 테스트 케이스 하나 이상 (`$ARGUMENTS-T01`, Given, When, Then, 정상/실패/예외).
4. AI를 쓰는 기능은 프롬프트 요지, JSON 출력 스키마, 시간 제한, 실패 처리, 근거를 지어내지 못하게 막는 확인 방법을 적는다.
5. 키는 환경 변수 이름만. 정하지 못한 기술 선택은 선택지 2~3개와 추천을 "미결"로 남긴다.
6. 쓰기 전에 목차와 큰 결정만 먼저 보여 주고 OK를 받는다.
