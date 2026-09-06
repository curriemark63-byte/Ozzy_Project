import requests
from ask_searxng import search_web

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

system_prompt = "You are a helpful, knowledgeable assistant with access to live web search. Answer clearly and concisely, and cite what you find when relevant."

def get_search_context(query, max_results=3):
    """Pull live search results and format them as plain text context."""
    results = search_web(query)
    return results

def ask_Ozzy(user_question):
    context = get_search_context(user_question)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Here's some live search info that might help:\n{context}\n\nQuestion: {user_question}"}
    ]
    response = requests.post(LM_STUDIO_URL, json={
        "model": "mistralai/mistral-7b-instruct-v0.3",
        "messages": messages,
        "temperature": 0.8
    })
    data = response.json()
    if "choices" not in data:
        print("\n[DEBUG] LM Studio returned:", data)
        return "(error - see debug output above)"
    reply = data["choices"][0]["message"]["content"]
    return reply

if __name__ == "__main__":
    while True:
        q = input("\nYou: ")
        if q.lower() in ("quit", "exit"):
            break
        answer = ask_Ozzy(q)
        print(f"\nOzzy: {answer}")