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

import socket
import re
import sys
import rules
import helpers
import time

class IRCBot():
    #A simple IRC Bot that pongs et all
    #Requires a call to 'run' to start
    lastline = ''
    rules = {}
    def __init__( self, host = 'irc.freenode.net', channel = '#bmslug', nick = 'bmsbot', port = 6667, symbol = '!' ):
        self.host = host
        self.channel = channel
        self.nick = nick
        self.port = port
        self.symbol = symbol
        self.channeltopic = ''
        self.socket = socket.socket()
        self.maxlength = 2048
        self.timer = time.time()

    	self.nameslist = helpers.readNicksFromFile( 'known_nicks.txt' )
        self.admins = helpers.readNicksFromFile( 'admins.txt' )
        self.activeNickList = []
        
        self.initConnection()
    
    
    def initConnection( self ):
        try:
            self.socket.connect( ( self.host, self.port ) )
            self.socket.send( "USER " + self.nick + " " + self.nick + " " + self.nick + " :bmsbot\n" )
            self.socket.send( "NICK " + self.nick + "\r\n" )
            self.socket.send( "JOIN " + self.channel + "\r\n" )
        except:
            print sys.exc_info()[ 0 ]
        
        
    def getnicklist( self ):
        self.socket.send( "NAMES " + self.channel + "\r\n" )
        #Implement parsing this
        
    def readlines( self ):
        data = self.lastline + self.socket.recv( self.maxlength )
        lines = data.split( "\r\n" )
        self.lastline = lines.pop()
        return lines

    def run( self ):
        while True:
            if time.time() - self.timer > 180: #Tries to reconnect to server on loss of connectivity
                self.initConnection()

            lines = self.readlines()
            for line in lines:
                print line
                self.parseline( line )


    def addrule( self, rule, callback ):
        if rule in self.rules.keys():
            self.rules[ rule ].append( callback )
        else:
            self.rules[ rule ] = [ callback ]


    def parseline( self, line ):
        for rule in self.rules:
            if line.find( rule ) != -1:
                for cb in self.rules[ rule ]:
                    cb( self, line, self.socket )

        
    
    def pongToServer( self, msg ):
        #Check if "PING :" is in 'line' and call pongToServer
        self.timer = time.time()
        pingcmd = msg.split( ":", 1 )
        pingmsg = pingcmd[ 1 ]
        self.socket.send( "PONG :" + pingmsg + "\r\n" )


    def privmsg( self, msg ):
        if msg == '':
            return
        self.socket.send( "PRIVMSG " + self.channel + " :" + msg + "\r\n" )

    
    def setChannelTopic( self, channeltopic ):
        self.channeltopic = channeltopic


    def addNames( self, nameslist ):
        self.activeNickList.extend( [ i for i in nameslist if i not in self.activeNickList ] )


    def addKnownNick( self, nick ):
        if helpers.isNewNick( nick, self.nameslist ):
            self.nameslist.append( nick )
            return True
        return False


    def serializeNicks( self ):
        helpers.serializeNicks( 'known_nicks.txt', self.namelist )
        helpers.serializeNicks( 'admins.txt', self.admins )



if __name__ == "__main__":
    bot = IRCBot( nick = 'bmsbotbot' )
    bot.addrule( 'PRIVMSG', rules.privmsg )
    bot.addrule( 'PING :', rules.pong ) #Special case, to pong back to the server only
    bot.addrule( 'ACTION', rules.action )
    bot.addrule( 'JOIN', rules.join )
    bot.addrule( bot.symbol, rules.command )
    bot.addrule( '353', rules.nameList )
    bot.addrule( '332', rules.topic )
    bot.run()
