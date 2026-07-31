from pathlib import Path
import base64

parts = []
for i in range(1, 5):
    path = Path(f'pika_patch_{i}.b64')
    if not path.exists():
        raise SystemExit(f'Fehlender Patch-Teil: {path}')
    parts.append(path.read_text().strip())

patch_code = base64.b64decode(''.join(parts)).decode('utf-8')
exec(compile(patch_code, 'pikachu_electric_patch.py', 'exec'))

html = Path('index.html').read_text()
required = ['Pikachu', 'Donnerblitz', 'VOLT-TITAN', 'function electricSound', 'function drawPlayer', 'function drawShot']
missing = [item for item in required if item not in html]
if missing:
    raise SystemExit('Fehlende Inhalte: ' + ', '.join(missing))
print('Pikachu-Elektro-Version erfolgreich eingebaut.')
