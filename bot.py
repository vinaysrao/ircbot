import socket
import re

class IRCBot:
    #A simple IRC Bot that pongs et all
    #Requires a call to 'run' to start

    def __init__( self, host = 'irc.freenode.net', channel = '#bmslug', nick = 'bmsbot', port = 6667, symbol = '$'):
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
        self.socket.send( "USER " + NICK + " " + NICK + " " + NICK + " :bmsbot\n" )
        self.socket.send( "NICK " + NICK + "\r\n" )
        self.socket.send( "JOIN " + CHANNEL + "\r\n" )
        
        
    def nicklist( self ):
        self.socket.send( "NAMES " + CHANNEL + "\r\n" )
        #Implement parsing this
        
        
    def run( self ):
        while True:
            line = self.socket.recv( self.maxlength ).strip( "\r\n" )
            print line
    
    
    def pongToServer( self, msg ):
        #Check if "PING :" is in 'line' and call pongToServer
        pingcmd = msg.split( ":", 1 )
        pingmsg = pingcmd[ 1 ]
        self.socket.send( "PONG :" + pingmsg + "\r\n" )
    
    
    def privmsg( self, msg ):
        self.socket.send( "PRIVMSG " + CHANNEL + " :" + msg + "\r\n" )
        
        

if __name__ == "__main___":
    bot = IRCBot()
    bot.run()