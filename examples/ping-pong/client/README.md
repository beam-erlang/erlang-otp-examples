# Ping Pong client

This is an independent Rebar3 project for Erlangsters Erlang/OTP. Select the
installed distribution and checksum-verified Rebar3 3.27.0 explicitly:

```sh
export OTP_PREFIX=/absolute/path/to/otp
export REBAR3=/absolute/path/to/rebar3
export PATH="$OTP_PREFIX/bin:$PATH"
"$OTP_PREFIX/bin/escript" "$REBAR3" get-deps
export REBAR_OFFLINE=1
"$OTP_PREFIX/bin/escript" "$REBAR3" compile
"$OTP_PREFIX/bin/escript" "$REBAR3" eunit
"$OTP_PREFIX/bin/escript" "$REBAR3" escriptize
```

Build outputs stay in `_build/`. No sibling project is a build dependency.
The production release includes ERTS; escripts require the selected installed
runtime. Dependency acquisition is explicit, and subsequent builds run offline.
See the [validation status](../../../README.md#validation-status) for measured coverage; GitHub runtime
execution remains pending the setup action and distribution artifacts.

Run the built client with:

```sh
"$OTP_PREFIX/bin/escript" _build/default/bin/ping-pong-client http://127.0.0.1:8080/ping
python3 test/smoke.py "$OTP_PREFIX" "$PWD/_build/default/bin/ping-pong-client"
```

Success prints `pong` and exits 0. `--help` exits 0. Invalid arguments and
unsupported URLs exit 2; request/response errors exit 1 with diagnostics on
stderr. Only HTTP/1.1 is supported, without retries or redirects. Each connection
or response wait is bounded to five seconds. The escript contains Gun and its
Erlang dependencies; OTP supplies the runtime and standard applications.
