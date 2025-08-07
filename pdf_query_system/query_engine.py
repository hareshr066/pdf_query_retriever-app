from db import fetch_all_documents

def search_documents(query):
    results = []
    for doc in fetch_all_documents():
        if query.lower() in doc["content"].lower():
            results.append(doc["filename"])
    return results
