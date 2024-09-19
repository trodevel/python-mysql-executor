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
import re

from python_mysql_executor.tokenize import tokenize
from python_mysql_executor.prepare_value import prepare_value
from python_mysql_executor.exceptions import IOErrorException, RuntimeException

class MyLogger:
    _logger = None

    def __init__( self ):
        self._logger = None

    def set_logger( self, logger ):
        self._logger = logger

    def critical( self, v ):
        if not self._logger:
            return
        self._logger.critical( v )

    def error( self, v ):
        if not self._logger:
            return
        self._logger.error( v )

    def debug( self, v ):
        if not self._logger:
            return
        self._logger.debug( v )

logger = MyLogger()

def set_logger( l ):
    global logger
    logger.set_logger( l )

class DB:

    cnx     = None

    def __init__(self, user: str, password: str, host: str, db: str, sql_path: str, must_quit_on_error: bool = False):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.sql_path = sql_path
        self.is_query_debug = False
        self.must_quit_on_error = must_quit_on_error

    def set_query_debug( self, v: bool ) -> None:
        self.is_query_debug = v

    def execute_query_from_file( self, filename: str, template_params: dict = {} ):

        sql_commands = self._load_sql_commands( filename, template_params )

        return self._auto_execute_sql_commands( sql_commands )

    def execute_query( self, query_template: str, template_params: dict = {} ):

        sql_commands = self._init_template_and_cleanup_and_include_source_to_sql( query_template, template_params )

        return self._auto_execute_sql_commands( sql_commands )

    def _auto_execute_sql_commands( self, sql_commands ):

        self._connect_db()

        res = self._execute_sql_commands( sql_commands )

        self.cnx.close()

        return res

    def _replace_params( query: str, template_params: dict ) -> str:

        if len( template_params ) == 0:
            return query

        res = query

        for k, v in template_params.items():
            res = res.replace( f'%{k}%', prepare_value( v ) )
            #logger.debug( f"replace_param: %{k}% -> {v}" )

        return res

    def _connect_db(self) -> None:

        try:
            self.cnx = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                db=self.db )

        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.critical("Something is wrong with your user name or password")
            if self.must_quit_on_error: quit()
            raise IOErrorException( "Something is wrong with your user name or password" )
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.critical("Database does not exist")
            if self.must_quit_on_error: quit()
            raise IOErrorException( "Database does not exist" )
          else:
            logger.critical(err)
            if self.must_quit_on_error: quit()
            raise RuntimeError( err )
        else:
            self.cnx.get_warnings = True

    def _adjust_filename( self, filename: str ) -> str:

        if self.sql_path:
            return self.sql_path + "/" + filename

        return filename

    def _load_sql_commands( self, filename_raw: str, template_params: dict ):

        logger.debug( f"load_sql_commands: {filename_raw}" )

        filename = self._adjust_filename( filename_raw )

        return self._load_sql_commands_adjusted( filename, template_params )

    def _load_sql_commands_adjusted( self, filename: str, template_params: dict ):

        logger.debug( f"load_sql_commands_adjusted: {filename}" )

        query_template = open( filename, "r" ).read()

        return self._init_template_and_cleanup_and_include_source_to_sql( query_template, template_params )

    def _add_aux_params( self, template_params: dict ) -> dict:
        res = template_params
        res['QUERY_DEBUG'] = self.is_query_debug
        return res

    def _init_template_and_cleanup_and_include_source_to_sql( self, query_template: str, template_params_in: dict ):

        template_params = self._add_aux_params( template_params_in )

        query = DB._replace_params( query_template, template_params )

        logger.debug( f"query: {query}" )

        res = self._cleanup_and_include_source_to_sql( query, template_params )

        return res

    @staticmethod
    def _remove_comments( s: str ) -> str:
        """Removes comments starting with "^\s*#.*$" regex from a string.
        """

        # Use the re.sub function to replace all matches of the regex with an empty string
        return re.sub(r"^\s*#.*$", "", s, flags=re.MULTILINE)

    def _cleanup_and_include_source_to_sql( self, query, template_params ):

        sql_commands = tokenize( query, ';' )

        res = []

        for command in sql_commands:
            cc = command.strip()

            c = DB._remove_comments(cc)

            print( f"DEBUG: cc {cc} -> c{c}" )

            if c != '':
                first_word = c.split()[0].lower()
                if first_word == "source":
                    filename = c.split()[1]
                    res += self._load_sql_commands( filename, template_params )
                else:
                    res.append( c )

        return res

    def _execute_sql_commands( self, sql_commands ):

        data = []

        cursor = self.cnx.cursor()

        self.cnx.commit()

        for command in sql_commands:
            try:
                c = command.strip()
                if c != '':
                    #print( "DEBUG: executing '{}'".format( c ) )
                    cursor.execute( c )
                    result = cursor.fetchall()
                    #print( "DEBUG: command: '{}' res size {}".format( c, len( result ) ) )
                    if len( result ) == 0:
                        continue
                    row = []
                    for v in result:
                        row.append( v )
                    data.append( row )
            except IOError as e:
                logger.error( "execute_sql_commands: command skipped: {}, error {}".format( c, e ) )
                raise IOErrorException( f"command {c}, error {e}" )
            except Exception as e:
                logger.error( "execute_sql_commands: command skipped: {}, error {}".format( c, e ) )
                raise RuntimeException( f"command {c}, error {e}" )

        self.cnx.commit()

        logger.debug( "fetch warnings: {}".format( cursor.fetchwarnings() ) )

        cursor.close()

        return data
