import random
from django.shortcuts import render
from django.shortcuts import redirect

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page not found for '{title}'."
        })
    # Assuming util.entry_item() returns a dictionary with the entry content
    content = markdown2.markdown(content)  # Convert Markdown to HTML

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content          
    })

def search(request):
    query = request.GET.get("search_item")

    if query:
        content = util.get_entry(query)
        if content:
            content = markdown2.markdown(content)  # Convert Markdown to HTML
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": content
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
        
def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if title and content:
            # Check if the entry already exists
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": f"An entry with the title '{title}' already exists."
                })
            else:
                # Save the new entry
                util.save_entry(title, content)
                content = markdown2.markdown(content)  # Convert Markdown to HTML
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": content
                })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Title and content cannot be empty."
            })
    
    return render(request, "encyclopedia/new_entry.html")

def edit_entry(request, title):

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            # Save the edited entry
            util.save_entry(title, content)
            content = markdown2.markdown(content)  # Convert Markdown to HTML
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "Content cannot be empty."
            })
    
    # If GET request, load the existing entry for editing
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page not found for '{title}'."
        })
    
    return render(request, "encyclopedia/edit_entry.html", {
        "title": title,
        "content": content
    })

def random_entry(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
    
    random_title = random.choice(entries)
    content = util.get_entry(random_title)
    
    content = markdown2.markdown(content) 
    return render(request, "encyclopedia/entry.html", {
        "title": random_title,
        "content": content
    })
# Note: The util module is assumed to have the following functions: