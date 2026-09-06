import requests

def search_web(query, num_results=5):
    url = "http://localhost:8080/search"
    params = {"q": query, "format": "json"}
    response = requests.get(url, params=params)
    data = response.json()
    results = []
    for item in data.get("results", [])[:num_results]:
        title = item.get("title")
        content = item.get("content")
        link = item.get("url")
        results.append(title + ": " + content + " (" + link + ")")
    return "\n".join(results)

if __name__ == "__main__":
    query = input("Search query: ")
    print(search_web(query))
