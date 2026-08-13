import urllib.request, json, urllib.parse, time

MIRROR = 'https://netease-cloud-music-api-five-tau.vercel.app'

def search(singer, name, retries=5):
    s = singer + ' ' + name
    for _ in range(retries):
        try:
            url = f'{MIRROR}/search?keywords={urllib.parse.quote(s)}&limit=12&type=1'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://music.163.com/'})
            j = json.loads(urllib.request.urlopen(req, timeout=12).read().decode('utf-8', 'replace'))
            for song in j.get('result', {}).get('songs', []):
                arts = '/'.join(a['name'] for a in song.get('artists', []))
                dur = song.get('duration', 0)
                if singer in arts and name in song['name'] and dur > 60000:
                    return song['id'], song['name'], arts, dur
        except Exception:
            pass
        time.sleep(1)
    return None

def inj_url(idv):
    url = f'https://api.injahow.cn/meting/?server=netease&type=url&id={idv}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Origin': 'https://x'})
    r = urllib.request.urlopen(req, timeout=15)
    return r.status, len(r.read())

def inj_lrc(idv):
    url = f'https://api.injahow.cn/meting/?server=netease&type=lrc&id={idv}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return len(urllib.request.urlopen(req, timeout=12).read())

songs = [
    ('颜人中', ['晚安', '夏天', '有些', '留白', '夏夜最后的烟火', '你想要的', '我只能离开', '慢慢']),
    ('张新成', ['莎士比哑', '第57次取消发送', '我也不在', '晚安星光冻', '是你没选我啊', '晚风', '靠近我', '等你擦肩']),
]
result = {}
for singer, names in songs:
    result[singer] = []
    print('###', singer)
    for name in names:
        r = search(singer, name)
        if r:
            sid, rn, arts, dur = r
            try:
                st, sz = inj_url(sid)
            except Exception as e:
                st, sz = 'ERR', str(e)[:40]
            try:
                ll = inj_lrc(sid)
            except Exception:
                ll = 0
            ok = (st == 200 and isinstance(sz, int) and sz > 2000000 and ll > 200)
            print(f'  {name}: id={sid} "{rn}" {arts} dur={dur//1000}s mp3={sz}B lrc={ll} {"OK" if ok else "XX"}')
            if ok:
                result[singer].append({'name': name, 'id': sid})
        else:
            print(f'  {name}: NOT FOUND')
        time.sleep(0.6)

print('\nJSON_START')
print(json.dumps(result, ensure_ascii=False))
print('JSON_END')
