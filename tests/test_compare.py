"""P03-F13~F15 생성기 회귀 검증: python3 -m unittest discover -s tests."""
import re
import unittest

from screen_loader import ROOT, load_screens


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.ns = load_screens()

    def test_P03_T01_T06_trend_labels(self):
        popup = self.ns['trend_popup']
        self.assertIn('공고 목록으로 돌아가기', popup(False, None))
        self.assertIn('이 직무 공고 보기', popup(False, 'S1-list.dc.html'))
        for mobile in (False, True):
            result = popup(mobile, None, '공고 비교로 돌아가기')
            self.assertIn('공고 비교로 돌아가기', result)
            self.assertNotIn('공고 목록으로 돌아가기', result)

    def test_P03_T24_empty_sections(self):
        self.ns.update(DUTIES=[], POST_REQ=[], PROCEDURE='')
        for mobile in (False, True):
            result = self.ns['posting_card'](mobile)
            self.assertEqual(result.count('공고에 기재된 내용이 없어요'), 4)
            for title in ('담당업무', '자격요건', '우대사항', '전형절차'):
                self.assertIn(f'aria-label="{title}"', result)
            self.assertNotIn('<ul', result)

    def test_P03_T26_data_preserved(self):
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

    def test_P03_T33_missing_box(self):
        style = self.ns['HL']['no']
        for value in ('background: #D5DCE5', 'color: #333D4B', 'font-weight: 600', 'text-decoration: none', 'box-decoration-break: clone'):
            self.assertIn(value, style)
        self.assertNotIn('underline', style)
        self.assertIn('border: 1px solid #6B7684', style)
        self.assertEqual(self.ns['MK']['no'][2], '#EEF0F3')

    def test_P03_T56_T57_matched_and_partial_boxes(self):
        for key, bg, color in (('ok', '#E8F3FF', '#1B64DA'), ('part', '#FFF6E5', '#C26A00')):
            with self.subTest(state=key):
                style = self.ns['HL'][key]
                for rule in (f'background: {bg}', f'color: {color}',
                             f'border: 1px solid {color}', 'border-radius: 4px',
                             'padding: 1px 2px', 'font-weight: 600',
                             'text-decoration: none', '-webkit-box-decoration-break: clone',
                             'box-decoration-break: clone'):
                    self.assertIn(rule, style)
                self.assertNotIn('nowrap', style)
                self.assertNotIn('inline-block', style)
                self.assertNotIn('border:', self.ns['mk_badge'](key))

    def test_P03_T32_white_body(self):
        for mobile in (False, True):
            result = self.ns['posting_card'](mobile)
            self.assertNotIn('background: #EDF2F8;', result)
            self.assertIn('aria-label="공고 본문"', result)
            self.assertNotIn('background: #EDF2F8;', self.ns['side_panel'](mobile))

    def test_P03_T54_contrast(self):
        def luminance(color):
            values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            values = [v / 12.92 if v <= 0.04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
            return sum(v * w for v, w in zip(values, (.2126, .7152, .0722)))
        def contrast(a, b):
            light, dark = sorted((luminance(a), luminance(b)), reverse=True)
            return (light + .05) / (dark + .05)
        style = self.ns['HL']['no']
        background = re.search(r'background: (#[A-Fa-f0-9]{6})', style)[1]
        foreground = re.search(r'color: (#[A-Fa-f0-9]{6})', style)[1]
        border = re.search(r'border: 1px solid (#[A-Fa-f0-9]{6})', style)[1]
        self.assertGreaterEqual(contrast(foreground, background), 4.5)
        for adjacent in (background, '#FFFFFF'):
            self.assertGreaterEqual(contrast(border, adjacent), 3)
        blank = self.ns['posting_section']('빈 목차', '', True)
        blank_color = re.search(r'color: (#[A-Fa-f0-9]{6})', blank)[1]
        self.assertGreaterEqual(contrast(blank_color, '#FFFFFF'), 4.5)

    def test_P03_T55_example_notice(self):
        for mobile in (False, True):
            result = self.ns['side_panel'](mobile)
            self.assertEqual(result.count('시연용 예시 비교 결과'), 2)
            self.assertEqual(result.count('실제 AI 분석은 아직 연결되지 않았어요'), 2)
            self.assertNotIn('AI가 문장마다 근거를 찾고', result)

    def test_P03_T10_T11_resume_secondary(self):
        for mobile in (False, True):
            result = self.ns['side_panel'](mobile)
            self.assertEqual(result.count('나의 이력서 수정'), 1)
            if mobile:
                self.assertIn('min-height: 44px', result)
            else:
                # 데스크톱은 두 버튼이 같은 크기 (2026.11.02 아노 결정)
                self.assertEqual(result.count('width: 100%; height: 52px'), 2)
            self.assertLess(result.index('AI로 비교하기'), result.index('나의 이력서 수정'))
            self.assertNotIn('이력서 수정 ›', result)
            self.assertIn(('m-' if mobile else '') + 'S5-resume.dc.html', result)


if __name__ == '__main__':
    unittest.main()
