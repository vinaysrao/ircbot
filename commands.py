# Copyright (C) 2012 Vinay.S.Rao <sr.vinay@gmail.com>

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

commandlist = []

class Command:
	'''Inherit this class and define commands that define the following methods'''
	def __init__( self, bot = None, command = '', usage_format = '' ):
		self.command = command
		self.bot = bot
		self.usage_format = usage_format
		global commandlist
		commandlist.append( self )


	def usage( self ):
		return self.usage_format

	def setBot( self, bot ):
		self.bot = bot

	def command_string( self ):
		return self.command

	def handler( self, command_string ):
		'''What must be done when this command is found'''
		self.bot.privmsg( command_string )


class WebQuery( Command ):
	def __init__( self, bot = None, command = '', usage_format = '', url = '' ):
		Command.__init__( self, bot, command,  usage_format )
		self.url = url

	def handler( self, command_string ):
		if command_string == '':
			return
		query = command_string.split( ' ', 1 )
		if helpers.isNewNick( query[ 0 ], bot.activeNickList ):
			msg = ''
			query = '+'.join( query )
		else:
			msg = query[ 0 ] + ': '
			query = '+'.join( query[ 1: ] )

		query = '+'.join( query.split() )
		url = self.url + query
		msg += url
		self.bot.privmsg( msg )


class SingleEchoCommand( Command ):
	def __init__( self, bot = None, command = '', usage_format = '', echo_message = '' ):
		Command.__init__( self, bot, command, usage_format )
		self.echo_message = echo_message

	def handler( self, command_string ):
		msg = helpers.prependNick( command_string )
		msg += self.echo_message
		self.bot.privmsg( msg )


class Toggle( Command ):
	def __init__( self, bot = None, command = '', usage_format = '', toggle_variable = None ):
		Command.__init__( self, bot, command, usage_format )
		self.toggle_variable = toggle_variable

	def handler( self, command_string ):
		vars( self.bot )[ self.toggle_variable ] = not vars( self.bot )[ self.toggle_variable ]
		msg = 'Bot\'s %s mode: %s' % ( self.toggle_variable, vars( self.bot )[ self.toggle_variable ] )
		self.bot.privmsg( msg )



#START: Objects creation
say = Command( command = 'say' )

google = WebQuery( command = 'google', url = 'https://www.google.com/search?q=' )
lmgtfy = WebQuery( command = 'lmgtfy', url = 'http://www.lmgtfy.com/?q=' )

yourcode = SingleEchoCommand( command = 'say', echo_message = 'https://github.com/vinaysrao/ircbot.git' )
god = SingleEchoCommand( command = 'god', echo_message = 'http://www.youtube.com/watch?v=8nAos1M-_Ts' )
listcommands = SingleEchoCommand( command = 'list', echo_message = helpers.commandList() )

quiet = Toggle( command = 'quiet', toggle_variable = 'quiet' )
welcome = Toggle( command = 'welcome', toggle_variable = 'welcome_new' )