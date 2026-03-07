import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

# fetch env variables or gets default values
username = os.getenv('DJANGO_ADMIN_USER')
email = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_ADMIN_PASSWORD')

def create_admin():
    if not username or password:
        print("ERROR: DJANGO_ADMIN_USER or DJANGO_ADMIN_PASSWORD not set. Skipping admin creation.")
        return
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}...")
        User.objects.create_superuser(
            username=username, 
            email=email, 
            password=password
        )
        print("Superuser created successfully.")
    else:
        print(f"Admin user '{username}' already exists. No action taken.")

if __name__ == "__main__":
    create_admin()