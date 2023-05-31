import clickhouse_connect


class CH_Sql_manage(object):

    def __init__(self):
        self.cursor = None
        self.client()

    def client(self):
        self.cursor = clickhouse_connect.get_client(host='cc-bp1katvjq8981nu8d.ads.rds.aliyuncs.com',
                                                    port=8123,
                                                    username='',
                                                    password=''
                                                    )

    # 操作数据
    # client.command()
    def commandw(self, sql):
        """
        无返回 / 只返回一个值
        用来做数据增删改，或者聚合查询
        :return:
        """
        return self.cursor.command(sql)

    # 查询
    def select_column_names(self, sql, parameters):
        result = self.cursor.query(sql, parameters=parameters)
        return result.column_names

    def select_result_set(self, sql, parameters):
        result = self.cursor.query(sql, parameters=parameters)
        return result.result_set

    def select_row_count(self, sql, parameters):
        result = self.cursor.query(sql, parameters=parameters)
        return result.row_count

    def select_result_rows(self, sql, parameters):
        result = self.cursor.query(sql, parameters=parameters)
        return result.result_rows

    def select_result_columns(self, sql, parameters):
        result = self.cursor.query(sql, parameters=parameters)
        return result.result_columns
