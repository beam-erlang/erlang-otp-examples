"""Exercise an extracted release with an owned EPMD and optional filesystem isolation."""
import argparse, os, pathlib, signal, socket, subprocess, tarfile, tempfile, time, urllib.request, urllib.error, shutil
p = argparse.ArgumentParser()
p.add_argument('archive')
p.add_argument('--otp', required=True)
p.add_argument('--client')
p.add_argument('--work-root', required=True)
p.add_argument('--isolate', action='store_true', help='Hide original inputs using Linux bubblewrap')
p.add_argument('--deny', action='append', default=[])
a = p.parse_args()
a.otp = str(pathlib.Path(a.otp).resolve())
if a.deny and not a.isolate:
    p.error('--deny requires --isolate')
name = 'ping_pong_server' if a.client else 'example_release'

def port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, timeout=20, text=True, capture_output=True, cwd=dst, **kw)
children = []

def stop(proc):
    if proc.poll() is None:
        os.killpg(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()

def interrupted(*_):
    raise KeyboardInterrupt
signal.signal(signal.SIGTERM, interrupted)
root = pathlib.Path(a.work_root).resolve()
root.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='release-', dir=root) as temp:
    dst = pathlib.Path(temp) / 'release space'
    dst.mkdir()
    if a.client:
        client_copy = pathlib.Path(temp) / pathlib.Path(a.client).name
        shutil.copy2(a.client, client_copy)
        a.client = str(client_copy)
    with tarfile.open(a.archive) as t:
        t.extractall(dst, filter='data')
    env = dict(os.environ, ERL_EPMD_PORT=str(port()), ERL_EPMD_ADDRESS='127.0.0.1', PING_PONG_PORT=str(port()), PATH='/usr/bin:/bin')
    for key in ('ERL_LIBS', 'ERL_FLAGS', 'ERL_AFLAGS', 'ERL_ZFLAGS', 'LD_LIBRARY_PATH', 'LD_PRELOAD'):
        env.pop(key, None)
    base = []
    if a.isolate:
        denied = {str(pathlib.Path(x).resolve()) for x in a.deny + [a.otp]}
        base = ['bwrap', '--die-with-parent', '--ro-bind', '/', '/', '--dev-bind', '/dev', '/dev', '--proc', '/proc', '--tmpfs', '/tmp']
        for path in sorted(denied):
            base += ['--tmpfs', path]
        base += ['--bind', str(dst), '/tmp/release', '--chdir', '/tmp/release']

    def cmd(*args):
        executable = '/tmp/release/bin/' + name if a.isolate else str(dst / 'bin' / name)
        return base + [executable, *args]
    log = open(pathlib.Path(temp) / 'server.log', 'w+')
    try:
        epmd = subprocess.Popen([str(next(dst.glob('erts-*/bin/epmd'))), '-port', env['ERL_EPMD_PORT']], env=env, stdout=log, stderr=log, start_new_session=True, cwd=dst)
        children.append(epmd)
        for cycle in range(2):
            server = subprocess.Popen(cmd('foreground'), env=env, stdout=log, stderr=log, start_new_session=True, cwd=dst)
            children.append(server)
            end = time.monotonic() + 15
            while True:
                if server.poll() is not None:
                    raise RuntimeError('release exited before readiness')
                try:
                    out = run(cmd('rpc', 'application:which_applications().'), env=env).stdout
                    if name in out:
                        break
                except (subprocess.SubprocessError, OSError):
                    pass
                if time.monotonic() > end:
                    raise RuntimeError('release readiness timeout')
                time.sleep(0.15)
            out = run(cmd('rpc', 'is_pid(whereis(' + name + '_sup)).'), env=env).stdout
            assert 'true' in out, out
            if a.client:
                url = 'http://127.0.0.1:' + env['PING_PONG_PORT'] + '/ping'
                for _ in range(3):
                    client_cmd = [str(pathlib.Path(a.otp) / 'bin/escript'), a.client, url]
                    if a.isolate:
                        client_cmd = ['bwrap', '--die-with-parent', '--ro-bind', '/', '/', '--tmpfs', '/tmp']
                        for denied_source in a.deny:
                            client_cmd += ['--tmpfs', str(pathlib.Path(denied_source).resolve())]
                        client_cmd += ['--ro-bind', a.otp, a.otp, '--ro-bind', a.client, '/tmp/ping-pong-client', '--chdir', '/tmp', str(pathlib.Path(a.otp) / 'bin/escript'), '/tmp/ping-pong-client', url]
                    out = run(client_cmd, env=env)
                    assert out.stdout == 'pong\n', out
                for path, method, status in [('/missing', 'GET', 404), ('/ping', 'POST', 405)]:
                    try:
                        urllib.request.urlopen(urllib.request.Request(url.rsplit('/', 1)[0] + path, method=method), timeout=5)
                        raise AssertionError('unexpected success')
                    except urllib.error.HTTPError as ex:
                        assert ex.code == status
            run(cmd('stop'), env=env)
            server.wait(timeout=15)
            assert server.returncode == 0, server.returncode
        mode = 'isolated' if a.isolate else 'smoke'
        print(name + ': packaged ' + mode + ' and restart checks passed')
    except BaseException:
        log.flush()
        log.seek(0)
        print(log.read()[-12000:])
        raise
    finally:
        for child in reversed(children):
            stop(child)
        log.close()
