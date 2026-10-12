# Humanizer

A Claude Code skill that rewrites text so it sounds like a real person wrote it, not an AI or a stiff translation. Works in Indonesian and English.

Good for website and portfolio copy, app UI text, captions, bios, emails and docs.

## Install

Copy the `humanizer` folder into your skills directory:

```bash
git clone https://github.com/saifulveri/humanizer.git
cp -r humanizer/humanizer ~/.claude/skills/
```

## Use

Ask Claude something like "pakai skill humanizer", "biar lebih manusiawi", or "make this sound less like AI". You can also run `/humanizer`.

## Audit

The skill ships with `humanizer/scripts/audit.py` (Python 3, no dependencies). It counts stiff or banned words before and after a rewrite and checks that numbers and names survived:

```bash
python3 ~/.claude/skills/humanizer/scripts/audit.py scan site.html copy.json --out before.json
python3 ~/.claude/skills/humanizer/scripts/audit.py diff before.json after.json
python3 ~/.claude/skills/humanizer/scripts/audit.py facts copy.json
```

See [`humanizer/SKILL.md`](humanizer/SKILL.md) for the full rules.
