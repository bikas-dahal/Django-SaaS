import helpers

from django.conf  import settings

from typing import Any 
from django.core.management.base import BaseCommand 


STATICFILES_VENDOR_DIR = getattr(
    settings, 'STATICFILES_VENDOR_DIRS'
)


VENDOR_STATICFILES = {
    'flowbite.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css',
    'flowbite.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js',

}

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Downloading vendor static files,!!!')
        completed_urls = []

        for filename, url in VENDOR_STATICFILES.items():
            outpath = STATICFILES_VENDOR_DIR / filename
            download_status = helpers.download_file(url, outpath)
            if download_status:
                completed_urls.append(url)
            else:
                self.stderr.write(f'Error while downloading {url}')

        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS('All vendor static files downloaded successfully')
            )
        else:
            self.stderr.write(
                self.style.ERROR('Some files failed to download')
            )