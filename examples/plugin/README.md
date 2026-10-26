# Rebar3 plugin

A minimal plugin named `example_plugin`, generated with Rebar3 3.27.0's
`plugin` template. It registers `hello`, which prints `Hello, world!` and exits
successfully. The provider keeps the standard initialization, execution and
error-formatting callbacks.

Use an explicitly selected Erlangsters OTP installation and the verified
Rebar3 3.27.0 executable described in the root README. Python 3.12+ is needed
for the smoke test. Run these commands from this directory (Bash):

```sh
export OTP_PREFIX=/absolute/path/to/otp
export REBAR3=/absolute/path/to/rebar3
export PATH="$OTP_PREFIX/bin:$PATH"
"$OTP_PREFIX/bin/escript" "$REBAR3" get-deps
export REBAR_OFFLINE=1
"$OTP_PREFIX/bin/escript" "$REBAR3" compile
```

A plugin is used from another project's Rebar configuration. The tiny fixture
in `test/consumer/` declares this plugin. Use Rebar3's local checkout mechanism
to try it without publishing a package:

```sh
mkdir -p test/consumer/_checkouts/example_plugin
cp -R src rebar.config test/consumer/_checkouts/example_plugin/
cd test/consumer
"$OTP_PREFIX/bin/escript" "$REBAR3" help hello
"$OTP_PREFIX/bin/escript" "$REBAR3" hello
```

The second command prints `Hello, world!` after any Rebar3 build messages.
Return to the example directory and remove the disposable consumer outputs:

```sh
cd ../..
rm -rf test/consumer/_checkouts test/consumer/_build
```

The automated check performs the same consumer setup in a temporary directory,
verifies help and the greeting, and removes the directory on completion:

```sh
python3 test/smoke.py "$OTP_PREFIX" "$REBAR3"
"$OTP_PREFIX/bin/escript" "$REBAR3" clean
```

No external plugin package is required. The workflow uploads a source archive,
including the consumer fixture, that Rebar3 can compile locally. Windows uses
`escript.exe`; the workflow selects that executable explicitly.

Local compile, consumer execution and cleanup passed on both Linux flavors.
See the root [validation status](../../README.md#validation-status) for the
installation identities and remaining platform/release limitations.
