def privmsg( bot, line, socket ):
    if 'ping' in line.lower() and bot.nick in line:
        nick = bot.getnick( line.split() [ 0 ] )
        if nick:
            bot.privmsg( nick  + ': Pong' )


def pong( bot, line, socket ):
    bot.pongToServer( line )


def action( bot, line, socket ):
	if 'kick' in line.lower():
		bot.privmsg( 'Ow' )