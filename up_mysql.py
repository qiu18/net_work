import pymysql as mysql
class mysql_up:
    def __init__(self, mysqlip, mysqlport, mysqlname, mysqlpassword):
        self.mysqlip = mysqlip
        self.mysqlport = mysqlport
        self.mysqlname = mysqlname
        self.mysqlpasword = mysqlpassword

    def int_or_up_data(self, sql):
        get_conn = mysql.Connect(
            host=self.mysqlip,
            port=self.mysqlport,
            user=self.mysqlname,
            password=self.mysqlpasword,
            database='Net_work',
            charset='utf8'
            )
        try:
            cursor = get_conn.cursor()
            cursor.execute(sql)
            get_conn.commit()
        finally:
            get_conn.close()
