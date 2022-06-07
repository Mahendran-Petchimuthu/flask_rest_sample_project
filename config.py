#!/usr/bin/env python3

mysql = {'host': 'localhost',
         'user': 'root',
         'passwd': 'helloworld',
         'db': 'fsudp'}

mysqlConfig = "mysql+pymysql://{}:{}@{}/{}".format(mysql['user'], mysql['passwd'], mysql['host'], mysql['db'])