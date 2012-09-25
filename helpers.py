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

def readNicksFromFile( filename ):
	return [ f for f in open( filename ) ]


def serializeNicks( filename, nameslist ):
	file = open( filename, 'w' )
	for i in nameslist:
        file.write( i + '\n' )
    file.close()


def getnick( user ):
        m = re.match( ":(.*?)!~", user )
        if m:
            return m.group( 1 )
        else:
            return False


def getMsg( line ):
    x = line.split( ':', 2 )
    if len( x ) < 3:
        return ' '
    return x[ 2 ] 


def getCmdAndCmdString( self, line ):
    #Returns a tuple, containing the command and the command
    #string as its members
    line = getMsg( line )
    if line[ 0 ] != '!':
        return ( '' , '' )

    m = re.match( r'!(.+?)\b\s?(.*)$' , line )
    if m:
        return m.groups( '' )
    else:
        return ( '' , '' )
