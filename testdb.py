#! /usr/bin/python3

import sqlite3

"""
conn = sqlite3.connect('qrdata.db') 
c = conn.cursor() 
c.execute('DELETE FROM qrs;',); 

print('We have deleted', c.rowcount, 'records from the table.') 

conn.commit() 

conn.close()
"""
conn = sqlite3.connect('qrdata.db') 
c = conn.cursor() 
c.execute('SELECT * FROM qrs;',);
records = c.fetchall()
print("Всего строк:  ", len(records))

for row in records:
    print(row[0])

c.close()


"""
class SUBD:    
    def __init__(self):
        self.conn=None
        self.curs=None
        
    def lookFor(self, data):
        sql = "SELECT * FROM qrs WHERE qr=?"

        if self.conn is None:
            self.conn=sqlite3.connect('qrdata.db')
            self.curs=self.conn.cursor()
        
        self.curs.execute(sql, [(data)])
        count = len(self.curs.fetchall())
        print(data + ' found: ' + str(count))
        if count == 0:
            return False
        else:
            return True
        
    def add(self, data):
        sql = "INSERT INTO qrs VALUES ('" + data + "')"
        self.curs.execute(sql)
        self.conn.commit()
        print(data + ' added')

    def close(self):
        if self.conn is not None:   
            self.conn.close()
            self.conn=None
            self.curs=None
"""            
        