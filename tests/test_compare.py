"""P03-F13~F15 생성기 회귀 검증: python3 -m unittest discover -s tests."""
import json
import os
from pathlib import Path
import re
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_screens():
    ns = dict(json=json, os=os, re=re, sys=SimpleNamespace(argv=[]), ROOT='/tmp/illo-unused',
              DATA=str(ROOT / 'design/data'), HERE=str(ROOT / 'design/scripts'))
    for path in sorted((ROOT / 'design/screens').glob('*.py')):
        if path.name >= '40':
            break
        exec(compile(path.read_text(), str(path), 'exec'), ns)
    return ns


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.ns = load_screens()

    def test_trend_default_and_compare_labels(self):
        popup = self.ns['trend_popup']
        self.assertIn('공고 목록으로 돌아가기', popup(False, None))
        self.assertIn('이 직무 공고 보기', popup(False, 'S1-list.dc.html'))
        for mobile in (False, True):
            result = popup(mobile, None, '공고 비교로 돌아가기')
            self.assertIn('공고 비교로 돌아가기', result)
            self.assertNotIn('공고 목록으로 돌아가기', result)

    def test_empty_sections_keep_all_titles(self):
        self.ns.update(DUTIES=[], POST_REQ=[], PROCEDURE='')
        for mobile in (False, True):
            result = self.ns['posting_card'](mobile)
            self.assertEqual(result.count('공고에 기재된 내용이 없어요'), 4)
            for title in ('담당업무', '자격요건', '우대사항', '전형절차'):
                self.assertIn(f'aria-label="{title}"', result)
            self.assertNotIn('<ul', result)

    def test_nonempty_data_preserved(self):
        for mobile in (False, True):
            result = self.ns['posting_card'](mobile)
            for duty in self.ns['DUTIES']:
                self.assertIn(duty, result)
            for _, pieces, finds in self.ns['POST_REQ']:
                for text, _ in pieces:
                    self.assertIn(text, result)
                for _, note, action, href in finds:
                    self.assertIn(note, result)
                    if href and action != '트렌드 보기':
                        self.assertIn(('m-' if mobile else '') + href, result)
            self.assertIn(self.ns['PROCEDURE'], result)

    def test_missing_highlight_is_box_without_underline(self):
        style = self.ns['HL']['no']
        for value in ('background: #D5DCE5', 'color: #333D4B', 'font-weight: 600', 'text-decoration: none', 'box-decoration-break: clone'):
            self.assertIn(value, style)
        self.assertNotIn('underline', style)
        self.assertEqual(self.ns['MK']['no'][2], '#EEF0F3')

    def test_section_color_only(self):
        for mobile in (False, True):
            result = self.ns['posting_card'](mobile)
            self.assertEqual(result.count('background: #EDF2F8;'), 4)
            self.assertNotIn('background: #EDF2F8;', self.ns['side_panel'](mobile))

    def test_resume_link_replaced_without_duplicate(self):
        for mobile in (False, True):
            result = self.ns['side_panel'](mobile)
            self.assertEqual(result.count('나의 이력서 수정'), 1)
            self.assertNotIn('이력서 수정 ›', result)
            self.assertIn(('m-' if mobile else '') + 'S5-resume.dc.html', result)


if __name__ == '__main__':
    unittest.main()
