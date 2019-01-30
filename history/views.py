from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from history.models import Artist, Song, Album, Song_Album

def index(request):
  # The dict passed into the tmeplate helps us tell the nav bar where we are
  return render(request, 'history/index.html', {"location": "home"})

# Songs
def songList(request):
  # Long way, using try/except. See the artist functions for using Django's get_list_or_404 and get_object_or_404
  try:
    # By default, Django figures out a database table name by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them.
    songs = Song.objects.raw('SELECT * FROM history_song')
  except Song.DoesNotExist:
    raise Http404("Songs do not exist")

  context = {'song_list': songs, "location": "songs"}
  return render(request, 'history/song_list.html', context)

def songDetail(request, pk):
  print("PK?", pk)
  try:

    # The ORM way:
    song = Song.objects.get(pk=pk)

    # The raw SQL way, for Bangazon sprint #2!:
    # By default, Django figures out a database table name by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them.
    # sql = '''
    #       SELECT * FROM history_song
    #       JOIN history_artist ON history_song.artist_id = history_artist.id
    #       JOIN history_song_album ON history_song.id = history_song_album.song_id
    #       WHERE history_song.id = %s
    #       '''
    # NOTE: To avoid SQL injection attacks, you must use the "params" formatting. The params argument is a list or dictionary of parameters. We use %s placeholders in the query string above for a list of variables ( here we just have a single one: [pk]). We would use %(key)s placeholders for a dictionary (where key is replaced by a dictionary key, of course). Such placeholders will be replaced with parameters from the params argument.
    # song = Song.objects.raw(sql, [pk])[0]  # The [0] is very imprtant!!

  except Song.DoesNotExist:
    raise Http404("Song does not exist")
  context = {'song': song}
  return render(request, 'history/song_detail.html', context)

# helper function used by add and edit song functions
def addSongAlbum(form_albums, song):
  for album_id in form_albums:
    album = Album.objects.get(pk=album_id)
    song_album_pairing = Song_Album.objects.filter(song=song, album=album)
    if song_album_pairing:
      pass
    else:
      Song_Album.objects.create(song=song, album=album)

def songNew(request):
  if request.method == "GET":
    albums = Album.objects.all()
    artists = Artist.objects.all()
    context = {
        "route": "history:song_new",
        "albums": albums,
        "artists": artists
    }
    return render(request, 'history/song_form.html', context)

  if request.method == "POST":
    title = request.POST["title"]
    # assuming artist was submittted from the form as a name. Using an ID is better, when possible, for example if user is selecting from a dropdown list of artists instead of just typing into a text box
    artist_name = request.POST["artist"]
    # Go get an instance of the artist so we cn save it as foreign key on song
    ar = Artist.objects.get(name=artist_name)
    # Longhand way of making Song instance and saving to db:
    new_song = Song(title=title, artist=ar)
    new_song.save()
    print("song added?", new_song.id)

    # Shorthand way makes instance and saves at same time
    # Song.objects.create(title=title, artist=artist)

    # Now, save the album(s) to join table, since song/album is many-to-many
    addSongAlbum(request.POST["albums"], new_song)

    return HttpResponseRedirect(reverse('history:songs'))

def songEdit(request, pk):

  if request.method == "GET":
    song = Song.objects.get(pk=pk)
    albums = Album.objects.all()
    artists = Artist.objects.all()
    print("Song to edit", song.title)
    context = {
        "song": song,
        "albums": albums,
        "artists": artists,
        "route": "history:song_edit",
        "id": song.id,
        "edit": True
    }
    return render(request, 'history/song_form.html', context)

  if request.method == "POST":
    song_to_edit = Song.objects.get(pk=pk)
    print("Song has id?", song_to_edit.id)
    artist = Artist.objects.get(pk=request.POST["artist"])

    song_to_edit.title = request.POST["title"]
    song_to_edit.artist = artist
    song_to_edit.save()

    # Now add new instances of song/album if new albums were added in the edit form.
    # We just call addSongAlbum again, since ait checks for whether a pairing already exists in the db before adding a new instance
    addSongAlbum(request.POST["albums"], song_to_edit)

    return HttpResponseRedirect(reverse('history:song_detail', args=(pk,)))

# Artists
def artistList(request):
  artists = get_list_or_404(Artist)
  return render(request, 'history/artist_list.html', {"artist_list": artists})

def artistDetail(request, artist_id):
  artist = get_object_or_404(Artist, pk=artist_id)
  context = {"artist": artist}

  return render(request, 'history/artist_detail.html', context)

def artistNew(request):
  if request.method == "GET":
    return render(request, 'history/artist_form.html')

  if request.method == "POST":
    req = request.POST
    artist_check = Artist.objects.filter(name=req["artist_name"]).exists()
    if artist_check:
      return render(request, 'history/artist_form.html', {"error": "An artist with that name already exists"})

    new_artist = Artist.objects.create(name=req["artist_name"], birth_date=req["birth_date"], biggest_hit=req["biggest_hit"])
    return HttpResponseRedirect(reverse('history:artist_list'))

# Albums
def albumList(request):
  albums = get_list_or_404(Album)
  return render(request, 'history/album_list.html', {"album_list": albums})

def albumDetail(request, pk):
  album = get_object_or_404(Album, pk=pk)
  context = {"album": album}

  return render(request, 'history/album_detail.html', context)

# TODO Genres
