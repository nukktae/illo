# P02 Spec 테스트 추적

2026.11.02 리뷰 반영 검증. 테스트 메서드 수와 수용 기준 수는 다르며, 하나의 시나리오에서 여러 기준을 검증할 수 있다.

| ID | 실행 위치·검증 | 상태 |
|---|---|---|
| P02-T01 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T02 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T03 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T04 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T05 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T06 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T07 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T08 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T09 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T10 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T11 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T12 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T13 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T14 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T15 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T16 | job_search_browser.mjs: 직무·검색·정렬·페이지·상태 시나리오 | 로컬 통과 |
| P02-T17 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T18 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T19 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T20 | test_job_search.py: 고유 교집합·안정 정렬·타입·사전 이력서·빈 내용·seed 분리 | 로컬 통과 |
| P02-T21 | test_job_search.py / job_search_browser.mjs: 제목 우선·7직무 순서 | 로컬 통과 |
| P02-T22 | review_layout_browser.mjs (QA_PAGE=list): 동일 조건 첫 공고 top·높이; browser 스크립트의 320px 넘침 | 로컬 통과 |

실제 P05 편집/삭제 전파·다른 직무 실제 역량 분석은 미구현이다. T08~T11은 별도 합성 자료 검증이며 실제 연동 통과가 아니다.
