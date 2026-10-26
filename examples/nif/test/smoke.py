"""Exercise only the copied application and its native library in a fresh VM."""
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

otp, archive = (Path(arg).resolve() for arg in sys.argv[1:])
erl = otp / 'bin' / ('erl.exe' if os.name == 'nt' else 'erl')
env = dict(os.environ)
for key in ('ERL_LIBS', 'ERL_FLAGS', 'ERL_AFLAGS', 'ERL_ZFLAGS',
            'LD_LIBRARY_PATH', 'LD_PRELOAD', 'DYLD_LIBRARY_PATH'):
    env.pop(key, None)
with tempfile.TemporaryDirectory(prefix='nif-copy-') as temp:
    copied = Path(temp) / 'example_nif'
    copied.mkdir()
    with tarfile.open(archive) as package:
        package.extractall(copied, filter='data')
    expression = ('ok = application:load(example_nif), '
                  '<<"Hello, world!">> = example_nif:hello(), '
                  'io:format("Hello, world!~n"), halt(0).')
    result = subprocess.run([str(erl), '-noshell', '-noinput', '-pa',
                             str(copied / 'ebin'), '-eval', expression],
                            cwd=temp, env=env, capture_output=True, text=True,
                            timeout=20)
    assert result.returncode == 0, (result.stdout[-4000:], result.stderr[-4000:])
    assert result.stdout == 'Hello, world!\n', result.stdout
print('nif: copied application loaded and executed native hello/0')
