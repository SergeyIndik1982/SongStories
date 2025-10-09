import os, requests, uuid, base64
from django.shortcuts import render
from django.conf import settings
from pathlib import Path

MUSICGPT_ENDPOINT = os.environ.get('MUSICGPT_ENDPOINT', 'https://api.musicgpt.com/v1/generate')

def index(request):
    return render(request, 'index.html')

def _save_file_from_url(url, dest_folder):
    local_filename = str(uuid.uuid4()) + '.mp3'
    local_path = dest_folder / local_filename
    try:
        r = requests.get(url, stream=True, timeout=60)
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return str(local_filename)
    except Exception as e:
        return None

def _save_file_from_base64(b64string, dest_folder):
    local_filename = str(uuid.uuid4()) + '.mp3'
    local_path = dest_folder / local_filename
    try:
        header, data = (b64string.split(',',1) if ',' in b64string else (None, b64string))
        raw = base64.b64decode(data)
        with open(local_path, 'wb') as f:
            f.write(raw)
        return str(local_filename)
    except Exception as e:
        return None

def generate(request):
    audio_file = None
    error = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '').strip()
        api_key = os.environ.get('ZGRKnaE2rH23gBLi8YxWBJydgt9dCNUpVlgQQHDKadgiWnI3U-YlUdJoKUycpjmxaw0JTPiYQsWHntR8zy5s0g')
        if not api_key:
            error = 'MUSICGPT_API_KEY not set in environment.'
        else:
            payload = {
                'prompt': prompt or 'funny short rap about a birthday',
                'length': 'short',
                'format': 'mp3',
                'genre': request.POST.get('genre','rap')
            }
            headers = {'Authorization': f'Bearer {api_key}'}
            try:
                resp = requests.post(MUSICGPT_ENDPOINT, json=payload, headers=headers, timeout=120)
                resp.raise_for_status()
                data = resp.json()
                dest = Path(settings.MEDIA_ROOT)
                dest.mkdir(parents=True, exist_ok=True)
                if isinstance(data, dict) and data.get('audio_url'):
                    saved = _save_file_from_url(data['audio_url'], dest)
                    if saved:
                        audio_file = settings.MEDIA_URL + saved
                    else:
                        error = 'Failed to download audio from provided URL.'
                elif isinstance(data, dict) and data.get('audio_base64'):
                    saved = _save_file_from_base64(data['audio_base64'], dest)
                    if saved:
                        audio_file = settings.MEDIA_URL + saved
                    else:
                        error = 'Failed to decode base64 audio.'
                else:
                    error = 'API did not return audio_url or audio_base64.'
            except Exception as e:
                error = str(e)
    return render(request, 'index.html', {'audio_url': audio_file, 'error': error})
