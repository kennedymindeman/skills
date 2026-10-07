#!/bin/sh
# Tiny synthetic warehouse app: one static screen plus a JSON API.
set -e
mkdir -p static data
cat > ISSUE.md <<'EOF'
# Orders screen: needs a rethink

Warehouse leads open this screen at the start of each shift. They want to see
at a glance which orders are late or due today, who the customer is, and how
many items are in each order. When a parcel leaves the dock they mark that
order shipped from this screen. Right now leads say late orders are hard to spot.
EOF
cat > data/orders.json <<'EOF'
{"orders": [
  {"id": "SO-1041", "customer": "Fernhill Bakery", "items": 12, "due": "2026-10-05", "status": "late"},
  {"id": "SO-1042", "customer": "Quayside Florists", "items": 3, "due": "2026-10-07", "status": "due_today"},
  {"id": "SO-1043", "customer": "Ostrander Cycles", "items": 7, "due": "2026-10-09", "status": "open"},
  {"id": "SO-1044", "customer": "Linden & Rowe", "items": 1, "due": "2026-10-04", "status": "late"},
  {"id": "SO-1045", "customer": "Marsh Lane Pottery", "items": 24, "due": "2026-10-07", "status": "shipped"}
]}
EOF
cat > server.py <<'EOF'
"""Serve the orders screen. GET /api/orders -> data/orders.json.
POST /api/orders/<id>/ship marks an order shipped (status -> "shipped").
Fields: id, customer, items (count), due (ISO date), status (late|due_today|open|shipped)."""
import json, http.server, pathlib

DATA = pathlib.Path(__file__).with_name("data") / "orders.json"

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/orders":
            body = DATA.read_bytes()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.end_headers(); self.wfile.write(body); return
        if self.path in ("/", "/orders"):
            self.path = "/static/orders.html"
        super().do_GET()

    def do_POST(self):
        parts = self.path.strip("/").split("/")
        if len(parts) == 4 and parts[:2] == ["api", "orders"] and parts[3] == "ship":
            doc = json.loads(DATA.read_text())
            for o in doc["orders"]:
                if o["id"] == parts[2]:
                    o["status"] = "shipped"
            DATA.write_text(json.dumps(doc))
            self.send_response(204); self.end_headers(); return
        self.send_error(404)

if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
EOF
cat > static/orders.html <<'EOF'
<!doctype html>
<meta charset="utf-8">
<title>Dispatch Board</title>
<style>
  body { font-family: Georgia, serif; background: #f3eefa; margin: 0; }
  .ledger-head-xq { background: #5b2a86; color: #fff; padding: 14px 20px; }
  .ledger-grid-xq { display: grid; grid-template-columns: 2fr 3fr 1fr 2fr 2fr 1fr; gap: 1px; background: #c9b6dd; }
  .ledger-grid-xq > div { background: #fff; padding: 8px; }
  .ledger-btn-xq { background: #5b2a86; color: #fff; border: 0; padding: 4px 10px; }
</style>
<header class="ledger-head-xq"><h1>Dispatch Board</h1></header>
<section class="ledger-grid-xq" id="grid">
  <div>Order</div><div>Customer</div><div>Items</div><div>Due</div><div>Status</div><div></div>
</section>
<script>
fetch('/api/orders').then(r => r.json()).then(({orders}) => {
  const grid = document.getElementById('grid');
  for (const o of orders) {
    for (const v of [o.id, o.customer, o.items, o.due, o.status]) {
      const d = document.createElement('div'); d.textContent = v; grid.append(d);
    }
    const cell = document.createElement('div');
    if (o.status !== 'shipped') {
      const b = document.createElement('button'); b.className = 'ledger-btn-xq'; b.textContent = 'Ship';
      b.onclick = () => fetch(`/api/orders/${o.id}/ship`, {method: 'POST'}).then(() => location.reload());
      cell.append(b);
    }
    grid.append(cell);
  }
});
</script>
EOF
git init -q -b main
git -c user.name=Eval -c user.email=eval@example.invalid add -A
git -c user.name=Eval -c user.email=eval@example.invalid commit -q -m "Orders screen"
