import MySQLdb


class MysqlSearch(object):
    def __init__(self):
        self.get_coon()

    def get_coon(self):
        try:
            self.coon = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                passwd='204534abc',
                db='movie',
                port=3306,
                charset='utf8'
            )
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def close_coon(self):
        try:
            if self.coon:
                self.coon.close()#关闭数据库的链接
        except MySQLdb.Error as e:
            print('Error: %s' % e)

    def get_one(self):
        # 准备sql
        sql = 'SELECT * FROM `news` WHERE `types` = %s ORDER BY `created_at` DESC;'
        # 找到cursor  看门的
        cursor = self.coon.cursor()
        # 执行sql
        cursor.execute(sql,('推荐',))
        # 拿到结果
        # cursor.rowcount 获取总共有多少行
        # print(cursor.description)
        #拿到结果
        rest = dict(zip([k[0] for k in cursor.description],cursor.fetchone()))  #fetchone()获取一条
        # 处理数据
        # print(rest['title'])
        # 关闭cursor
        cursor.close()
        #关闭数据库的链接
        self.close_coon()
        return  rest
    def get_more(self):
        # 准备sql
        sql = 'SELECT * FROM `news` WHERE `types` = %s ORDER BY `created_at` DESC;'

        cursor = self.coon.cursor()

        cursor.execute(sql,('百家',))

        rest = [dict(zip([k[0] for k in cursor.description],row)) for row in cursor.fetchall()]
        cursor.close()
        #关闭数据库的链接
        self.close_coon()
        return  rest
    def add_one(self):
        try:
            sql=(  #id view_content created_at
                "INSERT INTO `news` (`title`, `image`,`content`, `types`,`is_valid`)VALUE "
                "(%s,%s,%s,%s,%s);"
            )
            cursor=self.coon.cursor()
            cursor.execute(sql,('标题一','/static/image/1.png','新闻内容一','推荐',1))
            cursor.execute(sql,('标题二','/static/image/1.png','新闻内容一','推荐',0))
            #提交事务
            self.coon.commit()
            cursor.close()
        except MySQLdb.Error as e:
            self.coon.commit()#如果提交多条部分出错  会把正确的提交上去
            self.coon.rollback() #回滚到上一级，也就是说所有的都不提交
            print('Error: %s' % e)
        self.close_coon()

def main():
    obj = MysqlSearch()
    # rest=obj.get_more()
    # # print(rest)
    # for item in rest:
    #     print(item)
    obj.add_one()



if __name__=='__main__':
    main()