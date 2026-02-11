# People Scout

> AI agent that automatically generates person intelligence reports from a single Twitter handle.

## Installation

```bash
git clone <repo-url>
cd people-scout
pip install -e .
```

## Configuration

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

| Variable | Required | Description |
|----------|----------|-------------|
| `SELANET_API_KEY` | Yes | Selanet API key |
| `SELANET_BASE_URL` | Yes | Selanet API base URL |
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `SCOUT_GEMINI_MODEL` | No | Gemini model (default: `gemini-2.5-flash`) |
| `SCOUT_DEFAULT_LANG` | No | Default report language (default: `ko`) |

## CLI Usage

```bash
# Basic analysis
people-scout @cz_binance

# English report + JSON/Markdown output
people-scout @cz_binance --lang en --output console,json,markdown

# Run without installing
python -m people_scout @cz_binance -o console
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--lang` | `-l` | ko | Report language (`ko`, `en`) |
| `--output` | `-o` | console | Output formats (comma-separated: `console`, `json`, `markdown`) |
| `--post-count` | `-p` | 100 | Number of posts to collect |
| `--output-dir` | | `.` | Directory for file output |

## SDK Usage

```python
from people_scout import PeopleScout

# Auto-load from environment variables
scout = PeopleScout()

# Or pass keys directly
scout = PeopleScout(
    selanet_api_key="...",
    gemini_api_key="...",
    selanet_base_url="https://...",
)

# Run analysis
result = scout.analyze("@cz_binance", lang="ko")

# Access results
print(result.summary)
print(result.recent_interests)
print(result.communication_style)
print(result.conversation_entry_points)

# Save to file
result.to_json("report.json")
result.to_markdown("report.md")
```

## Report Contents

| Field | Description |
|-------|-------------|
| **summary** | 2-3 sentence person summary |
| **recent_interests** | Recent interests (topic, frequency, sentiment) |
| **communication_style** | Communication style (tone, frequency, active hours) |
| **conversation_entry_points** | Suggested conversation topics (3-5) |

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
