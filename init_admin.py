import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

# fetch env variables or gets default values
username = os.getenv('DJANGO_ADMIN_USER', 'admin')
email = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_ADMIN_PASSWORD', 'asdfasdf')

if not User.objects.filter(username=username).exists():
    print(f"creating user: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print(f"admin user: {username} already exists.")