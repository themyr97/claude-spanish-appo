#!/usr/bin/env python3
"""Deployment der Spanisch-App.

Umgeht zwei Fallen, die schon zu kaputten Deployments geführt haben:
  - ARG_MAX: der Request-Body wird in eine Datei geschrieben, nicht als
    Shell-Argument übergeben (sonst schlägt index.html fehl, während
    service-worker.js durchgeht — Version stimmt, Inhalt nicht).
  - CDN-Cache: verifiziert wird über die API, nicht über raw.githubusercontent.

Aufruf:
    GH_TOKEN=... python3 deploy.py <verzeichnis> <version>
z.B.  GH_TOKEN=... python3 deploy.py /home/claude/pwa-export v22
"""
import base64, json, os, subprocess, sys

USER, REPO = 'themyr97', 'claude-spanish-appo'
API = f'https://api.github.com/repos/{USER}/{REPO}/contents'
LIVE = ['index.html', 'service-worker.js', 'README.md', 'LERNSTAND.md']
ARCHIVE = ['index.html', 'manifest.json', 'service-worker.js',
           'icon-192.png', 'icon-512.png']


def curl(args):
    return subprocess.run(['curl', '-s'] + args, capture_output=True, text=True).stdout


def sha(token, path):
    out = curl(['-H', f'Authorization: Bearer {token}',
                '-H', 'Accept: application/vnd.github+json', f'{API}/{path}'])
    try:
        return json.loads(out).get('sha')
    except Exception:
        return None


def put(token, local, remote, msg):
    body = {'message': msg,
            'content': base64.b64encode(open(local, 'rb').read()).decode()}
    s = sha(token, remote)
    if s:
        body['sha'] = s
    with open('/tmp/_deploy_body.json', 'w') as f:
        json.dump(body, f)
    code = subprocess.run(
        ['curl', '-s', '-o', '/tmp/_deploy_resp.json', '-w', '%{http_code}',
         '-X', 'PUT', '-H', f'Authorization: Bearer {token}',
         '-H', 'Accept: application/vnd.github+json', f'{API}/{remote}',
         '-d', '@/tmp/_deploy_body.json'],
        capture_output=True, text=True).stdout.strip()
    ok = code in ('200', '201')
    print(f'  {remote:<28} {code}{"" if ok else "  <-- FEHLGESCHLAGEN"}')
    if not ok:
        print('   ', open('/tmp/_deploy_resp.json').read()[:300])
    return ok


def verify(token, d):
    """Rueckladen ueber die API und byteweise vergleichen."""
    print('\nVerifikation (ueber die API, nicht ueber raw):')
    allok = True
    for name in ['index.html', 'service-worker.js']:
        out = curl(['-H', f'Authorization: Bearer {token}',
                    '-H', 'Accept: application/vnd.github.raw', f'{API}/{name}'])
        local = open(os.path.join(d, name), encoding='utf-8').read()
        same = out == local
        allok &= same
        print(f'  {name:<22} identisch: {"JA" if same else "NEIN"}')
    print('\n  github.io ist aus der Sandbox nicht erreichbar — ob das Handy')
    print('  die neue Version zieht, zeigt nur das Badge in der App.')
    return allok


def main():
    token = os.environ.get('GH_TOKEN')
    if not token:
        sys.exit('GH_TOKEN fehlt. Miro um einen neuen Fine-grained PAT bitten '
                 '(Contents: Read and write, nur dieses Repo).')
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    d, version = sys.argv[1], sys.argv[2]

    # Vorpruefung: stimmen die beiden Versionsmarker ueberein?
    sw = open(os.path.join(d, 'service-worker.js'), encoding='utf-8').read()
    html = open(os.path.join(d, 'index.html'), encoding='utf-8').read()
    if f"APP_VERSION = '{version}'" not in sw:
        sys.exit(f'APP_VERSION in service-worker.js ist nicht {version}.')
    if f'id="versionBadge">{version}<' not in html:
        sys.exit(f'Badge in index.html ist nicht {version}.')
    print(f'Versionsmarker stimmen ueberein: {version}\n')

    msg = f'{version}'
    ok = True
    print('Wurzel (live):')
    for f in LIVE:
        p = os.path.join(d, f)
        if os.path.exists(p):
            ok &= put(token, p, f, msg)
    print(f'\nArchiv {version}/:')
    for f in ARCHIVE:
        p = os.path.join(d, f)
        if os.path.exists(p):
            ok &= put(token, p, f'{version}/{f}', f'Archiv {version}')

    ok &= verify(token, d)
    print('\n' + ('ALLES OK' if ok else 'NICHT VOLLSTAENDIG — oben pruefen'))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
