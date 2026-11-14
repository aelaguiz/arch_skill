"""Tests for the rendered deck: the slide order, each evidence kind's HTML, the redline, escaping and links."""
import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import decision_deck_deck as deck  # noqa: E402
import decision_deck_diff as diff  # noqa: E402
import decision_deck_inline as inline  # noqa: E402
import decision_deck_render as render  # noqa: E402
from test_decision_deck_spec import TempDirCase, spec_dict  # noqa: E402

NB = '<span class="nb">{}</span>'


def slide(html: str, i: int) -> str:
    start = html.index(f'id="sl-{i}"')
    end = html.find('<section class="slide', start)
    return html[start:end if end > 0 else len(html)]


def lines_of(html: str) -> list[str]:
    return re.findall(r'<p class="line">(.*?)</p>', html, re.S)


def one_line(before: str, after: str) -> str:
    (line,) = lines_of(diff.inline_diff(before, after))
    return line


class DeckPageTest(TempDirCase):
    def setUp(self):
        super().setUp()
        self.spec = self.load()
        self.html = render.deck_page(self.spec, [])

    def test_cover_then_one_slide_per_decision_then_the_summary(self):
        sections = re.findall(r'<section class="slide ([^"]*)"', self.html)
        self.assertEqual(sections, ["cover-s", "item", "item", "item", "item", "closing"])
        self.assertIn("Shop relaunch", slide(self.html, 0))
        self.assertIn('id="done-btn"', slide(self.html, 5))
        self.assertIn("Ordering: Pickup only at launch", re.sub(r"<[^>]+>", "", slide(self.html, 5)))

    def test_a_decision_slide_runs_title_why_evidence_answers_in_order(self):
        s = slide(self.html, 2)
        marks = ['class="title"', 'class="rec"', 'class="ev', 'class="dock"', 'data-status="D2"']
        positions = [s.index(m) for m in marks]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(s.count('class="choice"'), 2)
        self.assertIn('<span class="m">Recommended</span>', s)
        self.assertIn('data-item="D2"', s)

    def test_no_comment_box_where_the_decision_takes_no_note_and_no_recommendation_is_said(self):
        s = slide(self.html, 4)
        self.assertNotIn("<textarea", s)
        self.assertIn("<b>No recommendation.</b> Your call.", s)
        self.assertIn("<kbd>E</kbd>", s)

    def test_a_long_question_moves_under_the_evidence(self):
        dec = self.spec["decisions"][0]
        dec["question"] = "Which of the two hero layouts should the relaunched homepage use on every screen size?"
        title, moved = render.shown_title(dec)
        self.assertEqual((title, moved), ("Hero", True))
        self.assertIn(dec["question"], deck.context_text(dec, moved))

    def test_the_page_data_carries_pictures_by_content_hash(self):
        data = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', self.html, re.S).group(1))
        item = data["items"][0]
        self.assertEqual(item["kind"], "images")
        self.assertEqual([c["tag"] for c in item["columns"]], ["split", "banner"])
        self.assertRegex(item["columns"][0]["figs"][0]["src"], r"^/img/[0-9a-f]{16}$")
        self.assertEqual(data["start"], 0)

    def test_the_chart_draws_one_emphasised_bar_and_direct_labels(self):
        s = slide(self.html, 3)
        svg = s[s.index("<svg"):s.index("</svg>")]
        fills = re.findall(r'<rect [^>]*fill="([^"]+)"', svg)
        self.assertEqual((fills.count("var(--data-1)"), fills.count("var(--data-muted)")), (1, 2))
        for text in ("Free over $25", "310 orders", "180 orders"):
            self.assertIn(text, svg)
        self.assertIn('<p class="src">Source: Twelve weeks of orders</p>', s)

    def test_a_chart_with_a_prefix_uses_the_grid_drawing(self):
        ev = {"kind": "chart", "prefix": "$", "decimals": 2, "bars": [{"label": "Flat", "value": 3.5, "note": "per order"}]}
        html = deck.chart_html(ev)
        self.assertNotIn("<svg", html)
        self.assertIn("$3.50", html)
        self.assertIn("per order", html)

    def test_the_table_marks_number_columns_and_labels_cells_for_the_phone(self):
        s = slide(self.html, 4)
        self.assertIn('<th role="columnheader">Option</th>', s)
        self.assertIn('<th role="columnheader" class="num">Staff</th>', s)
        self.assertIn('<td role="rowheader" data-label="Option">Early</td>', s)
        self.assertIn('<td class="num" role="cell" data-label="Staff">2</td>', s)

    def test_a_wide_table_shows_one_card_per_row_on_a_phone(self):
        self.assertTrue(deck.phone_fits(["A", "B"], [["x", "y"]]))
        self.assertFalse(deck.phone_fits(list("ABCDE"), [list("vwxyz")]))

    def test_text_is_escaped_and_urls_become_links(self):
        data = spec_dict()
        data["title"] = "<script>alert(1)</script>"
        data["decisions"][1]["context"] = "See https://example.com/policy. Then decide <b>now</b>."
        self.spec_path.write_text(json.dumps(data))
        html = render.deck_page(self.load(), [])
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn('<a href="https://example.com/policy" target="_blank" rel="noopener noreferrer">', html)
        self.assertIn("&lt;b&gt;now&lt;/b&gt;", html)

    def test_the_header_shows_where_the_deck_comes_from_only_when_given(self):
        self.assertNotIn('class="from"', self.html)
        self.assertIn('<span class="from" title="From the shop team">From the shop team</span>',
                      render.deck_page(self.spec, [], source="From the shop team"))

    def test_the_page_opens_on_the_slide_asked_for_and_carries_the_ledger(self):
        records = [{"kind": "pick", "decision_id": "D1", "option_id": "split", "label": "Split", "note": "", "ts": "t1"}]
        html = render.deck_page(self.spec, records, start=2, gen=7)
        data = json.loads(re.search(r'id="data">(.*?)</script>', html, re.S).group(1))
        self.assertEqual((data["start"], data["gen"], data["n"]), (2, 7, 1))
        self.assertEqual(data["state"]["decisions"]["D1"]["choice"], "split")


class RedlineTest(unittest.TestCase):
    def test_the_diff_slide_marks_words_beside_the_rule_panel(self):
        html = diff.diff_html({"before": "Exchanges only on the day.", "after": "Exchanges or refunds on the day.",
                               "rule_now": "Exchanges or refunds on the day."})
        self.assertIn("The rule now reads", html)
        self.assertEqual(lines_of(html), ["Exchanges <del>only</del><ins>or refunds</ins> on the day."])
        self.assertIn("removed", html)
        self.assertIn("added", html)

    def test_a_few_words_changed_stay_word_by_word(self):
        self.assertEqual(one_line("The quick brown fox jumps over the lazy dog.",
                                  "The quick red fox jumps over the sleepy dog."),
                         "The quick <del>brown</del><ins>red</ins> fox jumps over the <del>lazy</del><ins>sleepy</ins> dog.")

    def test_a_rewritten_paragraph_shows_whole_old_then_whole_new(self):
        old = "Our bread is baked each morning and sold until it runs out, usually by noon."
        new = "Order online before eight and collect a warm loaf at the counter."
        self.assertLess(diff.word_ratio(old, new), diff.REWRITE_AT)
        line = one_line(old, new)
        self.assertEqual((line.count("<del>"), line.count("<ins>")), (1, 1))
        self.assertTrue(line.startswith("<del>Our bread") and line.endswith("counter.</ins>"))

    def test_paragraphs_pair_in_order_with_unequal_counts(self):
        before = "Opening: early.\n\nPrices: unchanged for the year.\n\nParking: none."
        after = "Opening: late.\n\nPrices: unchanged for the whole year."
        pairs = diff.align(diff.paragraphs(before), diff.paragraphs(after))
        self.assertEqual(pairs, [("Opening: early.", "Opening: late."),
                                 ("Prices: unchanged for the year.", "Prices: unchanged for the whole year."),
                                 ("Parking: none.", None)])
        lines = lines_of(diff.inline_diff(before, after))
        self.assertEqual(lines[1], "Prices: unchanged for the <ins>whole</ins> year.")
        self.assertEqual(lines[2], "<del>Parking: none.</del>")

    def test_word_diff_edges_line_breaks_and_escaping(self):
        self.assertEqual(diff.word_diff("a b c.", "a b"), "a b <del>c.</del>")
        self.assertEqual(diff.word_diff("a", "a x"), "a <ins>x</ins>")
        self.assertEqual(diff.word_diff("one\ntwo here", "one\n2 here"), "one\n<del>two</del><ins>2</ins> here")
        self.assertEqual(diff.word_diff("Bread & Butter", "Bread & <Butter>"), "Bread &amp; <del>Butter</del><ins>&lt;Butter&gt;</ins>")

    def test_markdown_in_rule_text_shows_formatted(self):
        self.assertEqual(one_line("**Trigger**: run `bake.py` first.", "**Trigger**: run `bake.py` first."),
                         f"<strong>Trigger</strong>: run <code>{NB.format('bake.py')}</code> first.")
        self.assertEqual(one_line("Run the check first.", "Run the **check** first."),
                         "Run the <del>check</del><ins><strong>check</strong></ins> first.")
        for same in ("Match *.py files.", "A lone ** stays.", "An odd ` tick."):
            self.assertEqual(one_line(same, same), same)

    def test_a_short_quoted_phrase_is_marked_whole(self):
        line = one_line('Say "fresh every morning" on the sign.', 'Say "baked before dawn" on the sign.')
        self.assertEqual((line.count("<del>"), line.count("<ins>")), (1, 1))
        self.assertIn("<del>&quot;fresh every morning&quot;</del>", line)

    def test_the_legend_names_only_the_marks_the_redline_has(self):
        html = diff.diff_html({"before": "", "after": "All new."})
        legend = html[html.index('class="legend"'):]
        self.assertIn("added", legend)
        self.assertNotIn("<del>", legend)


class LinksTest(unittest.TestCase):
    def test_url_spans_leave_trailing_punctuation_and_unopened_brackets_outside(self):
        text = "See https://example.com/a. And (https://example.com/b) or https://example.com/c)."
        self.assertEqual([text[s:e] for s, e in inline.url_spans(text)],
                         ["https://example.com/a", "https://example.com/b", "https://example.com/c"])

    def test_only_http_urls_are_linked(self):
        html = inline.linked("Mail mailto:a@example.com or javascript:alert(1) or ftp://x.org")
        self.assertNotIn("<a ", html)

    def test_numbers_drop_a_trailing_zero(self):
        self.assertEqual((inline.number(3.0), inline.number(2.5), inline.number(1200)), ("3", "2.5", "1,200"))


if __name__ == "__main__":
    unittest.main()
