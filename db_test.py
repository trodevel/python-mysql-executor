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
from externals.aux_logger.aux_logger import create_timed_rotating_logger

db.logger = create_timed_rotating_logger( "logs/db", "db" )

##########################################################

def dump_res( name: str, res ):

    print( f"{name}: ", end="" )

    for s in res:
        print( f"{s}, ", end="" )

    print()

##########################################################

def test_01():

    dbe = db.DB()

##########################################################

def test_02():

    dbe = db.DB()

    res = dbe.execute_query_from_file( "create_table_users.sql" )

    dump_res( "test_02", res )

##########################################################

def test_03():

    dbe = db.DB()

    res = dbe.execute_query_from_file( "tmpl_add_user.sql", { "ID": 1, "FIRST_NAME": "Test", "LAST_NAME": "User", "QUERY_DEBUG": 0 } )

    dump_res( "test_03", res )

##########################################################

def test_04():

    dbe = db.DB()

    id = random.randint( 1, 100 )

    res = dbe.execute_query_from_file( "tmpl_add_user.sql", { "ID": id, "FIRST_NAME": f"Test_{id}", "LAST_NAME": f"User_{id}", "QUERY_DEBUG": 0 } )

    dump_res( "test_04", res )

##########################################################

def test_05():

    dbe = db.DB()

    res = dbe.execute_query_from_file( "show_table_users.sql" )

    dump_res( "test_05", res )

##########################################################

def test():

    test_01()
    test_02()
    test_03()
    test_04()
    test_05()

##########################################################

if __name__ == "__main__":
   test()
