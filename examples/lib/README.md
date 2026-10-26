# Library application

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
```

Build outputs stay in `_build/`. No sibling project is a build dependency.
The production release includes ERTS; escripts require the selected installed
runtime. Dependency acquisition is explicit, and subsequent builds run offline.
See the [validation status](../../README.md#validation-status) for measured coverage; GitHub runtime
execution remains pending the setup action and distribution artifacts.

`example_lib:hello().` returns `<<"Hello, world!">>`. EUnit verifies it.
