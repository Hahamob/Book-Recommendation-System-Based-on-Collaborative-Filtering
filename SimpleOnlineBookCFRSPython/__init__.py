import pymysql

pymysql.version_info = (1, 4, 13, "final", 0)  # 必须有这个不然会报版本不对错误
pymysql.install_as_MySQLdb()  # 使用pymysql代替mysqldb连接数据库，当成是mysqldb一样使用，当然也可以不写这句，
# 那就按照pymysql的方式
# mysqldb目前MySQLdb并不支持python3
# 目前MySQLdb并不支持python3.x ， Python3.x连接MySQL的方案有：oursql, PyMySQL, myconnpy 等
