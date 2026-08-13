import urllib.request, json, urllib.parse, ssl, re, time
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

def fetch(url, headers, timeout=20, retries=3):
    last=None
    for _ in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout, context=ctx).read().decode('utf-8','replace')
        except Exception as e:
            last=e; time.sleep(2)
    raise last

def js_str(s):
    s = s.replace('\\','\\\\').replace("'","\\'").replace('\n',' ').replace('\r',' ').strip()
    return re.sub(r'\s+',' ', s)

# ---- 微博热搜 top 12 ----
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36','Referer':'https://weibo.com/','Accept':'application/json'}
b=fetch('https://weibo.com/ajax/side/hotSearch', H)
items=json.loads(b).get('data',{}).get('realtime',[])
wb=[]; seen=set()
for it in items:
    w=it.get('word','').strip()
    if not w or w in seen: continue
    seen.add(w)
    url='https://s.weibo.com/weibo?q='+urllib.parse.quote(w)
    wb.append("  {title:'%s', url:'%s', src:'微博热搜'}" % (js_str(w), url))
    if len(wb)>=12: break
print('微博热搜:', len(wb))

# ---- 百度热榜 top 10（本周热点）----
H2={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36','Accept':'text/html'}
b=fetch('https://top.baidu.com/board?tab=realtime', H2)
words=re.findall(r'"word":"([^"]+)"', b)
hot=[]; seen2=set()
for w in words:
    if len(hot)>=10: break
    if len(w)<4 or w in seen2: continue
    seen2.add(w)
    url='https://www.baidu.com/s?wd='+urllib.parse.quote(w)
    hot.append("  {title:'%s', url:'%s', src:'热门'}" % (js_str(w), url))
print('百度热榜:', len(hot))

with open('news_extra.js','w',encoding='utf-8') as f:
    f.write('\n'.join(wb+hot))
print('=== 微博热搜预览 ===')
for x in wb[:4]: print(x)
print('=== 百度热榜预览 ===')
for x in hot[:4]: print(x)
