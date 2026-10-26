# Ping Pong server

This is an independent Rebar3 project for Erlangsters Erlang/OTP. Select the
installed distribution and checksum-verified Rebar3 3.27.0 explicitly:

```sh
export OTP_PREFIX=/absolute/path/to/otp
export REBAR3=/absolute/path/to/rebar3
export PATH="$OTP_PREFIX/bin:$PATH"
"$OTP_PREFIX/bin/escript" "$REBAR3" get-deps
export REBAR_OFFLINE=1
"$OTP_PREFIX/bin/escript" "$REBAR3" compile
"$OTP_PREFIX/bin/escript" "$REBAR3" as prod tar
```

Build outputs stay in `_build/`. No sibling project is a build dependency.
The production release includes ERTS; escripts require the selected installed
runtime. Dependency acquisition is explicit, and subsequent builds run offline.
See the [validation status](../../../README.md#validation-status) for measured coverage; GitHub runtime
execution remains pending the setup action and distribution artifacts.

Extract `_build/prod/rel/ping_pong_server/ping_pong_server-0.1.0.tar.gz` into a new directory.
Run `bin/ping_pong_server foreground` there; from another terminal use
`bin/ping_pong_server stop`. The sample node name and cookie are in `config/vm.args`;
choose deployment-specific values before running outside a local demonstration.

The listener binds `127.0.0.1`. Set `PING_PONG_PORT` before launching to override
8080. Port 0 requests an ephemeral port, reported in the startup message.
`GET /ping` returns `200`, `text/plain`, and `pong`; unknown paths return 404,
and unsupported methods return 405 with `Allow: GET`. Invalid port values fail
startup. A browser or `curl http://127.0.0.1:8080/ping` can exercise the endpoint.
Application shutdown stops the listener. TLS and HTTP/2 are outside this example.
