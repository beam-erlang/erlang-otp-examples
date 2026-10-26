-module(ping_pong_handler).
-export([init/2]).
init(Req, State) ->
    Reply = case cowboy_req:method(Req) of
        <<"GET">> -> cowboy_req:reply(200, #{<<"content-type">> => <<"text/plain">>}, <<"pong">>, Req);
        _ -> cowboy_req:reply(405, #{<<"allow">> => <<"GET">>}, <<>>, Req)
    end,
    {ok, Reply, State}.
