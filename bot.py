import socket
import re

class IRCBot:
    #A simple IRC Bot that pongs et all
    #Requires a call to 'run' to start
    lastline = ''
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
                print "Newline:::: " + line

                #Ping from server
                if ( "PING :" in line ):
                    self.pongToServer( line )
                    
                if ( "ACTION" in line ):
                    #parse Action
                    pass
                
                if( " PRIVMSG " in line ):
                    #Normal messages to channel
                    msg = line.split( ':', 2 )[ 2 ] #What was said
                    nick = re.match( ":(.*?)!~", line ).group( 1 ) #nick who said this
                    
                    if re.search( 'ping', msg, re.IGNORECASE ):
                        self.privmsg( nick + ": Pong" )
                    pass
        
    
    def pongToServer( self, msg ):
        #Check if "PING :" is in 'line' and call pongToServer
        pingcmd = msg.split( ":", 1 )
        pingmsg = pingcmd[ 1 ]
        self.socket.send( "PONG :" + pingmsg + "\r\n" )
    
    
    def privmsg( self, user='', msg ):
        if user == '':
            self.socket.send( "PRIVMSG " + self.channel + " :" + msg + "\r\n" )
        else:
            self.socket.send( "PRIVMSG " + self.channel + " :" + user + ": " + msg + "\r\n" )
        
        

if __name__ == "__main__":
    bot = IRCBot()
    bot.run()