from django.urls import path
from . import views

app_name = 'history'
urlpatterns = [
    path('', views.index, name='index'),
    path('artists/<int:artist_id>/', views.artistDetail, name='artist_detail'),
    path('songs/', views.songList, name='songs'),
    path('songs/add', views.songNew, name='song_new'),
    path('songs/<int:pk>/', views.songDetail, name='song_detail'),
    path('songs/<int:pk>/edit', views.songEdit, name='song_edit'),

    # path('artists/', views.ArtistListView.as_view(), name='artists'),
    # path('artists/add/', views.ArtistFormView.as_view(), name='artist_form'),
    # path('songs/<int:pk>/edit', views.SongEditView.as_view(), name='song_edit'),
    # path('artists/add/', views.ArtistFormView.as_view(), name='artist_form'),
    # path('albums/', views.AlbumListView.as_view(), name='albums'),
    # path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    # path('albums/add/', views.AlbumFormView.as_view(), name='album_form'),
    # path('albums/<int:pk>/edit', views.AlbumEditView.as_view(), name='album_edit'),
]
