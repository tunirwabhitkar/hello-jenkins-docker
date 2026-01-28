from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html

# Simple in-memory store for tasks
tasks = []  # list of {'id': int, 'text': str, 'done': bool}
next_id = 1

class Handler(BaseHTTPRequestHandler):
    def _render_page(self):
        # Build HTML for the to-do list and form
        items_html = ""
        for t in tasks:
            checked = 'checked' if t['done'] else ''
            text = html.escape(t['text'])
            items_html += f"<li><form method=\"post\" action=\"/toggle\" style=\"display:inline\">"
            items_html += f"<input type=\"hidden\" name=\"id\" value=\"{t['id']}\">"
            items_html += f"<input type=\"checkbox\" onChange=\"this.form.submit()\" {checked}> {text}</form>"
            items_html += f" <form method=\"post\" action=\"/delete\" style=\"display:inline;margin-left:8px\">"
            items_html += f"<input type=\"hidden\" name=\"id\" value=\"{t['id']}\">"
            items_html += "<button type=\"submit\">Delete</button></form></li>"

        html_page = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\">
  <title>To-Do List</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 2rem auto; }}
    ul {{ padding-left: 1rem; }}
    li {{ margin: 0.5rem 0; }}
    form.inline {{ display: inline; }}
    .done {{ text-decoration: line-through; color: #888; }}
  </style>
</head>
<body>
  <h1>To-Do List</h1>
  <form method=\"post\" action=\"/add\">
    <input type=\"text\" name=\"task\" placeholder=\"New task...\" required style=\"width:70%\"> 
    <button type=\"submit\">Add</button>
  </form>
  <h2>Tasks</h2>
  <ul>
    {items}
  </ul>
  <p>Hosted by Jenkins CI/CD on Azure</p>
</body>
</html>
""".format(items=items_html)
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
