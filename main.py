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


import bot
import rules
import sys

if __name__ == "__main__":
    bot = bot.IRCBot( password = sys.argv[ 1 ] )
    #--START-- of main rules
    bot.addrule( 'PRIVMSG', rules.privmsg )
    bot.addrule( 'PING :', rules.pong ) #Special case, to pong back to the server only
    bot.addrule( 'ACTION', rules.action )
    bot.addrule( 'JOIN', rules.join )
    bot.addrule( bot.symbol, rules.command )
    bot.addrule( '353', rules.nameList )
    bot.addrule( '332', rules.topic )
    #--END-- of main rules
    #Add custom rules below
    bot.run()
