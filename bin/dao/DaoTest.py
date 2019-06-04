from OPMysql import OPMysql

if __name__ == '__main__':
    # 申请资源
    opm = OPMysql()

    sql = "SELECT VERSION()"
    res = opm.op_select(sql)

    # 释放资源
    opm.dispose()
