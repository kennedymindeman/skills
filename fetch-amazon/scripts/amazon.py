#!/usr/bin/env python3
"""Fetch Amazon product pages and search results with a browser User-Agent.

  amazon.py <url|ASIN> [...]         product summary per argument
  amazon.py --search "terms" [-n N]  top N search hits: title, ASIN, price,
                                     rating, review count, link, sponsored flag
                                     [--min-price D] [--max-price D] [--organic]
  amazon.py --details <url|ASIN>     summary plus feature bullets and spec table
  amazon.py --html <url|ASIN>        raw page HTML on stdout (for grep)
  amazon.py --json ...               JSON instead of text

Amazon returns HTTP 500 to default fetchers; a browser UA gets the real page.
Stdlib only.
"""

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UAS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
]
ASIN_RE = re.compile(r"/(?:dp|gp/product|gp/aw/d|d)/([A-Z0-9]{10})(?:[/?]|$)")
# Amazon's block pages. The Akamai ones return HTTP 200 with a real-looking shell,
# so a page that parses to zero results is a block, not an empty market.
BLOCK_MARKERS = (
    "api-services-support@amazon.com",
    "Type the characters you see",
    "bm-verify",
    "_sec/verify",
)


def asin_of(arg):
    if re.fullmatch(r"[A-Z0-9]{10}", arg):
        return arg
    m = ASIN_RE.search(arg)
    return m.group(1) if m else None


def canonical(asin):
    return f"https://www.amazon.com/dp/{asin}"


def fetch(url):
    last = None
    for ua in UAS:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": ua,
                "Accept": "text/html,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                body = r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            time.sleep(1)
            continue
        hit = next((m for m in BLOCK_MARKERS if m in body), None)
        if hit:
            # Akamai's interstitial ships as HTTP 200, so status alone can't see it.
            last = (
                "captcha" if "amazon.com" in hit or "characters" in hit else "bot check"
            )
            time.sleep(2)
            continue
        return body
    sys.exit(f"fetch failed for {url}: {last}")


def first(pat, s, flags=re.DOTALL):
    m = re.search(pat, s, flags)
    return clean(m.group(1)) if m else None


def clean(t):
    return re.sub(r"\s+", " ", html.unescape(t)).strip() or None


def block(s, elem_id, length=6000):
    i = s.find(f'id="{elem_id}"')
    return s[i : i + length] if i >= 0 else ""


def details(s):
    bullets = [
        clean(b)
        for b in re.findall(
            r'<span class="a-list-item">\s*([^<]+?)\s*</span>',
            block(s, "feature-bullets", 20000),
        )
    ]
    specs = {}
    row = r"<tr[^>]*>\s*<t[hd][^>]*>\s*(?:<span[^>]*>)?\s*([^<]+?)\s*(?:</span>)?\s*</t[hd]>\s*<td[^>]*>\s*(?:<span[^>]*>)?\s*([^<]+?)\s*<"
    for sec, n in (
        ("productOverview_feature_div", 30000),
        ("productDetails_feature_div", 80000),
        ("productDetails_techSpec_section_1", 30000),
    ):
        for k, v in re.findall(row, block(s, sec, n)):
            k, v = clean(k), clean(v)
            if k and v and k not in specs:
                specs[k] = v
    return {"bullets": [b for b in bullets if b], "specs": specs}


def product(arg, want_details=False):
    asin = asin_of(arg)
    if not asin:
        sys.exit(f"no ASIN in {arg}")
    s = fetch(canonical(asin))
    price = None
    for bid in (
        "corePriceDisplay_desktop_feature_div",
        "corePrice_feature_div",
        "corePrice_desktop",
        "price_inside_buybox",
        "buybox",
    ):
        price = first(r'class="a-offscreen">([^<]*)', block(s, bid))
        if price:
            break
    avail = first(r"<span[^>]*>\s*([^<]+?)\s*</span>", block(s, "availability", 1500))
    if 'id="outOfStockBuyBox_feature_div"' in s and not price:
        avail = avail or "Currently unavailable"
    d = details(s) if want_details else {}
    return {
        **d,
        "asin": asin,
        "url": canonical(asin),
        "title": first(r'id="productTitle"[^>]*>([^<]*)', s),
        "brand": first(r'id="bylineInfo"[^>]*>([^<]*)', s),
        "price": price,
        "availability": avail,
        "rating": first(r'id="acrPopover"[^>]*title="([^"]*)"', s),
        "reviews": first(r'id="acrCustomerReviewText"[^>]*aria-label="([^"]*)"', s),
    }


def search(terms, n, lo=None, hi=None, organic=False):
    q = {"k": terms}
    if (lo is not None and lo < 0) or (hi is not None and hi < 0):
        sys.exit("negative price bound; Amazon's p_36 filter can't express it")
    if lo is not None and hi is not None and lo > hi:
        sys.exit(f"--min-price {lo} is above --max-price {hi}; no price can match")
    if lo is not None or hi is not None:
        q["rh"] = (
            f"p_36:{round((lo or 0) * 100)}-{round(hi * 100) if hi is not None else ''}"
        )
    s = fetch("https://www.amazon.com/s?" + urllib.parse.urlencode(q))
    out = []
    parts = re.split(
        r'data-asin="([A-Z0-9]{10})"[^>]*data-component-type="s-search-result"', s
    )
    if len(parts) < 3:
        # A real "nothing matched" page says so; a bot check just omits the cards.
        if "No results for" in s:
            return []
        sys.exit(
            f"search for {terms!r} returned a page with no result cards — Amazon is "
            "throttling this IP (its bot check returns HTTP 200). Wait a minute, or "
            "run from the other machine (ssh mini / ssh laptop)."
        )
    for asin, p in zip(parts[1::2], parts[2::2]):
        sponsored = "Sponsored" in p[:3000]
        if organic and sponsored:
            continue
        title = first(r'<h2[^>]*aria-label="([^"]*)"', p) or first(
            r"<h2[^>]*>.*?<span[^>]*>([^<]+)</span>", p
        )
        out.append(
            {
                "asin": asin,
                "url": canonical(asin),
                "title": re.sub(r"^Sponsored Ad\s*-\s*", "", title) if title else None,
                "price": first(r'class="a-offscreen">([^<]*)', p),
                "rating": first(r'aria-label="([\d.]+ out of 5 stars)', p),
                "reviews": first(r'aria-label="([\d,]+ ratings?)"', p),
                "sponsored": sponsored,
            }
        )
        if len(out) >= n:
            break
    return out


def show(d):
    print(
        f"- [{d.get('title')}]({d['url']}) — {d.get('price') or 'no price'}"
        + (f"; {d['availability']}" if d.get("availability") else "")
        + (f"; {d['rating']}" if d.get("rating") else "")
        + (f" ({d['reviews']})" if d.get("reviews") else "")
        + (" [sponsored]" if d.get("sponsored") else "")
    )
    for b in d.get("bullets", []):
        print(f"    * {b}")
    for k, v in d.get("specs", {}).items():
        print(f"    {k}: {v}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("args", nargs="*")
    ap.add_argument("--search")
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--min-price", type=float)
    ap.add_argument("--max-price", type=float)
    ap.add_argument("--organic", action="store_true", help="drop sponsored hits")
    ap.add_argument("--details", action="store_true")
    ap.add_argument("--html", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.html:
        asin = asin_of(a.args[0])
        sys.stdout.write(fetch(canonical(asin) if asin else a.args[0]))
        sys.exit()
    rows = (
        search(a.search, a.n, a.min_price, a.max_price, a.organic)
        if a.search
        else [product(x, a.details) for x in a.args]
    )
    if a.json:
        print(json.dumps(rows, indent=1))
    else:
        for r in rows:
            show(r)
