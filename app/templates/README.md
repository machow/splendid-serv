Splendid Server
===============

Game commands
-------------

draw: select a number of gems (e.g. "draw rgb" or "draw gg")
buy: buy a land (e.g. "buy 1 rggb" for land with id 1 and cost rggb)
reserve: reserve a land using <land_id> (e.g. "reserve 1")
noble: collect a noble

Warning codes
-------------

If an invalid command is submitted, the server returns a json object with
{error_code: <error_code>, value: <more_details>}

Codes -- 
1: player not in game attempted to make move (value is string)
101: taking gems produces defecit (value is neg gems)
102: can't draw two (value is valid draw2 options)
103: invalid draw type (e.g. even before checks. value is str)
104: can't buy land with gem amount (str)
105: tried to reserve land not on table or can't afford (str)
106: can't reserve more than 3 lands
110: player tries to move on wrong turn (value is string saying which player is up)
