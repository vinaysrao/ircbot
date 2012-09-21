# Copyright (C) 2012 Vinay.S.Rao <sr.vinay@gmail.com>
# Copyright (C) 2012 Deepak Mittal <dpac.mittal2@gmail.com>

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