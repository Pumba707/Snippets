from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.form import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
            form.save()
            return redirect('snippets-list')
        
        print('non valid form')
        return render(request, 'pages/add_snippet.html', {'form':form})



def snippets_page(request):

    snippets = Snippet.objects.all()

    context = {
        'pagename': 'Просмотр сниппетов',
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

        invLANGS = {
            'Python': 'py',
            'JavaScript': 'js',
            'C++': 'cpp',
        }

        form = SnippetForm( 
            {
                'name': snippet.name,
                'lang': invLANGS[snippet.lang],
                'code': snippet.code 
            } )
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form,
        }
        return render(request, 'pages/upd_snippet.html', context)

    if request.method == 'POST':

        LANGS = {
            'py': 'Python',
            'js': 'JavaScript',
            'cpp':'C++',
        }

        form = SnippetForm(request.POST)
        if form.is_valid():

            snippet = Snippet.objects.get(id=snippet_id)
            print(form.data['name'])
            snippet.name = form.data['name']
            snippet.lang = LANGS[form.data['lang']]
            snippet.code = form.data['code']
            snippet.save()

            return redirect('snippets-list')
        
        return render(request, 'pages/upd_snippet.html', {'form':form})




