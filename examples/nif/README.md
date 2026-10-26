# Native function

A Rebar3 library named `example_nif` with one function implemented in C:

```erlang
example_nif:hello().
%% <<"Hello, world!">>
```

The Erlang module loads its native library from the application's `priv`
directory. Its stub raises `nif_not_loaded`; it cannot produce the greeting
without executing the C implementation.

Use an explicitly selected Erlangsters OTP installation with public NIF headers
in `usr/include`, verified Rebar3 3.27.0, CMake 3.20+, a C compiler and Python
3.12+. Run these commands from this directory (Bash):

```sh
export OTP_PREFIX=/absolute/path/to/otp
export REBAR3=/absolute/path/to/rebar3
export PATH="$OTP_PREFIX/bin:$PATH"
"$OTP_PREFIX/bin/escript" "$REBAR3" get-deps
export REBAR_OFFLINE=1
"$OTP_PREFIX/bin/escript" "$REBAR3" compile
"$OTP_PREFIX/bin/escript" "$REBAR3" eunit
```

Rebar3's compile hooks configure and build the C library. CMake requires
`OTP_PREFIX` and uses only that installation's public NIF headers. The library
is written to `priv/example_nif.so` on Linux/macOS or `priv/example_nif.dll` on
Windows. The native module must be built for the selected runtime's architecture.

This starts from Rebar3's `lib` template and adds a small actual CMake project.
Rebar3's template named `cmake` generates a GNU Makefile; using CMake here is a
portable adaptation for the three intended workflow targets, not the output of
that template. No additional Rebar3 plugin or C library dependency is needed.

For an interactive call, run `"$OTP_PREFIX/bin/escript" "$REBAR3" shell` and
enter `example_nif:hello().`. EUnit checks the same result automatically.

Package the compiled application and exercise it after extraction into an
unrelated temporary directory:

```sh
tar -chzf _build/example_nif.tar.gz -C _build/default/lib/example_nif ebin priv
python3 test/smoke.py "$OTP_PREFIX" _build/example_nif.tar.gz
"$OTP_PREFIX/bin/escript" "$REBAR3" clean
```

The archive dereferences Rebar3's `priv` link so it contains the native library.
The smoke test starts a fresh selected runtime with the extracted application's
code path, checks the greeting, and removes its temporary files. It requires
both `ebin` and `priv`; an Erlang module alone is not a usable NIF package.
The clean hook removes the native build and library. On Windows, use
`escript.exe`; the workflow handles this selection and builds with CMake's
native toolchain.

Local compilation, EUnit, packaged execution and cleanup passed on both Linux
flavors. See the root [validation status](../../README.md#validation-status)
for installation identities. macOS, Windows and GitHub execution remain untested.
