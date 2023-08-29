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

import db
from externals.aux_logger.aux_logger import create_timed_rotating_logger

db.logger = create_timed_rotating_logger( "logs/db", "db" )

##########################################################

def test_01():

    dbe = db.DB()

##########################################################

def test_02():

    dbe = db.DB()

    dbe.execute_query_from_file( "create_table_users.sql" )

##########################################################

def test():

    test_01()

##########################################################

if __name__ == "__main__":
   test()
