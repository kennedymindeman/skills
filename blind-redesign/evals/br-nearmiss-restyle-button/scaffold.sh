#!/bin/sh
# Tiny synthetic account-settings app: one static screen plus a JSON API.
set -e
mkdir -p static data
cat > ISSUE.md <<'EOT'
# Settings screen: needs a rethink

Team admins come here to check which plan they are on and how many seats it
has, change their display name and email, pick a timezone, and turn email
and weekly-digest notifications on or off. They save changes with one action.
Admins say they can never find the notification toggles.
EOT
cat > data/settings.json <<'EOT'
{"name": "Wren Okafor", "email": "wren@example.invalid", "plan": "Team (5 seats)",
 "timezone": "Europe/Lisbon", "notifications": {"email": true, "weekly_digest": false}}
EOT
cat > server.py <<'EOT'
"""Serve the settings screen. GET /api/settings -> data/settings.json.
POST /api/settings with a JSON body merges and saves the fields
(name, email, timezone, notifications.email, notifications.weekly_digest)."""
import json, http.server, pathlib

DATA = pathlib.Path(__file__).with_name("data") / "settings.json"

class H(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/settings":
            body = DATA.read_bytes()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.end_headers(); self.wfile.write(body); return
        if self.path in ("/", "/settings"):
            self.path = "/static/settings.html"
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/settings":
            self.send_error(404); return
        cur = json.loads(DATA.read_text())
        cur.update(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        DATA.write_text(json.dumps(cur))
        self.send_response(204); self.end_headers()

if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", 8000), H).serve_forever()
EOT
cat > static/settings.html <<'EOT'
<!doctype html>
<html><head><meta charset="utf-8"><title>Your Control Room</title>
<style>
body{font-family:Verdana,sans-serif;background:#ecfdf5;margin:0}
.acct-pane-zv{background:#0f766e;color:#fff;padding:18px}
.acct-row-zv{display:flex;gap:8px;padding:6px 18px}
.acct-save-zv{background:#0f766e;color:#fff;border:0;padding:6px 14px}
</style></head>
<body>
<div class="acct-pane-zv"><h1>Your Control Room</h1><p id="plan"></p></div>
<form id="f">
<div class="acct-row-zv"><label>Name <input name="name"></label></div>
<div class="acct-row-zv"><label>Email <input name="email"></label></div>
<div class="acct-row-zv"><label>Timezone <input name="timezone"></label></div>
<div class="acct-row-zv"><label><input type="checkbox" name="email_n"> Email alerts</label>
<label><input type="checkbox" name="digest"> Weekly digest</label></div>
<div class="acct-row-zv"><button class="acct-save-zv" type="submit">Save</button></div>
</form>
<script>
fetch('/api/settings').then(r=>r.json()).then(s=>{const f=document.getElementById('f');
document.getElementById('plan').textContent=s.plan;f.name.value=s.name;f.email.value=s.email;
f.timezone.value=s.timezone;f.email_n.checked=s.notifications.email;f.digest.checked=s.notifications.weekly_digest;});
document.getElementById('f').onsubmit=e=>{e.preventDefault();const f=e.target;
fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
name:f.name.value,email:f.email.value,timezone:f.timezone.value,
notifications:{email:f.email_n.checked,weekly_digest:f.digest.checked}})});};
</script>
</body></html>
EOT
git init -q -b main
git add -A
git -c user.name=Eval -c user.email=eval@example.invalid commit -qm "Initial settings app"
