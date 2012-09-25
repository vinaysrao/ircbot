import bot

if __name__ == "__main__":
    bot = IRCBot()
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