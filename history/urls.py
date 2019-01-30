from django.urls import path
from . import views

app_name = 'history'
urlpatterns = [
    # home
    path('', views.index, name='index'),
    # artists
    path('artists/', views.artistList, name='artist_list'),
    path('artists/<int:artist_id>/', views.artistDetail, name='artist_detail'),
    path('artists/add/', views.artistNew, name='artist_new'),
    # path('artists/<int:pk>/edit', views.artistEdit, name='artist_edit'),
    # albums
    path('albums/', views.albumList, name='album_list'),
    path('albums/<int:pk>/', views.albumDetail, name='album_detail'),
    # path('albums/add/', views.AlbumFormView.as_view(), name='album_form'),
    # path('albums/<int:pk>/edit', views.AlbumEditView.as_view(), name='album_edit'),
    # songs
    path('songs/', views.songList, name='songs'),
    path('songs/add', views.songNew, name='song_new'),
    path('songs/<int:pk>/edit', views.songEdit, name='song_edit'),
    path('songs/<int:pk>/', views.songDetail, name='song_detail'),
]
