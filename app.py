from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html

# Simple in-memory store for tasks
tasks = []  # list of {'id': int, 'text': str, 'done': bool}
next_id = 1

class Handler(BaseHTTPRequestHandler):
    def _render_page(self):
        # Build HTML for the to-do list and form with improved styling
        items_html = ""
        for t in tasks:
            checked = 'checked' if t['done'] else ''
            text = html.escape(t['text'])
            done_class = 'done' if t['done'] else ''
            items_html += f"<li class=\"task {done_class}\">"
            items_html += f"<form method=\"post\" action=\"/toggle\" style=\"display:inline\">"
            items_html += f"<input type=\"hidden\" name=\"id\" value=\"{t['id']}\">"
            items_html += f"<label class=\"checkbox-label\"><input type=\"checkbox\" onChange=\"this.form.submit()\" {checked}> <span class=\"task-text\">{text}</span></label></form>"
            items_html += f"<form method=\"post\" action=\"/delete\" style=\"display:inline;margin-left:8px\">"
            items_html += f"<input type=\"hidden\" name=\"id\" value=\"{t['id']}\">"
            items_html += "<button class=\"btn btn-delete\" type=\"submit\">Delete</button></form></li>"

        count = len(tasks)
        html_page = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
  <title>To-Do List</title>
  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap\" rel=\"stylesheet\"> 
  <style>
    :root {{
      --bg-1: #0f172a;
      --bg-2: #0b1220;
      --card: rgba(255,255,255,0.04);
      --accent: #7c3aed; /* violet */
      --accent-2: #06b6d4; /* cyan */
      --muted: #94a3b8;
      --glass: rgba(255,255,255,0.03);
    }}
    html,body {{ height:100%; margin:0; font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background: linear-gradient(180deg,var(--bg-1),var(--bg-2)); color:#e6eef8; }}
    .container {{ max-width:840px; margin:48px auto; padding:24px; background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border-radius:14px; box-shadow: 0 8px 30px rgba(2,6,23,0.6); border: 1px solid rgba(255,255,255,0.03); }}
    header {{ display:flex; align-items:center; justify-content:space-between; gap:16px; margin-bottom:18px; }}
    h1 {{ margin:0; font-weight:700; letter-spacing:-0.5px; font-size:1.5rem; }}
    .subtitle {{ color:var(--muted); font-size:0.9rem; }}
    form.add-form {{ display:flex; gap:8px; margin-top:12px; }}
    input[type=text] {{ flex:1; min-width:0; background:var(--glass); border:1px solid rgba(255,255,255,0.04); padding:12px 14px; border-radius:10px; color:inherit; box-shadow: inset 0 1px 0 rgba(255,255,255,0.02); }}
    input[type=text]:focus {{ outline: none; box-shadow: 0 0 0 4px rgba(124,58,237,0.08); border-color: rgba(124,58,237,0.6); }}
    .btn {{ background: linear-gradient(90deg,var(--accent),var(--accent-2)); color:white; padding:10px 14px; border-radius:10px; border:none; cursor:pointer; font-weight:600; box-shadow: 0 6px 18px rgba(12,10,20,0.6); transition: transform .12s ease, box-shadow .12s ease; }}
    .btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(12,10,20,0.7); }}
    .btn:active {{ transform: translateY(0); }}
    .btn-ghost {{ background:transparent; border:1px solid rgba(255,255,255,0.04); color:var(--muted); box-shadow:none; }}
    ul.tasks {{ list-style:none; padding:0; margin:18px 0 0 0; display:block; }}
    li.task {{ display:flex; align-items:center; justify-content:space-between; gap:12px; padding:12px; margin-bottom:10px; border-radius:10px; background: rgba(255,255,255,0.015); border:1px solid rgba(255,255,255,0.02); }}
    li.task:hover {{ transform: translateY(-2px); transition: transform .12s ease; box-shadow: 0 6px 18px rgba(2,6,23,0.6); }}
    .checkbox-label {{ display:flex; align-items:center; gap:12px; cursor:pointer; user-select:none; }}
    .checkbox-label input[type=checkbox] {{ width:18px; height:18px; accent-color: var(--accent); cursor:pointer; }}
    .task-text {{ max-width:680px; display:inline-block; word-break:break-word; }}
    .task.done .task-text {{ text-decoration: line-through; color: #7b8794; opacity:0.85; }}
    .task .btn-delete {{ background:transparent; border: 1px solid rgba(255,255,255,0.04); color:var(--muted); padding:8px 10px; border-radius:8px; box-shadow:none; }}
    .task-count {{ color:var(--muted); font-size:0.95rem; }}
    .empty {{ padding:30px; text-align:center; color:var(--muted); border-radius:8px; background: linear-gradient(90deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00)); margin-top:8px; }}
    footer {{ margin-top:20px; color:var(--muted); font-size:0.85rem; text-align:right; }}
  </style>
</head>
<body>
  <div class=\"container\"> 
    <header>
      <div>
        <h1>To‑Do List</h1>
        <div class=\"subtitle\">Organize your tasks — simple and pretty</div>
      </div>
      <div class=\"task-count\">{count} task{plural}</div>
    </header>

    <form class=\"add-form\" method=\"post\" action=\"/add\">
      <input type=\"text\" name=\"task\" placeholder=\"Add a new task... e.g. Fix CI pipeline\" required>
      <button class=\"btn\" type=\"submit\">Add</button>
    </form>

    {items_section}

    <footer>
      <div>Built for CI/CD demos • Serve on port 8080</div>
    </footer>
  </div>
</body>
</html>
""".format(items_section=("<ul class=\"tasks\">"+items_html+"</ul>" if items_html else "<div class=\"empty\">No tasks yet — add one above.</div>"), count=count, plural=('s' if count!=1 else ''))
        return html_page.encode('utf-8')

    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        content = self._render_page()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        global next_id
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length else ''
        data = parse_qs(body)

        if self.path == '/add':
            text_vals = data.get('task')
            if text_vals:
                text = text_vals[0].strip()
                if text:
                    tasks.append({'id': next_id, 'text': text, 'done': False})
                    next_id += 1
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return

        if self.path == '/toggle':
            id_vals = data.get('id')
            if id_vals:
                try:
                    tid = int(id_vals[0])
                    for t in tasks:
                        if t['id'] == tid:
                            t['done'] = not t['done']
                            break
                except ValueError:
                    pass
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return

        if self.path == '/delete':
            id_vals = data.get('id')
            if id_vals:
                try:
                    tid = int(id_vals[0])
                    for i, t in enumerate(tasks):
                        if t['id'] == tid:
                            tasks.pop(i)
                            break
                except ValueError:
                    pass
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            return

        # Unknown POST path
        self.send_error(404)


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    print('Server listening on port 8080...')
    server.serve_forever()
