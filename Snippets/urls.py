from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page,name='home'),
    path('snippets/add', views.add_snippet_page,name='snippet-add'),
    path('snippets/list', views.snippets_page,name='snippets-list'),
    path('snippet/<int:snippet_id>', views.snippet_detail,name='snippet-detail'),
    path('snippet/<int:snippet_id>/delete', views.snippet_delete,name='snippet-delete'),
    path('snippet/<int:snippet_id>/update', views.snippet_update,name='snippet-update'),
    path('show_hidden', views.show_hidden,name='show-hidden'),
    path('hide_hidden', views.hide_hidden,name='hide-hidden'),
    path('login', views.login,name='login'),
    path('logout', views.logout,name='logout'),
    #path('snippet/create', views.snippet_create,name='snippet-create'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
