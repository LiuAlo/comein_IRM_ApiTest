from common.MySql_manage import MySqlManager


class DataOverviewShareholderGroupingData(object):
    """
    股东管理——关键数据总览——性质分析、分组分析
    """

    def __init__(self, company_id, number_of_periods):
        self.params = {'company_id': company_id, 'number_of_periods': number_of_periods}

    def property_analysis(self):
        """
        性质分析
        :return:
        """
        sql_template = "SELECT minor, SUM(cgsl) s_cgsl, SUM(cgbl) s_cgbl FROM ts_irm_shareholder " \
                       "WHERE company_id=%(company_id)s AND record_date=%(number_of_periods)s " \
                       "GROUP BY minor ORDER BY s_cgbl DESC"
        return MySqlManager().get_list(sql_template, self.params)

    def grouping_analysis(self):
        """
        分组分析
        :return:
        """
        sql_template = "SELECT tag_id, SUM(cgsl) s_cgsl, SUM(cgbl) s_cgbl FROM (SELECT * FROM ts_irm_shareholder " \
                       "WHERE company_id=%(company_id)s AND record_date=%(number_of_periods)s) t1 " \
                       "LEFT JOIN (SELECT tag_id, minor FROM ts_irm_shareholder_tag_relation " \
                       "WHERE tag_id IN (" \
                       "SELECT id FROM ts_irm_shareholder_tag WHERE company_id=%(company_id)s)) t2 " \
                       "ON t1.minor=t2.minor " \
                       "WHERE tag_id IS NOT NULL GROUP BY tag_id ORDER BY s_cgbl DESC"
        return MySqlManager().get_list(sql_template, self.params)


if __name__ == '__main__':
    d = DataOverviewShareholderGroupingData(774, 1673280000000)
    print(d.property_analysis())
    print(d.grouping_analysis())
