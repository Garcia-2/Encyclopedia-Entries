import random
from markdown2 import Markdown
from django.shortcuts import render

from . import util


def convert_markdown_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
     return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
   html_content = convert_markdown_to_html(title)
   if html_content == None:
      return render(request, "encyclopedia/error.html",{
         "message": "Entry Does Not Exist"
      })
   else:
      return render(request, "encyclopedia/entry.html", {
         "title": title,
         "content": html_content
      })
def search(request):
   if request.method == "POST":
    entry_search = request.POST['q']
    html_content = convert_markdown_to_html(entry_search)
    if html_content is not None:
       return render(request, "encyclopedia/entry.html", {
            "title": entry_search,
            "content": html_content
        })
    else:
        entries = util.list_entries()
        recommendations = []
        for entry in entries:
            if entry_search.lower() in entry.lower():
                recommendations.append(entry)
        return render(request, "encyclopedia/search.html", {
           "recommendations": recommendations
        })
    
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        existing_titles = util.get_entry(title)
        if existing_titles is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_markdown_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
          
def edit(request):
   if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_markdown_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def rand(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    html_content = convert_markdown_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
    })