-module(example_app_tests).
-include_lib("eunit/include/eunit.hrl").
lifecycle_test() ->
    {ok, _} = application:ensure_all_started(example_app),
    Pid = whereis(example_app_sup),
    ?assert(is_pid(Pid)),
    Ref = monitor(process, Pid),
    ok = application:stop(example_app),
    receive {'DOWN', Ref, process, Pid, _} -> ok after 5000 -> error(stop_timeout) end,
    ?assertEqual(undefined, whereis(example_app_sup)).
