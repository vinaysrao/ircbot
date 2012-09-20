import socket
import re

class IRCBot:
    #A simple IRC Bot that pongs et all
    #Requires a call to 'run' to start
    lastline = ''
    rules = {}
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
                self.parseline( line )
                
                """
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
                """

    def addrule( self, rule, callback):
        if rule in self.rules.keys():
            self.rules[ rule ].append(callback)
        else:
            self.rules[ rule ] = [ callback ]


    def parseline( self, line ):
        for rule in self.rules:
            if line.find(rule) != -1:
                for cb in self.rules[rule]:
                    cb( line, self.socket )

        
    
    def pongToServer( self, msg ):
        #Check if "PING :" is in 'line' and call pongToServer
        pingcmd = msg.split( ":", 1 )
        pingmsg = pingcmd[ 1 ]
        self.socket.send( "PONG :" + pingmsg + "\r\n" )
    
    
    def privmsg( self, msg, user='' ):
        if user == '':
            self.socket.send( "PRIVMSG " + self.channel + " :" + msg + "\r\n" )
        else:
            self.socket.send( "PRIVMSG " + self.channel + " :" + user + ": " + msg + "\r\n" )
        

def privmsg( line, socket ):
    print 'received privmsg'


def privmsg2( line, socket ):
    print 'received privmsg2'    

if __name__ == "__main__":
    bot = IRCBot()
    bot.addrule( 'PRIVMSG', privmsg )
    bot.addrule( 'PRIVMSG', privmsg2)
    bot.run()
    

