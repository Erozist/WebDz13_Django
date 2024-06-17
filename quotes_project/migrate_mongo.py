import os
import django
import pymongo
from django.conf import settings
from dateutil.parser import parse

# Ініціалізація Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()

from quotes.models import Author, Quote, Tag
from django.contrib.auth.models import User

# Завантаження MongoDB
client = pymongo.MongoClient(f"mongodb+srv://{os.environ.get('MONGO_USERNAME')}:{os.environ.get('MONGO_PASSWORD')}@cluster0.pubk7cp.mongodb.net")
db = client.quotes_db

# Отримання користувача для поля created_by
default_user = User.objects.first()
if not default_user:
    raise ValueError("No user found in the database. Please create a user before running this script.")

# Завантаження авторів
mongo_authors = db.authors.find()
for mongo_author in mongo_authors:
    born_date_str = mongo_author.get('born_date')
    try:
        born_date = parse(born_date_str).date() if born_date_str else None
    except ValueError:
        print(f"Skipping author {mongo_author['fullname']} due to invalid born_date format")
        continue
    
    if not born_date:
        print(f"Skipping author {mongo_author['fullname']} due to missing born_date")
        continue  # Пропускаємо авторів з відсутньою датою народження
    
    Author.objects.get_or_create(
        fullname=mongo_author['fullname'],
        born_date=born_date,
        born_location=mongo_author['born_location'],
        description=mongo_author['description']
    )
print("Автори успішно завантажені.")

# Завантаження цитат
mongo_quotes = db.quotes.find()
for mongo_quote in mongo_quotes:
    try:
        author = Author.objects.get(fullname=mongo_quote['author'])
    except Author.DoesNotExist:
        print(f"Skipping quote '{mongo_quote['quote']}' because author '{mongo_quote['author']}' does not exist")
        continue  # Пропускаємо цитати, для яких не знайдено автора

    # Створення тегів та зв'язків з цитатами
    tags = []
    for tag_name in mongo_quote['tags']:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        tags.append(tag)
    
    quote, created = Quote.objects.get_or_create(
        quote=mongo_quote['quote'],
        author=author,
        created_by=default_user  # Використання існуючого користувача
    )
    quote.tags.set(tags)
    quote.save()
print("Цитати успішно завантажені.")
