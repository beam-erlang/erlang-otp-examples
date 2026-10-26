import http.server, pathlib, socket, subprocess, sys, threading, time
otp, script = sys.argv[1:]

def check(args, status, output=None):
    r = subprocess.run([str(pathlib.Path(otp) / 'bin/escript'), script, *args], capture_output=True, text=True, timeout=18)
    assert r.returncode == status, r
    if output is not None:
        assert r.stdout == output, r
check(['--help'], 0)
check([], 2)
check(['https://localhost/ping'], 2)
with socket.socket() as s:
    s.bind(('127.0.0.1', 0))
    unused = s.getsockname()[1]
check([f'http://127.0.0.1:{unused}/ping'], 1)

class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == '/timeout':
            time.sleep(6)
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'wrong')
        except (BrokenPipeError, ConnectionResetError):
            pass
with http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler) as server:
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for path in ('/wrong', '/timeout'):
            check([f'http://127.0.0.1:{server.server_port}' + path], 1)
    finally:
        server.shutdown()
        thread.join()
print('client failure and timeout checks: passed')
