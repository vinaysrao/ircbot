def privmsg( line, socket ):
    if line.lower().find( 'ping' ) != -1 and line.find( bot.nick ) != -1:
        nick = bot.getnick( line.split() [ 0 ] )
        if nick:
            bot.privmsg( nick  + ': pong' )
        else:
            bot.privmsg( 'pong' )


def pong( line, socket ):
    bot.pongToServer( line )