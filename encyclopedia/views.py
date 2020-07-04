from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from markdown2 import Markdown

import random

from . import util, models


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_page(request, page):
    markdownPage = util.get_entry(page)

    if not markdownPage:
        return render(request, "encyclopedia/wiki_error.html", {
            "page": page
        })

    markdownConverted = Markdown().convert(markdownPage)

    return render(request, "encyclopedia/wiki_page.html", {
        "title": page,
        "markdownConverted": markdownConverted
    })

def search(request):
    allEntries = util.list_entries()

    query = request.GET['q']

    matches = []

    for entry in allEntries:
        #using .casefold() because of unicode
        #https://stackoverflow.com/a/45745761/12528799

        if query.casefold() == entry.casefold():
            return HttpResponseRedirect(f"wiki/{query}")

        if query.casefold() in entry.casefold():
            matches.append(entry)

    if not matches: 
        return render(request, "encyclopedia/wiki_error.html", {
            "page": query
        })

    if len(matches) == 1:
        return HttpResponseRedirect(f"wiki/{matches[0]}")

    return render(request, "encyclopedia/results.html", {
            "query": query,
            "matches": matches
        })

def new_page(request):
    form = models.PageForm()

    if request.method == "POST":
        form = models.PageForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Invalid form')

        elif util.get_entry(form.cleaned_data['title']):
            messages.error(request, 'There is already an entry with this title')

        else:
            util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])

            return HttpResponseRedirect(f"wiki/{form.cleaned_data['title']}")
        
    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })

def edit(request, page):
    if request.method == "POST":
        form = models.PageForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'Invalid form')

        util.save_entry(form.cleaned_data['title'], form.cleaned_data['content'])

        return HttpResponseRedirect(f"/wiki/{page}")

    content = util.get_entry(page)

    if not content:
        return render(request, "encyclopedia/wiki_error.html", {
            "page": page
        })

    form = models.PageForm(initial={
        'title': page.capitalize(),
        'content': content
    })

    return render(request, "encyclopedia/edit.html", {
        "title": page.capitalize(),
        "form": form
    })

def random_page(request):
    page = random.choice(util.list_entries())

    return HttpResponseRedirect(f"/wiki/{page}")
