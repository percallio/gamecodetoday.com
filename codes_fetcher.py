#!/usr/bin/env python3
"""主站② 日更管线：每游戏源 URL 配置化→抓源→抽码（弱模型或正则）→双源对账
→刷新码页表格+last-checked→（上线后）push。staging 期手动跑，上线后 daemon 实例 2 每日调用。

config: codes_sources.json
{
  "ragdoll-mma-codes": {
    "game": "Ragdoll MMA (Roblox)",
    "sources": [
      {"name": "IGN", "url": "https://www.ign.com/wikis/ragdoll-mma-roblox/Ragdoll_MMA_Codes"},
      {"name": "togame.io", "url": "https://togame.io/b/ragdoll-mma-codes-roblox/"}
    ]
  }
}
"""
import json, os, re, sys, datetime, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
CFG = f'{BASE}/codes_sources.json'
TODAY = datetime.date.today().strftime('%B %d, %Y')

UA = {'User-Agent': 'Mozilla/5.0 Chrome/131'}

def fetch(url):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f'  fetch fail {url[:60]}: {e}')
        return ''

def extract_codes(html):
    """正则先手（码=4-20 位大写字母数字串）；弱模型通道预留（gemma_worker --task codes）"""
    text = re.sub(r'<script.*?</script>', ' ', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    codes = {}
    for i, l in enumerate(lines):
        if re.match(r'^[A-Z0-9_\-]{4,20}$', l):
            ctx = ' '.join(lines[max(0, i-1):i+2])[:100]
            if l not in codes: codes[l] = ctx
    # 源页更新标记
    upd = ''
    m = re.search(r'(?:last updated|updated)\s*(?:on\s*)?([A-Z][a-z]+ \d{1,2}, \d{4})', html)
    if m: upd = m.group(1)
    return codes, upd

def refresh_page(slug, game, sources):
    per_src = []
    for s in sources:
        h = fetch(s['url'])
        if not h: continue
        codes, upd = extract_codes(h)
        per_src.append((s['name'], codes, upd))
        print(f'  {s["name"]}: {len(codes)} 码 {upd}')
    if not per_src:
        print(f'  {slug}: 无源可读，页不改'); return
    # 双源对账
    working, single = {}, {}
    for name, codes, upd in per_src:
        for c in codes:
            if c in working: continue
            hit_other = any(c in o[1] for o in per_src if o[0] != name)
            (working if hit_other else single)[c] = (name, upd)
    print(f'  {slug}: 双源 {len(working)} / 单源 {len(single)}')
    # 刷新页面表格+头信息（staging 期：打印 diff 摘要，上线期：写盘+git）
    fp = f'{BASE}/{slug}/index.html'
    if not os.path.exists(fp):
        print(f'  页不存在: {slug}（先由生产批次建页）'); return
    h = open(fp, encoding='utf-8').read()
    new_head = f'Last checked: {TODAY}'
    h = re.sub(r'Last checked: [A-Z][a-z]+ \d{1,2}, \d{4}', new_head, h)
    open(fp, 'w', encoding='utf-8').write(h)
    print(f'  页已刷 last-checked → {TODAY}（表格行刷新=上线期接弱模型对账后写）')

def main():
    if not os.path.exists(CFG):
        print('codes_sources.json 未配置（生产批次建页时同步写）'); return
    cfg = json.load(open(CFG))
    for slug, spec in cfg.items():
        print(f'[{slug}] {spec.get("game","")}')
        refresh_page(slug, spec.get('game'), spec.get('sources', []))
    print('codes_fetcher 完成')

if __name__ == '__main__':
    main()
