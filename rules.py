

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


def command( bot, line, socket ):
	#This is run if the bot's command symbol, by default '$' is found
	command, commandstring = bot.getCmdAndCmdString( line )
	if command == '':
		return
	if command in [ 'say', 'echo' ]:
		bot.privmsg( commandstring )

	if command in [ 'topic' ]:
		if commandstring != '':
			msg = commandstring + ': '
		else:
			msg = ''
		bot.privmsg( msg + "Topic is: " + bot.channeltopic )


def nameList( bot, line, socket ):
	if bot.nick + ' @' in line:
		msg = bot.getMsg( line )
		for i in msg.split():
			print i,


def topic( bot, line, socket ):
	msg = bot.getMsg( line )
	bot.setChannelTopic( msg )