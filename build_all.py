import urllib.request, json, urllib.parse, time

MIRROR = 'https://netease-cloud-music-api-five-tau.vercel.app'

def search_songs(kw, limit=80):
    url = f'{MIRROR}/search?keywords={urllib.parse.quote(kw)}&limit={limit}&type=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://music.163.com/'})
    j = json.loads(urllib.request.urlopen(req, timeout=12).read().decode('utf-8', 'replace'))
    return j.get('result', {}).get('songs', [])

def inj_url(idv):
    url = f'https://api.injahow.cn/meting/?server=netease&type=url&id={idv}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=15)
    return r.status, len(r.read())

def inj_lrc(idv):
    url = f'https://api.injahow.cn/meting/?server=netease&type=lrc&id={idv}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return len(urllib.request.urlopen(req, timeout=12).read())

for singer in ['颜人中', '张新成']:
    print('###', singer)
    songs = search_songs(singer, 80)
    avail = []
    seen = set()
    for s in songs:
        arts = '/'.join(a['name'] for a in s.get('artists', []))
        if singer not in arts:
            continue
        sid = s['id']
        name = s['name']
        dur = s.get('duration', 0)
        if dur < 60000 or sid in seen:
            continue
        seen.add(sid)
        try:
            st, sz = inj_url(sid)
        except Exception:
            st, sz = 0, 0
        try:
            ll = inj_lrc(sid)
        except Exception:
            ll = 0
        ok = st == 200 and isinstance(sz, int) and sz > 2000000 and ll > 200
        mark = 'OK' if ok else ('FRAG' if sz < 2000000 else '')
        print(f'  id={sid} "{name}" dur={dur//1000}s mp3={sz}B lrc={ll} {mark}')
        if ok:
            avail.append((name, sid))
        time.sleep(0.35)
    print(f'  >>> AVAILABLE({len(avail)}):', avail)
    time.sleep(1)
