%%%-------------------------------------------------------------------
%% @doc example_release public API
%% @end
%%%-------------------------------------------------------------------

-module(example_release_app).

-behaviour(application).

-export([start/2, stop/1]).

start(_StartType, _StartArgs) ->
    example_release_sup:start_link().

stop(_State) ->
    ok.

%% internal functions
