from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from history.models import Artist, Song, Album, Song_Album, Album_Artist

# Import this to use the direct db connection
from django.db import connection

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
    # song = Song.objects.filter(pk=pk)
    # # You can see how Django turned this into SQL with print song.query, BUT ONLY with a queryset. "get()" returns the object itself
    # print("Song SQL?", song.query)

    # The raw SQL way, for Bangazon sprint #2!:
    # By default, Django figures out a database table name by joining the model’s “app label” – the name you used in manage.py startapp – to the model’s class name, with an underscore between them.
    sql = '''
          SELECT * FROM history_song
          JOIN history_artist ON history_song.artist_id = history_artist.id
          LEFT JOIN history_song_album ON history_song.id = history_song_album.song_id
          WHERE history_song.id = %s
         '''
    # NOTE: To avoid SQL injection attacks, you must use the "params" formatting. The params argument is a list or dictionary of parameters. We use %s placeholders in the query string above for a list of variables ( here we just have a single one: [pk]). We would use %(key)s placeholders for a dictionary (where key is replaced by a dictionary key, of course). Such placeholders will be replaced with parameters from the params argument.
    song = Song.objects.raw(sql, [pk])[0]  # The [0] is very important!!
    print("raw song", song.artist)
  except Song.DoesNotExist:
    raise Http404("Song does not exist")

  context = {'song': song}
  return render(request, 'history/song_detail.html', context)

# helper function used by add and edit song functions
def addSongAlbum(form_albums, song_id):
  for album_id in form_albums:
    print("al id", album_id, "song id", song_id)
    # album = Album.objects.get(pk=album_id)
    # We don't need all the stuff from the query, but raw expects the primary key for some reason, so we'll just get everything with *
    sql = '''
        SELECT * FROM
        history_song_album
        WHERE history_song_album.album_id = %s
        AND history_song_album.song_id = %s
      '''
    song_album_pairing = Song_Album.objects.raw(sql, [album_id, song_id])

    if song_album_pairing:
      pass
    else:
      with connection.cursor() as cursor:
        cursor.execute("INSERT into history_song_album VALUES (%s,%s,%s)", [None, album_id, song_id])

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
    title = request.POST["title"] # This will be a string
    artist = request.POST["artist"] # This will be an id

    # WITH THE ORM
    # Go get an instance of the artist so we can save it as foreign key on song
    # ar = Artist.objects.get(id=artist)
    # Shorthand way makes instance and saves at same time
    # Song.objects.create(title=title, artist=artist)

    # WITH RAW SQL USING DIRECT CONNECTION VIA CURSOR
    with connection.cursor() as cursor:
      cursor.execute("INSERT into history_song VALUES(%s, %s, %s)", [None, title, artist])
      new_song_id = cursor.lastrowid
      print("New song id after adding new song", new_song_id)

      # Now, save the album(s) to join table, since song/album is many-to-many
      addSongAlbum(request.POST.getlist("albums"), new_song_id)

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
    req = request.POST
    with connection.cursor() as cursor:
      song_to_edit = pk
      artist = req["artist"]
      title = req["title"]

      cursor.execute("UPDATE history_song SET artist_id=%s, title=%s WHERE id=%s", [artist, title, song_to_edit])

      # Now add new instances of song/album if new albums were added in the edit form.
      # We just call addSongAlbum again, since it checks for whether a pairing already exists in the db before adding a new instance
      addSongAlbum(request.POST.getlist("albums"), song_to_edit)

    return HttpResponseRedirect(reverse('history:song_detail', args=(pk,)))

# Artists
def artistList(request):
  artists = get_list_or_404(Artist)
  return render(request, 'history/artist_list.html', {"artist_list": artists, "location": "artists"})

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

def albumNew(request):
  artists = Artist.objects.all()
  context = {
      "location": "add_album",
      "artists": artists,
      "route": "history:album_new"
    }

  if request.method == "GET":
    return render(request, 'history/album_form.html', context)

  if request.method == "POST":
    req = request.POST
    with connection.cursor() as cursor:
      album_check = Album.objects.raw("SELECT * FROM history_album WHERE title=%s", [req["title"]])
      if album_check:
        context["error"] = "An album with that title already exists"
        return render(request, 'history/album_form.html', context)

      # new_album = Album.objects.create(title=req["title"], year_released=req["year_released"])
      new_album = cursor.execute("INSERT INTO history_album VALUES (%s, %s, %s)", [None, req["title"], req["year_released"]])

      # If multiple artists are selected, this is how we pull all of them from the query data, with `getlist()`
      artist_id_list = req.getlist("artist")
      if artist_id_list:
        print("Artist", artist_id_list, "Album", cursor.lastrowid)
        album_id = cursor.lastrowid
        for artist_id in artist_id_list:
          cursor.execute("INSERT INTO history_album_artist VALUES (%s, %s, %s)", [None, artist_id, album_id])

    return HttpResponseRedirect(reverse('history:album_list'))


# TODO Genres
