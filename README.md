# Erlang/OTP examples

> **Distribution notice:** These examples target the Erlangsters Erlang/OTP
> distribution, which uses the BEAM/Erlang runtime implementation. This is not
> upstream Erlang/OTP or an official upstream examples repository.

> **Work in progress:** We are working towards making these examples build and
> run successfully with that distribution. They are not yet a verified set of
> working examples. End-to-end validation against published artifacts will follow
> the first distribution release. Installation and runtime compatibility work
> remains unfinished. The workflows are not ready for successful use today.

Small, conventional projects intended to demonstrate the Erlangsters Erlang/OTP
distribution. The catalog below describes their intended behavior; see
[validation status](#validation-status) for what has actually been checked.

| Example | Purpose |
| --- | --- |
| [App](examples/app/) | Empty supervised application |
| [Library](examples/lib/) | A pure exported function and EUnit |
| [Release](examples/release/) | Umbrella project with a bundled runtime |
| [Escript](examples/escript/) | Runnable argument-printing script |
| [Ping Pong](examples/ping-pong/) | Independent Cowboy server and Gun client |
| [Plugin](examples/plugin/) | A Rebar3 command that prints a greeting |
| [NIF](examples/nif/) | An Erlang function implemented in C |

Run each project’s commands from its directory under `examples/`.
Each project is structured to build independently with ordinary Rebar3 commands. There is no
root umbrella.

## Build tools

Select an installed Erlangsters OTP distribution explicitly. The examples use
Rebar3 3.27.0, which includes Relx 4.10.0. Each workflow contains the pinned
Rebar3 download URL and SHA-256 checksum; use that same verified executable for
local builds. No external Erlang distribution is used as a fallback.

Ping Pong uses Cowboy 2.20.0 and Gun 2.6.0. Each project keeps its own dependency
lock. Acquire dependencies explicitly before compiling, testing and packaging
offline. Smoke tests use Python 3.12+; optional local release isolation also
requires Linux bubblewrap. Example READMEs contain build and test commands.
The NIF example also requires CMake 3.20+ and a native C compiler. The plugin and
NIF have no external Erlang dependencies.

## GitHub Actions

Seven manual build-and-test workflows accept an exact distribution version. Each
defines six jobs: both `emu` and `jit` on the following targets.

| OS / architecture | GitHub runner |
| --- | --- |
| Linux x86-64 | `ubuntu-24.04` |
| macOS ARM64 | `macos-15` |
| Windows x86-64 | `windows-2025` |

Job and artifact names include the target and flavor. The workflows use major
action tags, including the intended
`setup-erlang-otp@v1` interface. That release is not yet published, installation is
not implemented, and distribution artifacts are not available. Runtime workflows
remain pending and must fail until those prerequisites exist.
Each workflow is structured to build, exercise the example, and upload tested artifacts.
The matrix is intended coverage, not established platform support. The existing
commands and runtime helpers were developed for Linux; macOS and Windows execution
remain unvalidated. Windows release startup and process cleanup still need native
adaptation. No tests are skipped or failures suppressed for those targets.
Rebar3 is downloaded at a fixed version and verified against its checksum.
Source and workflow checks are run locally.

## Validation status

Historical local checks on 2026-10-26 used unpublished OTP 29.0 development
installations on Linux x86-64. They predate the current layout and smoke-helper
revisions and do not establish compatibility for a published distribution or
validate the current repository end to end.

On the interpreter (`emu`) installation, the original six standalone projects compiled;
the application, library and client EUnit tests passed; both release archives and
both escripts were built. The copied argument-printing escript passed its checks,
as did the client's help, invalid URL, unreachable server, unexpected response and
timeout checks.

The extracted canonical release failed before application startup because its
generated configuration contains `+K true`. Both interpreter and JIT installations
failed this minimal probe with exit status 1 and
`erl: emulator option is not implemented: +K`:

```sh
"$OTP_PREFIX/bin/erl" +K true -noshell -eval 'halt(0).'
```

The option remains unchanged in `examples/release/config/vm.args`. Runtime
validation stopped at this compatibility blocker; no alternate runtime or
workaround was introduced. JIT builds and execution of the original five examples, successful release
startup/shutdown, and the packaged Ping Pong exchange and restart remain untested.
Compiling Cowboy and Gun does not establish a successful HTTP exchange.

Separate focused checks of the plugin and NIF on 2026-10-26 passed on both Linux
flavors. These used the installed OTP 29.0 development builds from OTP source
`45523f553b6efde243a2c783a9be1e62dea73ee5` and BEAM source
`7cfe9db137617605b1e0c256ca09c259e59393a8`, with SDK build IDs
`50ab237b91ca52ff2604dad4c3c251880e163fa2b436f54ba2d8cb0131df2098` (EMU) and
`e62c2198da47c5ae96c95e1789534dd0bc0968758e033d727eff5d671be82a86` (JIT).
Rebar3 was 3.27.0; the native build used CMake 4.2.3 and GCC 15.2.0.
Both projects built from independent source copies. Plugin help and greeting
passed in a separate consumer; NIF EUnit and execution from an extracted archive
passed. Clean hooks and disposable-copy cleanup also passed. These checks did
not retry or alter the release blocker above.

The current workflows pass Actionlint 1.7.7; Python syntax, workflow shell syntax,
paths and whitespace have also been checked. These are structural checks only.
GitHub runtime execution remains pending the setup action and distribution
artifacts. There are no macOS or Windows runtime results.

`umbrella` is an alias of the Rebar3 release template, so it has no separate
example. The NIF example uses a small CMake project in place of the GNU Make
scaffold generated by the template named `cmake`.
