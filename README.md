Ozzy, a local first AI assistant.

Opening section: Ozzy is a locally run AI assistant that combines a language model, Mistral 7B, running through LM Studio, with live web search via SearXNG. Rather than relying purely on the model's training data, which can be outdated, Ozzy pulls real-time search results and weaves them into its answers. Everything runs entirely on the local machine, so there's no data leaving to external servers, keeping the whole setup private by design.

Problems encountered and fixed section: During development, a mismatched variable name, system prompt defined in lowercase but called in uppercase elsewhere in the code, caused silent failures on every question. This was traced and fixed by aligning the casing throughout. File naming issues also came up repeatedly, with the text editor saving Python files under the wrong extension, resolved by renaming through the command line directly.

Closing section, what's next: Ozzy represents the first entry in a growing lineup of local AI tools. Future projects include a coding assistant trained on personal engineering documentation, and a job search assistant that filters listings by role, location, and cost of living. Each new build will expand on the local-first, privacy-focused approach established here.

