Ozzy, a local first AI assistant.

Opening section: Ozzy is a locally run AI assistant that combines a language model, Mistral 7B, running through LM Studio, with live web search via SearXNG. Rather than relying purely on the model's training data, which can be outdated, Ozzy pulls real-time search results and weaves them into its answers. Everything runs entirely on the local machine, so there's no data leaving to external servers, keeping the whole setup private by design.

Problems encountered and fixed section: During development, a mismatched variable name, system prompt defined in lowercase but called in uppercase elsewhere in the code, caused silent failures on every question. This was traced and fixed by aligning the casing throughout. File naming issues also came up repeatedly, with the text editor saving Python files under the wrong extension, resolved by renaming through the command line directly.

Closing section, what's next: Ozzy represents the first entry in a growing lineup of local AI tools. Future projects include a coding assistant trained on personal engineering documentation, and a job search assistant that filters listings by role, location, and cost of living. Each new build will expand on the local-first, privacy-focused approach established here.

# Ozzy — Setup Guide

A fully local, privacy-first conversational assistant with live web retrieval. Ozzy runs entirely on-device — no cloud API calls, no data leaving your machine — using a local LLM for conversation and a self-hosted search backend for current information (news, stocks, general queries).

This guide covers everything needed to clone this repo and run Ozzy yourself.

## Architecture

- **LLM runtime:** [LM Studio](https://lmstudio.ai/) running a local model (this build uses Mistral 7B Instruct v0.3) via its local OpenAI-compatible server
- **Live retrieval:** [SearXNG](https://github.com/searxng/searxng), a self-hosted metasearch engine, running in Docker with its JSON API enabled
- **Glue code:** Python scripts that query SearXNG and feed results into the model's context before it responds

The core idea: rather than relying on a model's frozen training data, Ozzy pulls live search results at query time — so it stays current without ever calling an external API or sending data off-device.

## Prerequisites

Before you start, install the following:

1. **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (includes WSL2 integration on Windows)
   - On Windows, make sure WSL2 is enabled. Docker Desktop will prompt you to install it if it isn't already.
2. **[LM Studio](https://lmstudio.ai/)** — for downloading and running the local model with a chat interface and local API server
3. **Python 3.10+** with `pip`
4. **Git** — to clone this repository

## Step 1: Clone the repo

```bash
git clone https://github.com/<your-username>/Ozzy_Project.git
cd Ozzy_Project
```

## Step 2: Install Python dependencies

```bash
pip install requests
```

*(This project keeps dependencies minimal — just the `requests` library for talking to SearXNG and the local LM Studio server.)*

## Step 3: Set up SearXNG in Docker

Ozzy needs a running SearXNG instance with its JSON API enabled. This runs in its own Docker container.

**3a. Pull and run SearXNG with a persistent config volume:**

```bash
docker run -d --name searxng -p 8080:8080 -v searxng-config:/etc/searxng searxng/searxng:latest
```

**3b. Enable the JSON API.**

By default, SearXNG only serves HTML. You need to enable JSON output so scripts can query it programmatically.

Copy the config file out of the container to edit it:

```bash
docker cp searxng:/etc/searxng/settings.yml ./settings.yml
```

Open `settings.yml` and add (or edit) the `search` section to include:

```yaml
search:
  formats:
    - html
    - json
```

Copy the edited file back into the container's volume:

```bash
docker cp ./settings.yml searxng:/etc/searxng/settings.yml
```

Restart the container:

```bash
docker restart searxng
```

**3c. Verify it's working.**

Open `http://localhost:8080` in a browser — you should see the SearXNG search page. Test the JSON API directly:

```
http://localhost:8080/search?q=test&format=json
```

If that returns JSON search results, the API is live.

## Step 4: Download and run the model in LM Studio

1. Open LM Studio and search for **Mistral 7B Instruct v0.3**
2. Download it and load it in the chat interface
3. Start LM Studio's local server (found in the Developer/Local Server tab) — by default this serves at `http://localhost:1234`

*Note: earlier testing with Llama 3.1 8B Instruct hit an issue where the model was trained for tool-calling and returned raw JSON instead of conversational text. Mistral 7B Instruct v0.3 was used instead specifically because it responds in plain conversational text with this setup.*

## Step 5: Run Ozzy

```bash
python ozzy_chat.py
```

`ozzy_chat.py` queries SearXNG (via `ask_searxng.py`) for live results relevant to your question, feeds them into the model's context through LM Studio's local server, and returns a conversational answer grounded in current information.

## Repo contents

| File | Purpose |
|---|---|
| `ask_searxng.py` | Queries the local SearXNG JSON API and returns live search results |
| `ozzy_chat.py` | Main chat loop — wires live search into the model's responses via LM Studio's local server |

## Roadmap (not yet implemented)

This first version focuses on getting a clean, working, fully local retrieval-augmented chatbot running end to end. Planned next steps:

- **Fine-tuning** — training the base model on a defined personality/conversational style, layered on top of the current live-retrieval setup
- **Voice** — integrating a local text-to-speech engine (Piper) for spoken interaction
- **Remote access** — using Tailscale to reach Ozzy securely from a phone, without exposing anything to the public internet

This is intended as the first entry in a growing set of local AI tools, alongside a coding agent (Tank) and a job-search assistant (the Investigator).
