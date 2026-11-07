import os


def on_starting(server):
    """Apply database migrations once, in the master process, before workers boot."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "district306.settings")
    import django
    from django.core.management import call_command

    django.setup()
    call_command("migrate", interactive=False, verbosity=1)
