from django.core.management.base import BaseCommand
from django_seed import Seed
import random
seeder = Seed.seeder()
from history.models import *

# execute this file directly with python manage.py seeder.py

class Command(BaseCommand):
  def handle(self, *args, **options):
    adjectives = ["Absorbing", "Adorable", "Adventurous","Appealing",
    "Artistic","Athletic","Attractive","Bold","Breathtaking","Bright","Busy","Calm","Capable",
    "Caring","Casual", "Charming","Cheerful","Chic","Classic","Clever","Collaborative",
    "Colorful","Comfortable","Conservative","Contemporary","Convenient",
    "Cool","Creative","Custom","Daring","Dashing","Dazzling",
    "Delicate","Delightful","Detailed","Dramatic","Dry","Dynamic",
    "Earthy","Eccentric","Efficient","Elegant", "Elevated",
    "Enchanting","Endearing",'Energetic',"Ethereal","Excellent",
    "Exciting","Exuberant","Fabulous","Familiar","Fancy","Fantastic","Fashionable",
    "Festive","Fierce","Flirty","Formal","Fresh","Friendly","Fun",
    "Functional","Futuristic","Glamorous","Graceful","Hip",
    "Historic","Honorable","Impressive","Industrial","Informal",
    "Innovative","Inspiring","Intense","Inviting","Lively",
    "Lush","Majestic","Modern","Natural","Nautical","Nifty",
    "Noisy","Nostalgic","Organic","Playful","Pleasant","Powerful",
    "Quirky","Relaxing","Reliable","Retro","Revolutionary",
    "Ritzy","Romantic","Royal","Rustic","Scholarly", "Secure",
    "Serious", "Silly","Sleek","Smart","Soothing","Sophisticated",
    "Stable","Stimulating","Striking","Swanky","Tasteful",
    "Tranquil","Urban","Versatile","Vintage","Whimsical"]

    things = [
        "Alarm clock", "Armoire", "Backpack", "Bedding", "Bedspread", "Blankets", "Blinds", "Bookcase", "Books", "Broom", "Brush", "Bucket", "Calendar", "Candles", "Carpet", "Chair", "Chairs", "China", "Clock", "Coffee table", "Comb", "Comforter", "Computer", "Containers", "Couch", "Credenza", "Cup", "Curtains", "Cushions", "Desk", "Dish towel", "Dishwasher", "Door stop", "Drapes", "Drill", "Dryer", "Dust pan", "Duvet", "Extension cord", "Fan", "Figurine", "Fire extinguisher", "Flashlight", "Flatware", "Flowers", "Forks", "Furnace", "Games", "Glasses", "Hammer", "Heater", 'Houseplant', "IPhone", "IPod", "Iron", "Ironing board", "Jewelry", "Knives", "Lamp", "Microwave", "Mop", "Napkins", "Pans", "Pants", "Paper", "Pen", "Pencil", "Piano", "Pillows", "Pitcher", "Plants", "Plastic plates", "Pliers", "Pots", "Radio", "Rags", "Refrigerator", "Rug", "Saw", "Scissors", "Screw driver", "Shirt", "Shoes", "Smoke detector", "Sneakers", "Socks", "Sofa", "Speakers", "Spoons", "Suitcase", "Telephone", "Toaster", "Toilet paper", "Toothbrush", "Toothpaste", "Towels", "TV", "Vacuum", "Vase"
    ]

    # Add artists first, so we can assign them to some songs
    # TODO: FInish this
    # seeder.add_entity(Artist, 10, {
    #     "artist": lambda x: random.choice(list(artists)),
    #     "title": lambda x: f"{seeder.faker.word(ext_word_list=adjectives)} {seeder.faker.word(ext_word_list=things)}"
    # })

    artists = Artist.objects.all()
    # To save an artist for a song, below, we pull one random artist from the query set after it's been converted to a list. Won't work directly on the QuerySet.
    seeder.add_entity(Song, 5, {
        "artist": lambda x: random.choice(list(artists)),
        "title": lambda x: f"{seeder.faker.word(ext_word_list=adjectives)} {seeder.faker.word(ext_word_list=things)}"
    })
    seeder.execute()
