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
        for value in ('background: #FDECEC', 'color: #B42318', 'font-weight: 600', 'text-decoration: none', 'box-decoration-break: clone'):
            self.assertIn(value, style)
        self.assertNotIn('underline', style)
        self.assertIn('border: 1px solid #B42318', style)
        self.assertEqual(self.ns['MK']['no'][2], '#EEF0F3')

    def test_P03_T56_T57_T60_matched_and_partial_boxes(self):
        for key, bg, color in (('ok', '#E8F5EC', '#166534'), ('part', '#FFF6E5', '#C26A00')):
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
                self.assertNotIn('border:', self.ns['mk_badge'](key, compare=True))

    def test_P03_T64_evidence_badge_colors(self):
        for key, label, color, bg in (('ok', '맞음', '#166534', '#E8F5EC'),
                                      ('part', '일부', '#C26A00', '#FFF6E5'),
                                      ('no', '없음', '#B42318', '#FDECEC')):
            with self.subTest(state=key):
                badge = self.ns['mk_badge'](key, compare=True)
                self.assertIn(f'background: {bg}', badge)
                self.assertIn(f'color: {color}', badge)
                self.assertIn(f'>{label}</span>', badge)
                self.assertNotIn('border:', badge)
                self.assertIn('padding: 2px 8px', badge)

    def test_P03_T65_ring_colors_and_proportions(self):
        import xml.etree.ElementTree as ET
        ring = self.ns['score_ring']()
        svg = ET.fromstring(re.search(r'<svg.*?</svg>', ring)[0])
        arcs = [e for e in svg if 'stroke-dasharray' in e.attrib]
        self.assertEqual([e.get('stroke') for e in arcs], ['#22C55E', '#F59E0B', '#EF4444'])
        for arc, units, offset in zip(arcs, (1, 1, 4), (0, 1, 2)):
            length, circumference = map(float, arc.get('stroke-dasharray').split())
            self.assertAlmostEqual((length + 2) / circumference, units / 6, delta=.001)
            self.assertAlmostEqual(float(arc.get('stroke-dashoffset')) / circumference, -offset / 6, delta=.001)
        self.assertIn('6개 중 맞음 1, 일부 1, 없음 4', ring)
        self.assertIn('>2<span', ring)
        self.assertIn('>/6</span>', ring)

    def test_P03_T66_shared_badge_default_preserved(self):
        for key, bg in (('ok', '#E8F3FF'), ('part', '#FFF6E5'), ('no', '#EEF0F3')):
            self.assertIn(f'background: {bg}', self.ns['mk_badge'](key))

    def test_P03_T32_white_body(self):
        for mobile in (False, True):
            result = self.ns['posting_card'](mobile)
            self.assertNotIn('background: #EDF2F8;', result)
            self.assertIn('aria-label="공고 본문"', result)
            self.assertNotIn('background: #EDF2F8;', self.ns['side_panel'](mobile))

    def test_P03_T54_T62_contrast(self):
        def luminance(color):
            values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
            values = [v / 12.92 if v <= 0.04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
            return sum(v * w for v, w in zip(values, (.2126, .7152, .0722)))
        def contrast(a, b):
            light, dark = sorted((luminance(a), luminance(b)), reverse=True)
            return (light + .05) / (dark + .05)
        for key in ('ok', 'no'):
            style = self.ns['HL'][key]
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
