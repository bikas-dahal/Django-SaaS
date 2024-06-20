from typing import Any
from django.core.management.base import BaseCommand 

from subscription import utils as subs_utils

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        subs_utils.sync_subs_group_permissions()
        