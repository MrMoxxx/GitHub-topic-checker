# github-topic-checker

A simple multi-threaded Python script to quickly check and filter GitHub topics/tags from a text file.

It sorts topics into 3 categories:
- 🟢 **Active** — topic exists and has public repositories.
- 🟡 **Empty** — topic exists, but currently has 0 repositories.
- 🔴 **Banned** — topic is banned or deleted (HTTP 404).

## Features
- Multi-threaded (fast checking)
- Colorized console UI
- Rate limit prevention
- Automatically saves output into 3 separate text files

## How to use

1. Clone the repo:
   ```bash
   git clone https://github.com/MrMoxxx/github-topic-checker.git
   cd github-topic-checker
