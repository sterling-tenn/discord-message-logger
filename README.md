discord message logger

receives events from discord's gateway (wss://gateway.discord.gg/?v=8&encoding=json"
from the events, filters out the channel id, and the content of the message
does not currently support logging embeds, outpu will be empty
