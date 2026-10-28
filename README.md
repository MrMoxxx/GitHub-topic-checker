# github-topic-checker

A simple multi-threaded Python tool to check and filter GitHub topics/tags from a text file.

It automatically sorts topics into 3 categories:
- 🟢 **Active** — Topic exists and has public repositories.
- 🟡 **Empty** — Topic exists, but currently has 0 repositories.
- 🔴 **Banned** — Topic is banned or deleted (HTTP 404).

## Features
- ⚡ **Multi-threaded** — Fast checking with custom thread pool.
- 🎨 **Clean Console UI** — Colorized status display and progress tracking.
- 🛡️ **Rate-Limit Safe** — Built-in delays to avoid HTTP 429 errors.
- 💾 **Auto-Save** — Instant output generation to separate text files.

## Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/github-topic-checker.git
cd github-topic-checker
```

2. **Install requirements:**
```bash
pip install requests
```

3. **Add your topics to `topics.txt` (one per line):**
```text
python
cheat
hdwaudbwuaydbw
```

4. **Run the script:**
```bash
python checker.py
```

## Output Files

The results will be automatically saved into three separate files:
- `active_topics.txt` — Active topics with existing repositories.
- `empty_topics.txt` — Active topics with 0 repositories.
- `banned_topics.txt` — Banned, deleted, or 404 topics.

## License

MIT
