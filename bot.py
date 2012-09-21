import socket
import re
from rules import *

class IRCBot:
    #A simple IRC Bot that pongs et all
    #Requires a call to 'run' to start
    lastline = ''
    rules = {}
    def __init__( self, host = 'irc.freenode.net', channel = '#bmslug', nick = 'bmsbot', port = 6667, symbol = '$' ):
        self.host = host
        self.channel = channel
        self.nick = nick
        self.port = port
        self.symbol = symbol
        self.socket = socket.socket()
        self.maxlength = 2048
        
        self.initConnection()
    
    
    def initConnection( self ):
        self.socket.connect( ( self.host, self.port ) )
        self.socket.send( "USER " + self.nick + " " + self.nick + " " + self.nick + " :bmsbot\n" )
        self.socket.send( "NICK " + self.nick + "\r\n" )
        self.socket.send( "JOIN " + self.channel + "\r\n" )
        
        
    def nicklist( self ):
        self.socket.send( "NAMES " + self.channel + "\r\n" )
        #Implement parsing this
        
    def readlines( self ):
        data = self.lastline + self.socket.recv( self.maxlength )
        lines = data.split( "\r\n" )
        self.lastline = lines.pop()
        return lines

    def run( self ):
        while True:
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
        pingcmd = msg.split( ":", 1 )
        pingmsg = pingcmd[ 1 ]
        self.socket.send( "PONG :" + pingmsg + "\r\n" )


    def privmsg( self, msg ):
        self.socket.send( "PRIVMSG " + self.channel + " :" + msg + "\r\n" )

    
    def getnick( self, user ):
        m = re.match( ":(.*?)!~", user )
        if m:
            return m.group( 1 )
        else:
            return False


    def getMsg( self, line ):
        return line.split( ':', 2 )[ 2 ]


    def getCmdAndCmdString( self, line ):
        #Returns a tuple, containing the command and the command
        #string as its members
        command = line[ 1: ].split()[ 0 ]
        end = re.search( command, line ) + 1
        commandstring = line[ end: ]
        return ( command, commandstring )



if __name__ == "__main__":
    bot = IRCBot()
    bot.addrule( 'PRIVMSG', privmsg )
    bot.addrule( 'PING :', pong ) #Special case, to pong back to the server only
    bot.addrule( 'ACTION', action )
    bot.run()