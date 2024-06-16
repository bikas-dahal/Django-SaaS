import requests 
from pathlib import Path 

def download_file(url: str, dest: Path, parent_mkdir:bool = True):
    if not isinstance(dest, Path):
        raise ValueError(f'{dest} must be valid path')
    
    if parent_mkdir:
        dest.parent.mkdir(parents=True, exist_ok = True)

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        dest.write_bytes(r.content)
        return True 
    except Exception as e:
        print(f'Error while downloading {url}: {e}')
        return False



    #     if r.status_code == 200:
    #         with open(dest, 'wb') as f:
    #             for chunk in r:
    #                 f.write(chunk)
    #     else:
    #         raise Exception(f'Status code {r.status_code} while downloading {url}')
    # except Exception as e:
    #     raise Exception(f'Error while downloading {url}:
