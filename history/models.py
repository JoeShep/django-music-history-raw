from django.db import models
from django.urls import reverse

class Artist(models.Model):
  name = models.CharField(default="", max_length=100)
  birth_date = models.CharField(default="", max_length=100)
  biggest_hit = models.CharField(default="", max_length=100)

  def __str__(self):
    return self.name

class Album(models.Model):
  title = models.CharField(max_length=100)
  year_released = models.CharField(max_length=4)
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return self.title

class Song(models.Model):
  title = models.CharField(default="", max_length=100)
  albums = models.ManyToManyField(Album, blank=True, through='Song_Album')
  artist = models.ForeignKey(Artist, on_delete=models.CASCADE, )

  def __str__(self):
    return self.title

# Note that wrapping the model reference to this class (Album_Songs) in strings makes them evaluate lazily (after the models have been defined), to avoid 'not defined' errors
class Song_Album(models.Model):
  album = models.ForeignKey(Album, on_delete=models.CASCADE, )
  song = models.ForeignKey(Song, on_delete=models.CASCADE, )

  # This enforces no added duplicates of a song/album relationship, but throws an error when a second pairing tries to be added to the db, so in the view we check the db for an existing pairing and just skip the insert to the db if the paring already exists
  class Meta:
    unique_together = (('album', 'song'),)
