---
name: fetch-amazon
description: Reads Amazon product pages and search results that WebFetch and plain curl can't (Amazon answers them with HTTP 500). Use when handed an amazon.com URL or ASIN, when searching Amazon by keyword for candidate products, when recommending or verifying a purchase link, when a price, availability, spec, or rating on Amazon is needed, when comparing what's in the user's cart against alternatives, and when writing a brief that sends a subagent at Amazon.
---

Amazon is reachable; the fetch tools just don't send a browser User-Agent, so they get a 500 that looks like a block. The script here sends one and parses the page. Prefer it over `WebFetch` for every amazon.com lookup, and hand its canonical `https://www.amazon.com/dp/ASIN` link to the user instead of a tracking-laden one.

```sh
S=~/.claude/skills/fetch-amazon/scripts/amazon.py
python3 $S <url|ASIN> [...]          # link, title, price, availability, rating, review count
python3 $S --details <url|ASIN>      # plus feature bullets and the spec table
python3 $S --search "terms" -n 5     # top hits: title, ASIN, price, rating, reviews, link
python3 $S --html <url|ASIN> | grep  # raw page when the parser misses a field
python3 $S --json ...                # machine-readable
```

Search by keyword instead of opening a product page per candidate. `--organic` drops
sponsored hits; `--min-price`/`--max-price` take dollars and filter server-side:

```sh
python3 $S --search "usb-c hub" -n 3 --organic --min-price 20 --max-price 60 --json
```

Each hit is `{asin, url, title, price, rating, reviews, sponsored}`; `url` is already the
canonical `/dp/ASIN` link. Search reads page 1 only, so `--organic` filters that one page
and can return fewer than `-n` hits; raise `-n` rather than assuming the market is thin.
Fields are the search card's, so `price` is the listing price
and can lag the buybox - re-run the ASIN through the product mode before quoting a price
you'll act on.

Read the result before quoting it:

- **Price** is the buybox price scoped to the listed ASIN. "no price; Currently unavailable" means the ASIN is out of stock; find the successor via `--search` (a variant or `Pro` model often replaced it) and quote that ASIN instead. Never lift a price from a related-items carousel.
- **Variants** share a page: an ASIN is one size/colour/bundle. When the user names a variant, resolve the exact ASIN and check the title says the right one before linking.
- **Sponsored** search hits are flagged; prefer organic hits with a review count.
- A **third-party seller** price on a brand like Mitutoyo can be a counterfeit; when the brand is counterfeit-prone, say so and prefer the manufacturer or an authorized dealer.

Failure modes: `fetch failed ... captcha` (or `... bot check`) after both User-Agents means Amazon is rate-limiting this IP; wait a minute or run from the other machine (`ssh mini` / `ssh laptop`). Amazon's bot check also ships as a normal HTTP 200 page, so a throttled search would otherwise look like an empty market - `--search` exits non-zero with `no result cards` instead of printing nothing. Treat that specific failure as "ask again later" and retry; it is not a verdict on the market. A genuine no-match page is told apart by Amazon's own "No results for" text and returns an empty list with exit 0, which does mean nothing matched - don't retry that one, widen the query or the price band. A wrong or missing field is a parser gap: use `--html` and grep, then fix the regex in the script rather than working around it.

## Delegating

A subagent sent at Amazon with WebFetch reports every page as HTTP 500 and returns maker-site prices only. Put `python3 ~/.claude/skills/fetch-amazon/scripts/amazon.py` in the brief with the two lines of usage it needs.
