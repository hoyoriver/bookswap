#!/usr/bin/env python3
"""bookswap 로컬 서버 — 네이버 책 검색 API 프록시 포함"""

import os
import ssl
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# .env 파일 로드
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, _, val = line.partition('=')
            os.environ.setdefault(key.strip(), val.strip())

PORT = int(os.environ.get('PORT', 3000))
NAVER_CLIENT_ID = os.environ.get('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = os.environ.get('NAVER_CLIENT_SECRET', '')


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/books'):
            self.handle_book_search()
        else:
            super().do_GET()

    def handle_book_search(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        query = params.get('q', [''])[0]

        if not query:
            self.send_json(400, {'error': 'query required'})
            return

        if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
            self.send_json(500, {'error': '.env에 NAVER_CLIENT_ID, NAVER_CLIENT_SECRET을 설정해주세요'})
            return

        url = f"https://openapi.naver.com/v1/search/book.json?query={urllib.parse.quote(query)}&display=10"
        req = urllib.request.Request(url, headers={
            'X-Naver-Client-Id': NAVER_CLIENT_ID,
            'X-Naver-Client-Secret': NAVER_CLIENT_SECRET,
        })

        try:
            with urllib.request.urlopen(req, context=ssl_ctx) as resp:
                data = json.loads(resp.read().decode())
                self.send_json(200, data.get('items', []))
        except urllib.error.HTTPError as e:
            self.send_json(e.code, {'error': e.read().decode()})
        except Exception as e:
            self.send_json(500, {'error': str(e)})

    def send_json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # 로그 조용히


if __name__ == '__main__':
    print(f'bookswap 실행 중 → http://localhost:{PORT}')
    if not NAVER_CLIENT_ID:
        print('⚠  .env 파일에 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET을 채워주세요')
    HTTPServer(('', PORT), Handler).serve_forever()
