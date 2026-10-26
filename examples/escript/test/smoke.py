import pathlib, subprocess, sys, tempfile, shutil
otp, script = sys.argv[1:]
with tempfile.TemporaryDirectory(prefix='escript space-') as d:
    copied = pathlib.Path(d) / pathlib.Path(script).name
    shutil.copy2(script, copied)
    for args, expected in [([], 'Args: []\n'), (['hello world', '--literal'], 'Args: ["hello world","--literal"]\n')]:
        r = subprocess.run([str(pathlib.Path(otp) / 'bin/escript'), str(copied), *args], cwd=d, capture_output=True, text=True, timeout=15)
        assert (r.returncode, r.stdout) == (0, expected), r
print('copied escript: passed')
