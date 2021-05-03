from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from . import util
import markdown2, re, random


def index(request):
    """
    Returns the list of encyclopedia entries.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getPage(request, title):
    """
    Returns a new page with the content of an encyclopedia entry.
    It uses the markdown module to convert from md format to html.
    """
    md = util.get_entry(title)
    if md == None:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "content": "<h1>Error</h1><p>The requested page was not found.<p>"
        })
    else:
        html = markdown2.markdown(md)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })
"""
def getHtml(md):
    "It was just a try...:"
    head = re.compile('#\s*[a-zA-Z]*')
    title = re.sub(r"#\s*", "", head.match(md).group())
    body = re.sub(r"#\s*[a-zA-Z]*\n*", "", md)
    link = re.findall(r'\[[a-zA-Z]*\]', md)

    if link:
        link = re.sub("\[|\]", "", (re.findall(r'\[[a-zA-Z]*\]', md)).group())
        url = re.sub("\]|\(|\)", "", (re.search(r'\]\(/[a-zA-Z]*/[a-zA-Z]*\)', md)).group())
        body1 = re.sub("\[", "", (re.search(r'[a-zA-Z\s*]*\[', body).group()))
        body2 = re.sub("\)", "", (re.search(r'\)\s*[a-zA-Z\s*]*.', body).group()))
        body = body1+'<a href="'+url+'">'+link+'</a>'+body2

    html = '<h1>'+title+'</h1>'+'<br>'+'<p>'+body+'</p>'
    return html
"""

def search(request):
    """
    Returns the content of an entry based on the user's search or shows
    the possible results based on a partial search.
    """
    entries = util.list_entries()
    query = request.GET.get("q", "")
    filter = []
    for entry in entries:
        if entry.lower() == query.lower():
            return HttpResponseRedirect(reverse("getPage", args=(entry,)))
            break
        else:
            comp = re.search(query.lower(),entry.lower())
            if comp != None:
                filter.append(entry)
    if filter:
        return render(request, "encyclopedia/search.html", {
            "entries": filter
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "content": "<h1>Error</h1><p>The requested page was not found.<p>"
        })

def create(request):
    """
    Creates a new entry on the wiki by means of a POST request which
    comes with a user defined title and contents using md format. If The
    entry already exists it shows an error to the user.
    """
    title = request.POST["title"]
    md = request.POST["info"]
    entries = util.list_entries()
    exist = False

    for entry in entries:
        if entry.lower() == title.lower():
            exist = True

    if exist:
        return render(request, "encyclopedia/entry.html", {
            "title": "Error",
            "content": "<h1>Error</h1><p>There is already an entry on the encyclopedia with that title.<p>",
            "exist": exist
        })
    else:
        f = default_storage.save(f"entries/{title}.md", ContentFile(md))
        return HttpResponseRedirect(reverse("getPage", args=(title,)))

def edit(request, title):
    """
    Gets the information of an entry and pre-pulates the form. User can edit the contents
    and save.
    """
    if request.POST:
        title = request.POST["title"]
        md = request.POST["info"]
        util.save_entry(title,md)
        return HttpResponseRedirect(reverse("getPage", args=(title,)))
    else:
        md = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "md": md
        })

def aleatorio(request):
    """
    Pulls a random entry from the list of entries. It uses the random module from python
    to generate a random number between 0 and the size of the list.
    """
    entries = util.list_entries()
    num = random.randint(0,len(entries)-1)
    entry = entries[num]
    return HttpResponseRedirect(reverse("getPage", args=(entry,)))
