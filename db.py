#!/usr/bin/python3

'''
Python MySQL Executor.

Copyright (C) 2023 Dr. Sergey Kolevatov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

'''

import mysql.connector
from mysql.connector import errorcode

import db_config
import tokenize

logger  = None

class DB:

    cnx     = None

    def execute_query_from_file( self, filename ):

        query = open( filename, "r" ).read()

        return self.execute_query( query )

    def execute_query( self, query ):

        self.cnx = connect_db()

        res = self._execute_query( query )

        self.cnx.close()

        return res

    def _auto_execute_query( self, query, template_params: dict ):

        self.cnx = connect_db()

        res = self._execute_query( query )

        self.cnx.close()

        return res

    def _replace_params( query: str, template_params: dict ) -> str:

        if len( template_param ) == 0:
            return query

        res = query

        for k, v in template_params.items():
            res.replace( f'%{k}%', str( v ) )

        return res

    def _connect_db(self):

        try:
            self.cnx = mysql.connector.connect(
                user=db_config.USER,
                password=db_config.PASSWORD,
                host=db_config.HOST,
                db=db_config.MYDB )

        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.critical("Something is wrong with your user name or password")
            quit()
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.critical("Database does not exist")
            quit()
          else:
            logger.critical(err)
            quit()
        else:
            self.cnx.get_warnings = True

    def _load_query( filename ):

        logger.debug( "load_query: {}".format( filename ) )

        query = open( filename, "r" ).read()

        res = _cleanup_and_include_source_to_sql( query )

        return res


    def _cleanup_and_include_source_to_sql( self, query ):

        sql_commands = tokenize.tokenize( query, ';' )

        res = []

        for command in sql_commands:
            c = command.strip()
            if c != '':
                first_word = c.split()[0].lower()
                if first_word == "source":
                    filename = c.split()[1]
                    res += self._load_query( filename )
                else:
                    res.append( c )

        return res

    def _execute_query( self, query ):

        sql_commands = self._cleanup_and_include_source_to_sql( query )

        data = []

        cursor = self.cnx.cursor()

        for command in sql_commands:
            try:
                c = command.strip()
                if c != '':
                    #print( "DEBUG: executing '{}'".format( c ) )
                    cursor.execute( c )
                    result = cursor.fetchall()
                    #print( "DEBUG: command: '{}' res size {}".format( c, len( result ) ) )
                    for v in result:
                        data.append( v )
            except IOError as e:
                logger.error( "execute_query: command skipped: {}, error {}".format( c, e ) )
            except Exception as e:
                logger.error( "execute_query: command skipped: {}, error {}".format( c, e ) )

        self.cnx.commit()

        logger.debug( "fetch warnings: {}".format( cursor.fetchwarnings() ) )

        cursor.close()

        return data
