#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from model_api.models import Model

def main():
    """Run administrative tasks."""
    if sys.argv[1] == "runserver":
        Model.get_instance()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technoscape_backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
