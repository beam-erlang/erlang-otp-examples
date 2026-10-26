# Umbrella release

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
See the [validation status](../../README.md#validation-status) for measured coverage; GitHub runtime
execution remains pending the setup action and distribution artifacts.

Extract `_build/prod/rel/example_release/example_release-0.1.0.tar.gz` into a new directory.
Run `bin/example_release foreground` there; from another terminal use
`bin/example_release stop`. The sample node name and cookie are in `config/vm.args`;
choose deployment-specific values before running outside a local demonstration.

Run the packaged smoke test on Linux with Python 3.12+:

```sh
python3 test/smoke.py _build/prod/rel/example_release/example_release-0.1.0.tar.gz \
  --otp "$OTP_PREFIX" --work-root /absolute/path/to/disposable-scratch
```

This starts a private EPMD, verifies the application and supervisor in the
extracted release, stops it, and repeats. Scratch copies and owned processes are
removed on completion or failure; the selected installation is never removed.
For full local isolation acceptance, install bubblewrap and add
`--isolate --deny "$PWD"`. This also hides the original project and selected OTP
prefix from the release processes. Keep scratch outside the hidden directories.
