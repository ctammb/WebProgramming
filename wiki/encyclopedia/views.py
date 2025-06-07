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
