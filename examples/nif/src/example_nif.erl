-module(example_nif).
-on_load(init/0).
-export([hello/0]).

init() ->
    erlang:load_nif(filename:join(code:priv_dir(example_nif), "example_nif"), 0).

hello() ->
    erlang:nif_error(nif_not_loaded).
