from django.apps import AppConfig
from django.db.models.signals import post_migrate

# This function runs after the database is ready
def create_admin(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Check if 'admin' already exists so we don't create it twice
    if not User.objects.filter(username="admin_edem").exists():
        User.objects.create_superuser("admin_edem", "efoedem@example.com", "Titivate22@$")
        print("Admin user admin_edem created successfully!")

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        # We connect the function to the post_migrate signal
        post_migrate.connect(create_admin, sender=self)