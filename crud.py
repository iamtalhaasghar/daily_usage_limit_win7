# Thanks to: https://github.com/victorxa4/Simple-SQLITE-Crud

import sqlite3 as sql

class crud:
    def __init__(self, database):
        self.conn = sql.connect(database)
        self.cursor = self.conn.cursor()
        
    def CREATE_TABLE(self, table_name, fields):
        fields_to_query = []
        query = 'CREATE TABLE IF NOT EXISTS ' + table_name + '(' + fields + ')'

        self.cursor.execute(query)
        self.conn.commit()

    def INSERT_INTO(self, table, values):
        query_i = []
        if len(values) >= 2:
            for i in range(len(values) - 1):
                query_i.append(', ?')
            query = 'INSERT INTO ' + table +  ' VALUES(?' + ''.join(query_i) + ')'
        else:
            query = 'INSERT INTO ' + table +  ' VALUES(?)'

        self.cursor.execute(query, values)
        self.conn.commit()

    def DELETE(self, table, where=False):
        query = 'DELETE FROM ' + table
        if where:
            query = query + ' WHERE ' + where['column'] + where['oper'] + '?'
            self.cursor.execute(query,[ where['value']])
        else:
            self.cursor.execute(query)

        self.conn.commit()

    def DROP_TABLE(self, table):
        query = 'DROP TABLE ' + table

        self.cursor.execute(query)
        self.conn.commit()

    def UPDATE(self, table_name, _set, where):
        query = 'UPDATE ' + table_name + ' SET ' + _set['column'] + _set['oper'] + '? ' + ' WHERE ' + where['column'] + where['oper'] + '?'

        self.cursor.execute(query, [_set['value'], where['value']])
        self.conn.commit()


    def SELECT(self, table, query, where=False):
        query = 'SELECT ' + query + ' FROM ' + table
        if where:
            query = query + ' WHERE ' + where['column'] + where['oper'] + '?'
            self.cursor.execute(query, [where['value']])
        else:
            self.cursor.execute(query)
        
        return self.cursor.fetchall()
        
