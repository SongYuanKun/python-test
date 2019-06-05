import pymysql
from DBUtils.PooledDB import PooledDB

from dao.MySqlProp import MySqlProp


class OPMysql(object):
    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            prop = MySqlProp()
            __pool = PooledDB(pymysql.connect, host=prop.host, port=3306, user=prop.user, password=prop.passWord,
                              database=prop.db)
            print(__pool)
        return __pool.connection()

    # 插入\更新\删除sql
    def op_insert(self, sql, args):
        print('op_insert', sql)
        insert_num = self.cur.execute(sql, args)
        print('mysql sucess ', insert_num)
        self.coon.commit()
        return insert_num

    # 查询
    def op_select(self, sql, args):
        print(1)
        print('op_select', sql)
        self.cur.execute(sql, args)  # 执行sql
        select_res = self.cur.fetchone()  # 返回结果为字典
        print('op_select', select_res)
        print(2)
        return select_res

    # 释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()
