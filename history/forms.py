from django import forms
from .models import Artist, Song, Album

class ArtistForm(forms.ModelForm):

  class Meta:
      model = Artist
      fields = ('name', 'birth_date', 'biggest_hit')


class SongForm(forms.ModelForm):

  class Meta:
      model = Song
      fields = ('title', 'albums', 'artist')


class AlbumForm(forms.ModelForm):
  songs = forms.ModelMultipleChoiceField(queryset=Song.objects.all())

  class Meta:
      model = Album
      fields = ('title', 'year_released', 'songs')
