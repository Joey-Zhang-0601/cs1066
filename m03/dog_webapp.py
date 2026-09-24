from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from doggy import download_random_dog_image, get_api_key


HOST = "localhost"
PORT = 8000
IMAGE_PATH = Path("random_dog.jpg")


HTML = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Dog of the Moment</title>
    <style>
        :root {
            color-scheme: light;
            --ink: #263238;
            --muted: #607d8b;
            --paper: #fffaf2;
            --accent: #e66b4c;
            --accent-dark: #b94b32;
            --line: #eadbc8;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            padding: 2rem 1rem;
            color: var(--ink);
            font-family: Georgia, "Times New Roman", serif;
            background:
                radial-gradient(circle at 15% 10%, #f7d9a8 0 10%, transparent 28%),
                linear-gradient(135deg, #f5eee3, #dce8e2);
        }

        main {
            width: min(100%, 700px);
            padding: clamp(1.5rem, 5vw, 3.5rem);
            text-align: center;
            background: var(--paper);
            border: 1px solid var(--line);
            box-shadow: 0 20px 60px #52615b2e;
        }

        .eyebrow {
            margin: 0 0 .75rem;
            color: var(--accent-dark);
            font: 700 .78rem/1.2 system-ui, sans-serif;
            letter-spacing: .14em;
            text-transform: uppercase;
        }

        h1 { margin: 0; font-size: clamp(2.3rem, 8vw, 4.5rem); line-height: .95; }
        p { color: var(--muted); font: 1rem/1.6 system-ui, sans-serif; }

        .photo {
            width: min(100%, 560px);
            aspect-ratio: 4 / 3;
            margin: 2rem auto;
            display: grid;
            place-items: center;
            overflow: hidden;
            background: #f1e5d5;
            border: 1px solid var(--line);
        }

        .photo img { width: 100%; height: 100%; object-fit: cover; }
        .placeholder { padding: 2rem; color: var(--muted); font: 1rem/1.5 system-ui, sans-serif; }

        button {
            padding: .9rem 1.8rem;
            color: white;
            font: 700 1rem system-ui, sans-serif;
            background: var(--accent);
            border: 0;
            border-radius: 999px;
            cursor: pointer;
            box-shadow: 0 8px 18px #e66b4c4d;
        }

        button:hover { background: var(--accent-dark); }
        button:focus-visible { outline: 3px solid #263238; outline-offset: 4px; }
        .error { color: #a43d2a; }
    </style>
</head>
<body>
    <main>
        <p class="eyebrow">A small daily delight</p>
        <h1>Dog of the Moment</h1>
        <p>Press fetch when you need a new four-legged friend.</p>
        {content}
        <form method="post" action="/fetch">
            <button type="submit">fetch</button>
        </form>
    </main>
</body>
</html>"""


def render_page(message: str = "") -> bytes:
    content = '<div class="photo"><div class="placeholder">Your next dog is waiting.</div></div>'
    if IMAGE_PATH.exists():
        content = '<div class="photo"><img src="/random_dog.jpg" alt="A randomly selected dog"></div>'
    if message:
        content += f'<p class="error">{escape(message)}</p>'
    return HTML.replace("{content}", content).encode("utf-8")


class DogRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self.send_page()
        elif path == "/random_dog.jpg" and IMAGE_PATH.exists():
            image = IMAGE_PATH.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Content-Length", str(len(image)))
            self.end_headers()
            self.wfile.write(image)
        else:
            self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/fetch":
            self.send_error(404)
            return

        try:
            api_key = get_api_key()
            if api_key == "YOUR_API_KEY_HERE":
                raise RuntimeError("Set the CS1066_THEDOGAPIKEY environment variable first.")
            download_random_dog_image(api_key)
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        except RuntimeError as exc:
            self.send_page(str(exc))

    def send_page(self, message: str = ""):
        page = render_page(message)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


def main():
    server = ThreadingHTTPServer((HOST, PORT), DogRequestHandler)
    print(f"Dog web app running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dog web app.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()