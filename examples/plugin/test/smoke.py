"""Load the local plugin in a disposable consumer and invoke its command."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

otp, rebar = (Path(arg).resolve() for arg in sys.argv[1:])
project = Path(__file__).resolve().parents[1]
escript = otp / 'bin' / ('escript.exe' if os.name == 'nt' else 'escript')
with tempfile.TemporaryDirectory(prefix='plugin-consumer-') as temp:
    consumer = Path(temp)
    shutil.copy2(project / 'test/consumer/rebar.config', consumer)
    checkout = consumer / '_checkouts/example_plugin'
    shutil.copytree(project / 'src', checkout / 'src')
    shutil.copy2(project / 'rebar.config', checkout)
    (consumer / 'config').mkdir()
    env = dict(os.environ, REBAR_OFFLINE='1',
               REBAR_GLOBAL_CONFIG_DIR=str(consumer / 'config'),
               REBAR_CACHE_DIR=str(consumer / 'cache'))
    for command in (['help', 'hello'], ['hello']):
        result = subprocess.run([str(escript), str(rebar), *command],
                                cwd=consumer, env=env, capture_output=True,
                                text=True, timeout=30)
        assert result.returncode == 0, (result.stdout[-4000:], result.stderr[-4000:])
        if command[0] == 'help':
            assert 'Print Hello, world!' in result.stdout, result.stdout
        else:
            assert result.stdout.splitlines().count('Hello, world!') == 1, result.stdout
print('plugin: help and greeting passed in a copied consumer')
