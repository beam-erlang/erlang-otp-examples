-module(ping_pong_client_tests).
-include_lib("eunit/include/eunit.hrl").
url_test() ->
    ?assertEqual({ok,"localhost",8080,"/ping"}, ping_pong_client:parse_url("http://localhost:8080/ping")),
    [?assertEqual(error, ping_pong_client:parse_url(U)) || U <- ["x", "https://localhost/ping", "http://localhost:0/ping", "http://user@localhost/ping"]].
