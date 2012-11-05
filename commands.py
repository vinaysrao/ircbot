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

class Command:
	'''Inherit this class and define commands that define the following methods'''
	def __init__( self, command = '', usage_format = '' ):
		self.command = command
		self.usage_format = usage_format


	def usage( self ):
		return self.usage_format

	def command_string( self ):
		return self.command

	def handler( self, line, bot ):
		'''What must be done when this command is found'''
		pass


class WebQuery( Command ):
	def __init__( self, command = '', usage_format = '', url = '' ):
		Command.__init__( self, command,  usage_format )
		self.url = url

	def handler( self, line, bot ):
		if line == '':
			return
		query = line.split( ' ', 1 )
		if helpers.isNewNick( query[ 0 ], bot.activeNickList ):
			msg = ''
			query = '+'.join( query )
		else:
			msg = query[ 0 ] + ': '
			query = '+'.join( query[ 1: ] )

		query = '+'.join( query.split() )
		url = self.url + query
		msg += url
		bot.privmsg( msg )


google = WebQuery( command = 'google', url = 'https://www.google.com/search?q=' )
lmgtfy = WebQuery( command = 'lmgtfy', url = 'http://www.lmgtfy.com/?q=' )