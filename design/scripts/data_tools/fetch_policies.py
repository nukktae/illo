"""온통청년 청년정책 API에서 일자리 분야 정책을 모두 받아 research/youth-policy/jobs_policies.json 에 저장한다.

키는 저장소 루트 .env 의 YOUTH_POLICY_KEY 에서 읽는다. 키를 코드나 문서에 적지 않는다.
사용: python3 design/scripts/data_tools/fetch_policies.py
"""
import json, os, urllib.parse, urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
OUT = os.path.join(REPO, 'research/youth-policy/jobs_policies.json')
URL = 'https://www.youthcenter.go.kr/go/ythip/getPlcy?'  # User-Agent 없이 부르면 "invalid api key"가 온다


def load_key():
    for line in open(os.path.join(REPO, '.env'), encoding='utf-8'):
        if line.startswith('YOUTH_POLICY_KEY='):
            return line.split('=', 1)[1].strip()
    raise SystemExit('.env 에 YOUTH_POLICY_KEY 가 없어요')


def main():
    key, out, page = load_key(), [], 1
    while True:
        q = urllib.parse.urlencode({'apiKeyNm': key, 'pageNum': page, 'pageSize': 100, 'rtnType': 'json', 'lclsfNm': '일자리'})
        req = urllib.request.Request(URL + q, headers={'User-Agent': 'Mozilla/5.0'})
        d = json.load(urllib.request.urlopen(req, timeout=60))
        lst = d['result']['youthPolicyList']
        out += lst
        total = d['result']['pagging']['totCount']
        if page * 100 >= total or not lst:
            break
        page += 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{len(out)}건 저장 (전체 {total}건)')


if __name__ == '__main__':
    main()
