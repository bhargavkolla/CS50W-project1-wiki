from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from . import util
from django import forms
from django.urls import reverse
from random import choice
import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,name):
    return render(request,"encyclopedia/entry.html",{"name":name.capitalize(),"content":markdown2.markdown(util.get_entry(name))})
def search(request):
    listof_entries=util.list_entries()
    entrylist=list()
    if request.method=="POST":
        searchbox=request.POST.get("q")
        if searchbox.capitalize() in listof_entries:
            return HttpResponseRedirect(f"wiki/{searchbox}")
        for entry in listof_entries:
            if searchbox.lower() in entry.lower():
                entrylist.append(entry)
        if entrylist:
            return render(request,"encyclopedia/search.html",{"entrylist":entrylist,"Search":searchbox})
        else:
            return render(request,"encyclopedia/search.html",{"entrylist":entrylist,"Search":searchbox})
    return render(request,"encyclopedia/index.html")
def newpage(request):
    if request.method=="POST":
        title=request.POST.get("title").capitalize()
        content=request.POST.get("content")
        listof_entries=util.list_entries()
        if title in listof_entries:
            return HttpResponse("error,entry name exists")
        else:
            util.save_entry(title,content)
            return render(request,"encyclopedia/newpage.html")
    else:
        return render(request,"encyclopedia/newpage.html")
class editpageform(forms.Form):
    edit_content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','cols':'90'}),label="content")

def edit(request,name):
    form=editpageform(initial={'edit_content':util.get_entry(name)})
    print(util.get_entry(name))
    if request.method=="POST":
        data=editpageform(request.POST)
        if data.is_valid():
            new_data=data.cleaned_data["edit_content"]
            util.save_entry(name,new_data)
            return HttpResponseRedirect(reverse('entry',args=[name]))
    else:
        return render(request,"encyclopedia/edit.html",{"name":name,"form":form})
def random(request):
    name=choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry',args=[name]))