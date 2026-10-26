-module(ping_pong_client).
-export([main/1, parse_url/1]).
main(Args) ->
    Status = case Args of
        ["--help"] -> io:format("Usage: ping-pong-client http://HOST:PORT/ping~n"), 0;
        [Url] ->
            case parse_url(Url) of
                {ok, Host, Port, Path} -> request(Host, Port, Path);
                error -> fail("Expected one complete HTTP URL", 2)
            end;
        _ -> fail("Usage: ping-pong-client http://HOST:PORT/ping", 2)
    end,
    init:stop(Status),
    receive after 10000 ->
        io:format(standard_error, "Shutdown timed out~n", []), erlang:halt(1)
    end.
parse_url(Url) ->
    try case uri_string:parse(Url) of
        #{scheme := "http", host := Host} = Parts when Host =/= [] ->
            false = maps:is_key(userinfo, Parts),
            false = maps:is_key(fragment, Parts),
            Port = maps:get(port, Parts, 80),
            true = is_integer(Port) andalso Port > 0 andalso Port =< 65535,
            Path0 = maps:get(path, Parts, "/"),
            Path = case Path0 of [] -> "/"; _ -> Path0 end,
            Target = case maps:find(query, Parts) of {ok,Q} -> Path ++ "?" ++ Q; error -> Path end,
            {ok, Host, Port, Target};
        _ -> error
    end catch _:_ -> error end.
request(Host, Port, Path) ->
    try
        {ok, _} = application:ensure_all_started(gun),
        {ok, Conn} = gun:open(Host, Port, #{transport => tcp, protocols => [http], retry => 0, connect_timeout => 5000}),
        try
            {ok, http} = gun:await_up(Conn, 5000),
            Stream = gun:get(Conn, Path),
            {response, nofin, 200, Headers} = gun:await(Conn, Stream, 5000),
            {<<"content-type">>, <<"text/plain">>} = lists:keyfind(<<"content-type">>, 1, Headers),
            {ok, <<"pong">>} = gun:await_body(Conn, Stream, 5000),
            io:format("pong~n"), 0
        after gun:close(Conn) end
    catch Class:Reason ->
        io:format(standard_error, "Request failed: ~p:~p~n", [Class, Reason]), 1
    end.
fail(Message, Code) -> io:format(standard_error, "~s~n", [Message]), Code.
