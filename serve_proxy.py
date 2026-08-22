#!/usr/bin/env python3
"""Caching reverse proxy: serve local Hubtown clone, fetch+cache misses from origin."""
from __future__ import annotations

import http.client
import ssl
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ORIGIN_HOST = "hubtown.co.in"
LOCAL_ORIGIN = "http://127.0.0.1:8765"
ROOT = Path(r"D:\real estate\hubtown-clone")
PORT = 8765
CTX = ssl.create_default_context()

MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".otf": "font/otf",
    ".mp4": "video/mp4",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".webmanifest": "application/manifest+json",
}


def guess_mime(path: Path) -> str:
    return MIME.get(path.suffix.lower(), "application/octet-stream")


def patch_html(data: bytes) -> bytes:
    """Fix relative URLs so Nuxt/WebGL init works when served from localhost."""
    text = data.decode("utf-8", errors="ignore")
    base_tag = f'<base href="{LOCAL_ORIGIN}/">'
    if "<base " not in text:
        text = text.replace("<head>", f"<head>{base_tag}", 1)
    text = text.replace("https://hubtown-live.netlify.app", LOCAL_ORIGIN)
    text = text.replace('hubtown-live",""', f'hubtown-live","{LOCAL_ORIGIN}"', 1)
    text = text.replace('"url":"/"', f'"url":"{LOCAL_ORIGIN}/"')
    text = text.replace('href="/"', f'href="{LOCAL_ORIGIN}/"', 1)
    return text.encode("utf-8")


def local_path(url_path: str) -> Path:
    path = unquote(url_path.split("?", 1)[0])
    if path.endswith("/"):
        path += "index.html"
    if path.startswith("/"):
        path = path[1:]
    if not path:
        path = "index.html"
    return ROOT / path


def fetch_origin(full_path: str) -> tuple[int, dict[str, str], bytes]:
    conn = http.client.HTTPSConnection(ORIGIN_HOST, context=CTX, timeout=90)
    conn.request(
        "GET",
        full_path,
        headers={
            "User-Agent": "Mozilla/5.0 HubtownLocalClone/1.0",
            "Accept": "*/*",
            "Host": ORIGIN_HOST,
        },
    )
    resp = conn.getresponse()
    data = resp.read()
    headers = {k: v for k, v in resp.getheaders()}
    status = resp.status
    conn.close()
    return status, headers, data


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def do_GET(self) -> None:  # noqa: N802
        self._handle()

    def do_HEAD(self) -> None:  # noqa: N802
        self._handle(head_only=True)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def _handle(self, head_only: bool = False) -> None:
        parsed = urlparse(self.path)
        rel = local_path(parsed.path)
        query = parsed.query
        origin_path = parsed.path + (("?" + query) if query else "")

        data: bytes | None = None
        if rel.exists() and rel.is_file():
            data = rel.read_bytes()
            status = 200
            ctype = guess_mime(rel)
        else:
            # Special-case: route files saved without .html (about, careers, ...)
            if not rel.suffix and rel.exists() and rel.is_file():
                data = rel.read_bytes()
                status = 200
                ctype = "text/html; charset=utf-8"
            else:
                try:
                    status, headers, data = fetch_origin(origin_path)
                except Exception as e:  # noqa: BLE001
                    self.send_error(502, f"Origin fetch failed: {e}")
                    return
                ctype = headers.get("Content-Type", guess_mime(rel))
                if status == 200 and data is not None and not query.startswith("v="):
                    # Cache successful responses without volatile query when possible
                    cache_rel = local_path(parsed.path)
                    try:
                        cache_rel.parent.mkdir(parents=True, exist_ok=True)
                        if not cache_rel.exists():
                            cache_rel.write_bytes(data)
                            print(f"CACHED {cache_rel.relative_to(ROOT)}")
                    except Exception as e:  # noqa: BLE001
                        print(f"cache fail {cache_rel}: {e}")

        if data is None:
            self.send_error(404)
            return

        if "text/html" in ctype and data:
            data = patch_html(data)

        body = b"" if head_only else data
        self.send_response(status if status else 200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    # Free note: binder
    httpd = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Hubtown caching proxy at http://127.0.0.1:{PORT}/")
    print(f"Local root: {ROOT}")
    print(f"Origin fallback: https://{ORIGIN_HOST}/")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
