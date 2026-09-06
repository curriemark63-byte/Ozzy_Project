Ozzy, a local first AI assistant.

Opening section: Ozzy is a locally run AI assistant that combines a language model, Mistral 7B, running through LM Studio, with live web search via SearXNG. Rather than relying purely on the model's training data, which can be outdated, Ozzy pulls real-time search results and weaves them into its answers. Everything runs entirely on the local machine, so there's no data leaving to external servers, keeping the whole setup private by design.

Problems encountered and fixed section: During development, a mismatched variable name, system prompt defined in lowercase but called in uppercase elsewhere in the code, caused silent failures on every question. This was traced and fixed by aligning the casing throughout. File naming issues also came up repeatedly, with the text editor saving Python files under the wrong extension, resolved by renaming through the command line directly.

Closing section, what's next: Ozzy represents the first entry in a growing lineup of local AI tools. Future projects include a coding assistant trained on personal engineering documentation, and a job search assistant that filters listings by role, location, and cost of living. Each new build will expand on the local-first, privacy-focused approach established here.

Prerequisites:
Ollama or LM Studio installed, with Mistral 7B pulled/loaded
Docker Desktop installed, with WSL2 enabled (Windows)
Python 3.10+ installed
A local SearXNG instance running via Docker, with the JSON API format enabled in its settings.yml
Setup:
Clone this repository
Install Python dependencies: pip install -r requirements.txt
Start the SearXNG Docker container (see Docker setup notes below, or your own SearXNG config)
Confirm SearXNG's JSON API is responding at your local instance URL
Load Mistral 7B in LM Studio and start its local server
Run python ozzy_chat.py
requirements.txt should list whatever your scripts actually import, at minimum probably requests for the SearXNG calls and whatever library your LM Studio connection uses.

Docker / SearXNG Setup:
Pull and run the SearXNG image with a persistent config volume:
Code
Copy the generated settings.yml out of the container to edit it locally (or edit it directly in the mounted volume).
In settings.yml, add a search: formats: block enabling both html and json, so the API can be queried programmatically:
Code
Restart the container so the config change takes effect.
Confirm it's working by visiting http://localhost:8080 in a browser, then testing the JSON endpoint directly (e.g. http://localhost:8080/search?q=test&format=json).