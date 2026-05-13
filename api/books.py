import ssl
import json
import urllib.request
import urllib.parse
import os
from http.server import BaseHTTPRequestHandler

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        query = params.get('q', [''])[0]

        if not query:
            self._json(400, {'error': 'query required'})
            return

        client_id = os.environ.get('NAVER_CLIENT_ID', '')
        client_secret = os.environ.get('NAVER_CLIENT_SECRET', '')

        if not client_id or not client_secret:
            self._json(500, {'error': 'NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 환경변수를 Vercel에 설정해주세요'})
            return

        url = f"https://openapi.naver.com/v1/search/book.json?query={urllib.parse.quote(query)}&display=10"
        req = urllib.request.Request(url, headers={
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret,
        })

        try:
            with urllib.request.urlopen(req, context=ssl_ctx) as resp:
                data = json.loads(resp.read().decode())
                self._json(200, data.get('items', []))
        except urllib.error.HTTPError as e:
            self._json(e.code, {'error': e.read().decode()})
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass
