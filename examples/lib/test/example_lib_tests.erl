-module(example_lib_tests).
-include_lib("eunit/include/eunit.hrl").
hello_test() -> ?assertEqual(<<"Hello, world!">>, example_lib:hello()).
