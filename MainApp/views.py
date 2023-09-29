from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.form import SnippetForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required
def add_snippet_page(request):

    if request.method == 'GET':
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form,
        }
        return render(request, 'pages/add_snippet.html', context)
    
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            #form.save()
            return redirect('snippets-list')
        
        print('non valid form')
        return render(request, 'pages/add_snippet.html', {'form':form})



def snippets_page(request):

    snippets = Snippet.objects.all()

    ShowHidden = request.session.get("show_hidden", False)

    context = {
        'pagename': 'Просмотр сниппетов',
        'ShowHidden': ShowHidden,
        'snippets': snippets,
    }



    return render(request, 'pages/view_snippets.html', context)



def snippet_detail(request, snippet_id):

    snippet = Snippet.objects.get(id=snippet_id)

    context = {
        'pagename': 'Просмотр сниппета',
        'snippet': snippet,
    }

    return render(request, 'pages/snippet_detail.html', context)

def snippet_create(request):

    if request.method == 'POST':
        name = request.POST['name']
        lang = request.POST['lang']
        code = request.POST['code']

        snippet = Snippet(name=name, lang=lang, code=code)
        snippet.save()

        return redirect('snippets-list')

def snippet_delete(request, snippet_id):

    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()

    return redirect('snippets-list')
    #return render(request, 'pages/snippet_detail.html', context)

def snippet_update(request, snippet_id):

    if request.method == 'GET':

        snippet = Snippet.objects.get(id=snippet_id)

        form = SnippetForm( 
            {
                'name': snippet.name,
                'lang': snippet.lang,
                'hidden': snippet.hidden,
                'code': snippet.code 
            } )
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form,
        }
        return render(request, 'pages/upd_snippet.html', context)

    if request.method == 'POST':

        form = SnippetForm(request.POST)
        if form.is_valid():

            snippet = Snippet.objects.get(id=snippet_id)
            snippet.name = form.data['name']
            snippet.lang = form.data['lang']
            if form.data.get('hidden') == 'on':
                snippet.hidden = True
            else:
                snippet.hidden = False
            snippet.code = form.data['code']
            snippet.save()

            return redirect('snippets-list')
        
        return render(request, 'pages/upd_snippet.html', {'form':form})



def show_hidden(request):
    request.session["show_hidden"] = True

    return redirect('snippets-list')



def hide_hidden(request):
    request.session["show_hidden"] = False

    return redirect('snippets-list')



def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        user = auth.authenticate(request,username=username,password=password)

        if user is not None:
            auth.login(request,user)
        else:
            pass

    return redirect('home')



def logout(request):
    auth.logout(request)

    return redirect('home')


