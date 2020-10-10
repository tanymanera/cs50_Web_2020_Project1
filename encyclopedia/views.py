from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from markdown2 import markdown

from . import util


def index(request):
    if request.method == 'POST':
        form = queryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            if isinstance(util.get_query(query), str):
                return redirect('show', title=query)
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": util.get_query(query),
                    'form': queryForm()
                })
        else:
            return render(request, 'index', {'form': form})
    # request method is GET
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': queryForm()
    })

def show(request, title):
    entry_page = util.get_entry(title)
    return render(request, "encyclopedia/show.html", {
        'form': queryForm(),
        'title': title,
        'entry_body': markdown(entry_page)
    })

def new_page(request):
    if request.method == 'POST':
        page = NewPageForm(request.POST)
        if page.is_valid():
            title = page.cleaned_data['entry_title']
            text = page.cleaned_data['entry_text']
            if title in util.list_entries():
                return render(request, 'encyclopedia/error_file_exist.html', {
                    'title': title
                })
            else:
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse('show', kwargs={'title': title}))
        else:
            return render(request,'encyclopedia/new_page.html', {
                'new_entry': NewPageForm(),
            })
    # method is GET
    new_entry = NewPageForm()
    return render(request, 'encyclopedia/new_page.html', {
        'new_entry': new_entry
    })

def edit(request, title):
    if request.method == 'POST':
        page = EditPageForm(request.POST)
        if page.is_valid():
            text = page.cleaned_data['entry_text']
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse('show', kwargs={'title': title}))
        else:
            return render(request,'encyclopedia/edit_page.html', {
                'title': title,
                'new_entry': EditPageForm(request.POST),
            })  
    # the method is GET
    entry = {'entry_title': title, 'entry_text': util.get_entry(title)}
    edit_form = EditPageForm(initial=entry)
    return render(request, 'encyclopedia/edit_page.html', {
        'title': title,
        'edit_entry': edit_form
    })

def random(request):
    return HttpResponseRedirect(reverse('show', kwargs={'title': util.a_caso()}))



class queryForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    entry_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    entry_text = forms.CharField(widget=forms.Textarea)

class EditPageForm(forms.Form):
    entry_text = forms.CharField(widget=forms.Textarea)