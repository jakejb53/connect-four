#!/usr/bin/env python3
"""
    python3 serve.py

Serves the current folder as static files, and exposes:

    POST /proxy?url=<url-encoded upstream URL>

which forwards the request upstream and streams the response back. Open
http://localhost:8000/ in the browser.

Only same-origin use is allowed: every request must carry a localhost Host
header (blocks DNS rebinding), and /proxy requests must carry a matching
Origin header (blocks cross-site requests from other pages in the browser).
No CORS headers are sent; the page calls /proxy on its own origin.
"""
import http.client, os, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8000
ALLOWED_HOSTS = {f"localhost:{PORT}", f"127.0.0.1:{PORT}"}
ALLOWED_ORIGINS = {"http://" + h for h in ALLOWED_HOSTS}

class Handler(SimpleHTTPRequestHandler):
    # HTTP/1.1 keeps static-file connections alive. Proxied responses are
    # streamed without a Content-Length, so _proxy sends Connection: close
    # and closing the socket marks the end of the body.
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("[serve] " + (fmt % args) + "\n")

    def parse_request(self):
        # Runs before every do_* method, so the Host check covers all
        # methods and paths. A rebound attacker domain resolving to
        # 127.0.0.1 still sends its own name as Host, which is rejected.
        if not super().parse_request():
            return False
        host = (self.headers.get("Host") or "").lower()
        if host not in ALLOWED_HOSTS:
            self.log_message("rejected Host %r", host)
            self.send_error(403, "Forbidden host")
            return False
        return True

    def do_POST(self):
        if not self.path.startswith("/proxy"):
            return self.send_error(404, "POST only supported on /proxy")
        self._proxy()

    def _proxy(self):
        # Browsers send Origin on every fetch() POST, same-origin included,
        # so a missing or foreign Origin means the request did not come from
        # the page this server hosts (e.g. a cross-site form post).
        origin = (self.headers.get("Origin") or "").lower()
        if origin not in ALLOWED_ORIGINS:
            self.log_message("rejected Origin %r for %s", origin, self.path)
            return self.send_error(403, "Forbidden origin")

        qs = parse_qs(urlparse(self.path).query)
        url = (qs.get("url") or [None])[0]
        if not url:
            return self.send_error(400, "missing url parameter")

        u = urlparse(url)
        if not u.hostname:
            return self.send_error(400, "invalid url")

        path = u.path or "/"
        if u.query:
            path += "?" + u.query

        # Only Content-Length-framed bodies are forwarded; chunked request
        # bodies are not supported (fetch() with a string body never sends one).
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else None

        # Any scheme other than https is treated as plain http.
        scheme = u.scheme or "http"
        cls = http.client.HTTPSConnection if scheme == "https" else http.client.HTTPConnection
        port = u.port or (443 if scheme == "https" else 80)


        # Strip headers that make the upstream think this is a browser request.
        drop = {"host", "content-length", "accept-encoding", "connection",
                "origin", "referer"}
        fwd = {k: v for k, v in self.headers.items() if k.lower() not in drop}

        try:
            # The timeout applies to each socket operation, not the whole
            # request, so long streamed generations are not cut off.
            conn = cls(u.hostname, port, timeout=300)
            conn.request(self.command, path, body=body, headers=fwd)
            resp = conn.getresponse()
        except Exception as e:
            # Details go to stderr only; the browser gets an empty 502.
            sys.stderr.write(f"[serve] upstream error for {url}: {e}\n")
            self.send_response(502)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        self.send_response(resp.status)
        # http.client has already de-chunked the body, and its length is not
        # known up front, so the upstream framing headers would be wrong here.
        for k, v in resp.getheaders():
            if k.lower() in {"connection", "transfer-encoding", "content-length"}:
                continue
            self.send_header(k, v)
        self.send_header("Connection", "close")
        self.end_headers()

        try:
            while True:
                chunk = resp.read1(4096)      # read1 => SSE flushes live
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            # The browser went away (e.g. Stop aborted the fetch); nothing to report.
            pass
        finally:
            try: conn.close()
            except Exception: pass
            self.close_connection = True


if __name__ == "__main__":
    addr = ("127.0.0.1", PORT)
    print(f"Open: http://localhost:{PORT}/")
    print("Set each player's endpoint field to the real upstream URL, e.g.")
    print("    http://10.0.0.5:1234/v1")
    ThreadingHTTPServer(addr, Handler).serve_forever()
