# Ozzy — A Local-First AI Assistant

Ozzy is a locally run AI assistant that combines a language model — Mistral 7B, running through LM Studio — with live web search via SearXNG. Rather than relying purely on the model's training data, which can be outdated, Ozzy pulls real-time search results and weaves them into its answers. Everything runs entirely on the local machine, so no data leaves to external servers, keeping the whole setup private by design.

## Architecture

- **LLM runtime:** [LM Studio](https://lmstudio.ai/) running a local model (Mistral 7B Instruct v0.3) via its local OpenAI-compatible server
- **Live retrieval:** [SearXNG](https://github.com/searxng/searxng), a self-hosted metasearch engine, running in Docker with its JSON API enabled
- **Glue code:** Python scripts that query SearXNG and feed results into the model's context before it responds

## Problems Encountered and Fixed

- **Silent failures on every question:** a mismatched variable name — `system_prompt` defined in lowercase but referenced as `SYSTEM_PROMPT` elsewhere in the code — caused the assistant to fail silently. Traced and fixed by aligning the casing throughout.
- **File naming issues:** the text editor repeatedly saved Python files under the wrong extension (e.g. `.py.txt` instead of `.py`). Resolved by renaming and saving the files directly through the command line instead of relying on the editor's save dialog.
- **Tool-calling JSON instead of conversation:** an earlier model (Llama 3.1 8B Instruct) was trained for tool use and returned raw function-call-style JSON instead of plain text. Resolved by swapping to Mistral 7B Instruct v0.3, which responds conversationally in this setup.

## Setup Guide

Everything needed to clone this repo and run Ozzy yourself.

### Prerequisites

1. **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (includes WSL2 integration on Windows — enable WSL2 if prompted)
2. **[LM Studio](https://lmstudio.ai/)** — for downloading and running the local model with a chat interface and local API server
3. **Python 3.10+** with `pip`
4. **Git** — to clone this repository

### Step 1: Clone the repo

```bash
git clone https://github.com/<your-username>/Ozzy_Project.git
cd Ozzy_Project
```

### Step 2: Install Python dependencies

```bash
pip install requests
```

*(Dependencies are kept minimal — just `requests` for talking to SearXNG and the local LM Studio server.)*

### Step 3: Set up SearXNG in Docker

**3a. Pull and run SearXNG with a persistent config volume:**

```bash
docker run -d --name searxng -p 8080:8080 -v searxng-config:/etc/searxng searxng/searxng:latest
```

**3b. Enable the JSON API.**

By default, SearXNG only serves HTML. Copy the config file out of the container to edit it:

```bash
docker cp searxng:/etc/searxng/settings.yml ./settings.yml
```

Open `settings.yml` and add (or edit) the `search` section:

```yaml
search:
  formats:
    - html
    - json
```

Copy the edited file back into the container, then restart:

```bash
docker cp ./settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
```

**3c. Verify it's working.**

Open `http://localhost:8080` in a browser — you should see the SearXNG search page. Test the JSON API directly:

```
http://localhost:8080/search?q=test&format=json
```

If that returns JSON search results, the API is live.

### Step 4: Download and run the model in LM Studio

1. Open LM Studio and search for **Mistral 7B Instruct v0.3**
2. Download it and load it in the chat interface
3. Start LM Studio's local server (Developer/Local Server tab) — by default this serves at `http://localhost:1234`

### Step 5: Run Ozzy

```bash
python ozzy_chat.py
```

`ozzy_chat.py` queries SearXNG (via `ask_searxng.py`) for live results relevant to your question, feeds them into the model's context through LM Studio's local server, and returns a conversational answer grounded in current information.

### Repo contents

| File | Purpose |
|---|---|
| `ask_searxng.py` | Queries the local SearXNG JSON API and returns live search results |
| `ozzy_chat.py` | Main chat loop — wires live search into the model's responses via LM Studio's local server |

## What's Next

Ozzy represents the first entry in a growing lineup of local AI tools. Future projects include a coding assistant trained on personal engineering documentation, and a job search assistant that filters listings by role, location, and cost of living. Each new build will expand on the local-first, privacy-focused approach established here.
