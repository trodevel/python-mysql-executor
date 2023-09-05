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

import random
import db
import db_config
from aux_logger.aux_logger import create_timed_rotating_logger

db.set_logger( create_timed_rotating_logger( "logs/db", "db" ) )

##########################################################

def dump_res( name: str, res ):

    print( f"{name}: ", end="" )

    for s in res:
        print( f"{s}, ", end="" )

    print()

##########################################################

def my_db():
    return db.DB( db_config.USER, db_config.PASSWORD, db_config.HOST, db_config.MYDB, db_config.SQL_PATH )

##########################################################

def test_00():

    dbe = my_db()

##########################################################

def test_01():

    dbe = my_db()

    res = dbe.execute_query_from_file( "drop_table_users.sql" )

    dump_res( "test_01", res )

##########################################################

def test_02():

    dbe = my_db()

    res = dbe.execute_query_from_file( "create_table_users.sql" )

    dump_res( "test_02", res )

##########################################################

def test_03():

    dbe = my_db()

    res = dbe.execute_query_from_file( "tmpl_add_user.sql", { "ID": 1, "FIRSTNAME": "Test", "LASTNAME": "User" } )

    dump_res( "test_03", res )

##########################################################

def test_04():

    dbe = my_db()

    id = random.randint( 1, 100 )

    res = dbe.execute_query_from_file( "tmpl_add_user.sql", { "ID": id, "FIRSTNAME": f"Test_{id}", "LASTNAME": f"User_{id}" } )

    dump_res( "test_04", res )

##########################################################

def test_05():

    dbe = my_db()

    id = random.randint( 1, 100 )

    res = dbe.execute_query_from_file( "tmpl_add_user.sql", { "ID": id, "FIRSTNAME": f"Test_{id}", "LASTNAME": f"User_{id}" } )

    dump_res( "test_05", res )

##########################################################

def test_06():

    dbe = my_db()

    res = dbe.execute_query_from_file( "show_table_users.sql" )

    dump_res( "test_06", res )

##########################################################

def test_07():

    dbe = my_db()

    res = dbe.execute_query_from_file( "show_table_users_as_json.sql" )

    dump_res( "test_07", res )

##########################################################

def test():

    test_00()
    test_01()
    test_02()
    test_03()
    test_04()
    test_05()
    test_06()
    test_07()

##########################################################

if __name__ == "__main__":
   test()
