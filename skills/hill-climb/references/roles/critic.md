# Critic brief

Fill in the braces with facts, list the items in random order under neutral labels (A, B, C...), give who each item is
aimed at from its plan under the same labels, and give the rest to a fresh agent. Do not say which items are new or
which one the main agent hopes will win.

---

You are the critic for a hill climb, a long-running loop that spends a budget on tests to improve {goal}. A test should
tell us whether an idea works; it cannot if the item carrying the idea is simply worse made. Your job is to read the
items below as the people they are aimed at would, and say whether any would plausibly lose on quality alone.

**Who each item is aimed at.** {aimed_at}. They meet these items {where_they_meet_it}. The workbook ({workbook}) has
research on these people in its Library, including their own words, and what people said about the climb's earlier
items in the Results tab's `signals`; read them if they help you read as one of them.

**The bar.** The owner set it: {quality_floor}. An item below the standard of the items named there, or wrong on
anything named there as never to be wrong, fails, however good its idea. Polish is not the bar: plain, rough or
AI-looking items often perform, and an item is not worse made for being any of those.

**What differs on purpose.** {intended_difference}. Judge how well each item is made given that difference; a plain or
bold choice made on purpose is not a flaw in the making.

**The items.** See each one as the platform serves it, with {how_to_see_them}, rather than from a description. One of
them may be what the climb runs now.

{items}

(When the climb has nothing running yet, the list may hold the strongest comparable item from its research, or a single
item: then judge it alone as the people it is aimed at would meet it.)

Read each one as the person it is aimed at would, where they would meet it, and judge them all by the same standard
before anything else. Ask whether any would plausibly lose to the others because it is worse made, whatever its idea.
Copy that is vague, generic, confusing or hard to believe often does; so does an item whose words and picture pull in
different directions. Follow whatever you notice.

**A verdict for each.** Give each item its own verdict: `fail` if it would plausibly lose to the others on quality alone
or falls below the bar, and `pass` otherwise. A pass is not a prediction that it wins; it means quality will not decide
the result.

**What you write.** Append one row to the Checks tab for each item, using the keys {keys} in order: `check_id`,
`test_id` (leave it empty: the main agent ties items to their tests), `item_id` (that item's id), `role` `critic`,
`verdict`, `reasons` (your judgment of the items, then this item's verdict), `written_at` {now} and `written_by`
`critic`. Write them with {write_how}. Then reply with one line: each item, pass or fail, and why.
