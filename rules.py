# Copyright (C) 2012 Vinay.S.Rao <sr.vinay@gmail.com>
# Copyright (C) 2012 Deepak Mittal <dpac.mittal2@gmail.com>
# Copyright (C) 2012 Shantanu Tushar <shantanu@kde.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
	#This is run if the bot's command symbol, by default '!' is found
	command, commandstring = bot.getCmdAndCmdString( line )
	command = command.lower()
	if command == '':
		return
	if command in [ 'say', 'echo' ]:
		bot.privmsg( commandstring )

	if command in [ 'topic' ]:
		msg = prependNick( bot, commandstring )
		bot.privmsg( msg + "Topic is: " + bot.channeltopic )

	if command in [ 'yourcode' ]:
		msg = prependNick( bot, commandstring )
		msg += 'https://github.com/vinaysrao/ircbot.git'
		bot.privmsg( msg )

	if command in [ 'god' ]:
		msg = prependNick( bot, commandstring )
		msg += '\'  \''
		bot.privmsg( msg )

	if command in [ 'addnick' ]:
		nick = bot.getnick()
		if commandstring == '' or ' ' in commandstring:
			return
		if not isNewNick( nick, bot.nameslist ):
			bot.addKnownNick( commandstring )


	if command in [ 'quit' ]:
		bot.serializeNicks()
		__import__( 'sys' ).exit( 0 )

	if command in [ 'restart' ]:
		bot.serializeNicks()
		__import__( 'sys' ).exit( 1 )

def nameList( bot, line, socket ):
	if bot.nick + ' @' in line:
		msg = bot.getMsg( line )
		nameslist = []
		for i in msg.split():
			if i == bot.nick:
				continue
			if i == '366':
				nameslist.pop()
				break
			nameslist.append( i )
		bot.addNames( nameslist )


def topic( bot, line, socket ):
	msg = bot.getMsg( line )
	bot.setChannelTopic( msg )


def join( bot, line, socket ):
	import re
	nick = re.search( ':(.*)!', line )
	if nick:
		nick = nick.group( 1 )
		if isNewNick( nick, bot.nameslist ) and nick != bot.nick:
			msg = nick + ': '
			msg += 'Hi! Looks like you\'re new here. This is the IRC Channel of the \"BMS - Libre User Group\".'
			bot.privmsg( msg )
			msg = nick + ': '
			msg +=  'If you don\'t receive a reply immediately, stick around; someone will get to you eventually.'
			bot.privmsg( msg )
			bot.addNames( [ nick ] )


def prependNick( bot, nick ):
	if nick != '' and nick in bot.nameslist:
		msg = nick + ': '
	else:
		msg = ''
	return msg


def isNewNick( nick, nameslist ):
	import re
	for i in nameslist:
		if re.match( '[@,_]?' + i + '_?', nick ):
			return False
	return True