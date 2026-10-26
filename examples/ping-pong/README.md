# Ping Pong

One example, two independent programs. The server uses Cowboy; the client uses Gun.
Build each project using its README. Start the extracted server release in one
terminal, then run in another:

```sh
"$OTP_PREFIX/bin/escript" client/_build/default/bin/ping-pong-client http://127.0.0.1:8080/ping
```

The server stays running; the client prints `pong` and exits zero. The server
binds loopback, defaults to port 8080, and accepts `PING_PONG_PORT` (0 selects
an ephemeral port printed at startup). `GET /ping` returns `200 text/plain`
with body `pong`; other routes return 404 and other methods return 405.

The client takes one complete HTTP URL. `--help` exits zero; malformed arguments
or unsupported URLs exit 2. Transport errors, five-second operation timeouts,
and unexpected responses exit 1. HTTP/1.1 only: no retries, redirects or TLS.
The packaged client contains Gun and its Erlang dependencies, but needs an OTP
installation. Server and client have separate locks and separate VMs.

The outer test/smoke.py tests the packaged pair; client/test/smoke.py tests
client failures using temporary local fixtures. Both own and clean their processes.

After building both projects, run the packaged smoke test on Linux with Python 3.12+:

```sh
python3 test/smoke.py server/_build/prod/rel/ping_pong_server/ping_pong_server-0.1.0.tar.gz \
  --otp "$OTP_PREFIX" --work-root /absolute/path/to/disposable-scratch \
  --client "$PWD/client/_build/default/bin/ping-pong-client"
```

The test extracts the server, copies the client, exchanges repeated requests,
checks route and method errors, and stops and restarts the server. For full local
isolation acceptance, add `--isolate --deny "$PWD"` with bubblewrap installed.
Keep scratch outside the hidden directories. The isolated server cannot access
the original project or OTP prefix; the copied client retains its selected runtime.
