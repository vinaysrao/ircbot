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

import helpers
import sys
from nltk.corpus import wordnet


def privmsg( bot, line, socket ):
    if 'ping' in line.lower() and bot.nick in line:
        nick = helpers.getnick( line.split()[ 0 ] )
        if nick:
            bot.privmsg( nick  + ': Pong' )


def pong( bot, line, socket ):
    bot.pongToServer( line )


def action( bot, line, socket ):
	if 'kick' in line.lower() and bot.nick in line:
		bot.privmsg( 'Ow' )
		msg = chr( 1 ) + "ACTION kicks " + helpers.getnick( line ) + " back" + chr( 1 )
		bot.privmsg( msg )

	if 'hugs' in line.lower() and bot.nick in line:
		msg = chr( 1 ) + "ACTION hugs " + helpers.getnick( line ) + chr( 1 )
		bot.privmsg( msg )

	if 'kills' in line.lower() and bot.nick in line:
		msg = chr( 1 ) + "ACTION is a zombie." + chr( 1 )
		bot.privmsg( msg )
		msg = helpers.getnick( line ) + ': X|'
		bot.privmsg( msg )

	if 'yawns' in line.lower():
		msg = chr( 1 ) + "ACTION yawns" + chr( 1 )
		bot.privmsg( msg )


def command( bot, line, socket ):
	#This is run if the bot's command symbol, by default '!' is found
	command, commandstring = helpers.getCmdAndCmdString( line )
	command = command.lower()
	if command == '':
		return
	if command in [ 'say', 'echo' ]:
		bot.privmsg( commandstring )

	if command in [ 'topic' ]:
		msg = helpers.prependNick( commandstring )
		bot.privmsg( msg + "Topic is: " + bot.channeltopic )

	if command in [ 'yourcode' ]:
		msg = helpers.prependNick( commandstring )
		msg += 'https://github.com/vinaysrao/ircbot.git'
		bot.privmsg( msg )

	if command in [ 'god' ]:
		msg = helpers.prependNick( commandstring )
		msg += 'http://www.youtube.com/watch?v=8nAos1M-_Ts'
		bot.privmsg( msg )

	if command in [ 'addnick' ]:
		nick = helpers.getnick( line )
		if commandstring == '' or len( commandstring.split() ) > 1:
			return
		if helpers.isAdmin( bot, nick ):
			if bot.addKnownNick( commandstring ):
				bot.privmsg( commandstring + ' added to known nicks' )

	if command in [ 'kick' ]:
		msg = chr( 1 ) + "ACTION kicks " + commandstring + chr( 1 )
		bot.privmsg( msg )

	if command in [ 'lmgtfy' ]:
		if commandstring == '':
			return
		query = commandstring.split( ' ', 1 )
		if helpers.isNewNick( query[ 0 ], bot.activeNickList ):
			msg = ''
			query = '+'.join( query )
		else:
			msg = query[ 0 ] + ': '
			query = '+'.join( query[ 1: ] )

		query = '+'.join( query.split() )
		url = 'http://www.lmgtfy.com/?q=' + query
		msg += url
		bot.privmsg( msg )

	if command in [ 'define' ]:
		s = wordnet.synsets( commandstring )
		try:
			msg = s[ 0 ].definition.capitalize()
		except:
			msg = 'Definition not found'
		if commandstring == 'god':
			msg = "\' \'"
		bot.privmsg( msg )


	if command in [ 'quit' ]:
		if( helpers.isAdmin( bot, helpers.getnick( line ) ) ):
			bot.serializeNicks()
			__import__( 'sys' ).exit( 0 )

	if command in [ 'restart' ]:
		if( helpers.isAdmin( bot, helpers.getnick( line ) ) ):
			bot.serializeNicks()
			__import__( 'sys' ).exit( 1 )

	if command in [ 'list' ]:
		msg = helpers.prependNick( commandstring )
		msg += ', '.join( helpers.commandList() )
		bot.privmsg( msg )

	if command == 'togglewelcome':
		if( helpers.isAdmin( bot, helpers.getnick( line ) ) ):
			bot.welcome_new = not bot.welcome_new
			msg = 'Bot\'s welcome mode: %s' % bot.welcome_new


def nameList( bot, line, socket ):
	if bot.nick + ' @' in line:
		bot.activeNickList = []
		msg = helpers.getMsg( line )
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
	msg = helpers.getMsg( line )
	bot.setChannelTopic( msg )


def join( bot, line, socket ):
	import re
	nick = re.search( ':(.*)!', line )
	if not bot.welcome_new:
		return
	if nick:
		nick = nick.group( 1 )
		if helpers.isNewNick( nick, bot.nameslist ) and nick != bot.nick:
			msg = nick + ': '
			msg += 'Hi! Looks like you\'re new here. This is the IRC Channel of the \"BMS - Libre User Group\".'
			bot.privmsg( msg )
			msg = nick + ': '
			msg +=  'If you don\'t receive a reply immediately, stick around; someone will get to you eventually.'
			bot.privmsg( msg )
			bot.addNames( [ nick ] )
