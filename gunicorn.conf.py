import os


def on_starting(server):
    """Apply database migrations once, in the master process, before workers boot."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "district306.settings")
    import django
    from django.core.management import call_command

    django.setup()
    call_command("migrate", interactive=False, verbosity=1)

    # Create the admin user from env vars if it does not exist yet.
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    if username and password:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
                password=password,
            )
