-module(ping_pong_server_app).
-behaviour(application).
-export([start/2, stop/1]).
start(_Type, _Args) ->
    Port = case os:getenv("PING_PONG_PORT") of
        false -> 8080;
        Value ->
            try list_to_integer(Value) of
                N when N >= 0, N =< 65535 -> N;
                _ -> error({invalid_port, Value})
            catch error:badarg -> error({invalid_port, Value}) end
    end,
    Dispatch = cowboy_router:compile([{'_', [{"/ping", ping_pong_handler, []}]}]),
    case cowboy:start_clear(ping_pong_listener,
            [{ip, {127,0,0,1}}, {port, Port}], #{protocols => [http], env => #{dispatch => Dispatch}}) of
        {ok, _} ->
            case ping_pong_server_sup:start_link() of
                {ok, _} = Result ->
                    io:format("Listening on http://127.0.0.1:~B/ping~n", [ranch:get_port(ping_pong_listener)]),
                    Result;
                Error -> cowboy:stop_listener(ping_pong_listener), Error
            end;
        Error -> Error
    end.
stop(_State) -> cowboy:stop_listener(ping_pong_listener), ok.
