from typing import Any
from django.core.management.base import BaseCommand, CommandParser 

from subscription import utils as subs_utils



class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--clear-dangling',
            action='store_true',
            default=False
        )
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        print(options)
        subs_utils.clear_dangling_subs()