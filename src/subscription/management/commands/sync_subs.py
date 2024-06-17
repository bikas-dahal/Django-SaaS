from typing import Any
from django.core.management.base import BaseCommand 


from subscription.models import Subscription

class Command(BaseCommand):
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        print('Hyalo')
        qs = Subscription.objects.filter(active=True)


        for obj in qs:

            sub_perm = obj.groups.all()


            for group in obj.groups.all():
                group.permissions.set(sub_perm)