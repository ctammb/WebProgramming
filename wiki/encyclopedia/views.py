from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Entry not found for '{title}'."
        })
    # Assuming util.entry_item() returns a dictionary with the entry content
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content          
    })

def search(request):
    query = request.GET.get("search_item")

    if query:
        entry = util.get_entry(query)
        if entry:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": entry
            })
        else:
            # If no exact match, search for entries that contain the query
            matching_entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
            if matching_entries:
                return render(request, "encyclopedia/index.html", {
                    "query": query,
                    "entries": matching_entries
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": f"No entries found containing '{query}'."
                })
    else:
        # If no query is provided, redirect to the index page
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
        
