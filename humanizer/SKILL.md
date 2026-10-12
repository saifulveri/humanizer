---
name: humanizer
description: Rewrites or writes text so it sounds like a real person wrote it, not an AI or a textbook translation. Works in Indonesian and English. Use when the user says "humanizer", "pakai skill humanizer", "biar lebih manusiawi", "kata-katanya kaku", "terlalu formal", "kayak AI", or asks to make copy (website, portfolio, app UI, captions, bios, emails, docs) more natural and relaxed.
---

# Humanizer

Goal: text that reads like a person saying it, plain and to the point. Not stiff, not salesy, not machine-written.

## Before you start

1. Find every piece of text in scope. For a website or app, that means all user-facing copy: hero, headings, buttons, labels, empty states, descriptions, project details, meta description. Do not stop at the first screen.
2. Keep facts locked. Never change numbers, dates, names, client names, product names, prices or tech names. Never add a claim the original did not make. If something is unclear, keep the original meaning and shorten it.
3. Keep the type of text. A button stays a button, a title stays short, a bullet stays a bullet.

## Indonesian

Write the way people actually talk and write today: santai tapi sopan, like explaining to a client over coffee.

- Use loanwords people really use. Do not force a "proper" translation.
  - booking (bukan "janji temu" / "pemesanan"), refund (bukan "pengembalian dana"), login, update, upload, download, dashboard, admin, fitur, tim, klien, deadline, tools, payroll, live, HP (bukan "ponsel" in casual copy)
- Prefer short everyday words:
  - bisa (bukan "dapat"), pakai (bukan "menggunakan" when casual), bikin / membuat (bukan "mengimplementasikan"), cek (bukan "memantau"), punya (bukan "memiliki"), lewat (bukan "melalui"), jalan (bukan "beroperasi")
- Drop stiff and translated phrasing:
  - "memungkinkan pengguna untuk ...", "sebuah", "berbasis", "dilengkapi dengan", "dalam rangka", "adapun", "merupakan", "perancangan", "penyerahan", "mutakhir", "dipelihara", "kokoh", "lintas platform", "secara efektif dan efisien"
- Also swap these (found leaking through earlier passes):
  - "serta" → "dan" · "secara X" → drop it or use the plain adjective · "mengelola" → "atur" / "urus" / the specific verb (catat, hitung, kirim) · "berbasis web/peran" → "web" / "per peran" · "solusi" → what it actually does · "berbagai" → "banyak" or name them · "ditambah" → "dan" / "plus" · "memantau" → "cek" · "dapat" → "bisa" · "demi" → "supaya" · "sistem" / "platform" as filler ("dalam satu sistem") → cut
  - Stacked prepositions are a translation tell: "sistem untuk mengelola X dengan Y yang Z". Split it into two sentences.
- First person "saya" for the owner's own work. No "gue/lo" unless asked. Don't overuse "nggak".

## English

- Plain words, short sentences. Contractions are fine (I've, it's).
- Cut jargon a client would not say: leverage, robust, seamless, end-to-end, scalable architecture, streamlined, cutting-edge, synergy, empower, utilize.
- Use the standard industry term when one exists (Frontend, Backend, Database, Mobile). Do not invent cute replacements and do not explain the term.

## Remove AI-writing patterns (both languages)

- "Not just X, but also Y" / "tidak hanya X, tapi juga Y"
- Forced lists of three, and adjective stacks. A real list of features, modules or tech names is fine; a decorative triple ("cepat, mudah, dan aman") is not. Keep feature lists, trim adjective ones.
- Inflated words: pivotal, crucial, comprehensive, significant, optimal, menyeluruh, komprehensif, krusial, signifikan, optimal
- Em dashes. Use a comma or a full stop.
- Tail clauses that add vague importance: "..., ensuring X", "..., highlighting Y", "..., sehingga memastikan X"
- Vague impact claims and promotional tone ("transforming the way...", "solusi terbaik untuk...")
- Colon lists ("X: A, B, and C") where a normal sentence reads better
- Generic openers and closers ("In today's digital world", "Di era digital ini", "Overall, ...")
- Every sentence the same length. Mix short and medium.

## CV text

- No pronouns, no "saya" / "I". Bullets start with a past-tense verb (Built, Led, Memimpin, Membuat), one line each.
- Numbers and tech names stay exactly. No adjectives about yourself ("berpengalaman", "passionate").
- It must still fit the page after the rewrite. Regenerate the PDF and check.

## Length and layout

- Shorter wins. Cut filler, keep one idea per sentence.
- For UI copy, check that new text still fits: no extra lines in a hero, no labels overflowing buttons or cards. If the project can be run, screenshot mobile (390px) and desktop and fix anything that breaks.

## Audit (mandatory when there are more than ~20 strings)

Script: `~/.claude/skills/humanizer/scripts/audit.py` (python3, no dependencies).

1. Before rewriting: `audit.py scan <files> --out before.json`. If the project has `data/audit/baseline-scan.json`, use that as "before".
2. Rewrite.
3. After: `audit.py scan <files> --out after.json`, then `audit.py diff before.json after.json`. Banned-word count must go down; report banned per 100 strings before and after.
4. For key→value copy maps (original → rewrite): `audit.py facts <copy.json>`. Every listed pair lost a number or a name. Fix it or confirm it was meant.
5. `weak` counts (list3, colon, untuk/dengan/yang, sistem, platform) are watch items, not bans. Use them to find the worst offenders, not to hit zero.

6. Audit the rendered output too, not only the source files. Last time ~100 bullet strings were never touched because the wording layer skipped arrays, and only a scan of the built page (`dist/index.html`) showed it. Scan it with `audit.py scan dist/index.html`, or at least grep it for the banned list.

Known limits: the script cannot judge tone, only patterns. A string with zero hits can still sound stiff, so still do the read-aloud check.

## Self-check before finishing

- Would a person actually say this out loud to a client? If not, rewrite.
- Did any fact, number or name change? If yes, revert it.
- Read it once for each banned pattern above.

## Output

- When editing files, change the text in place. Do not leave old and new side by side.
- Report a few before/after examples, the audit numbers (before → after), and anything you were unsure about.
