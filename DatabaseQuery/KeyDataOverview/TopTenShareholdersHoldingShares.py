from common.MySql_manage import MySqlManager


class TopTenShareholdersHoldingShares(object):
    """
    持股数前十大
    """

    def __init__(self, company_id, current_time, contrast_time):
        self.params = {"company_id": company_id,
                       "current_time": current_time,
                       "contrast_time": contrast_time}

    def all_shareholder_dimensions_top_ten(self):
        """
        全部股东
        :return:
        """
        sql_template = "SELECT t1.ymth, t1.zqzhmc, SUM(t1.cgsl) t1_cgsl, SUM(t2.cgsl) t2_cgsl, " \
                       "(SUM(t1.cgsl) - SUM(t2.cgsl)) diff_cgsl, SUM(t1.cgbl) t1_cgbl, SUM(t2.cgbl) t2_cgbl, " \
                       "(SUM(t1.cgbl) - SUM(t2.cgbl)) diff_cgbl FROM (SELECT ymth, zqzhmc, cgsl, cgbl " \
                       "FROM ts_irm_shareholder WHERE company_id=%(company_id)s AND record_date=%(current_time)s) t1 " \
                       "LEFT JOIN (SELECT ymth, zqzhmc, cgsl, cgbl FROM ts_irm_shareholder " \
                       "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s) t2 " \
                       "ON t1.ymth=t2.ymth GROUP BY t1.ymth ORDER BY t1_cgsl DESC LIMIT 10"

        return MySqlManager().get_list(sql_template, args=self.params)

    def institution_shareholder_dimensions_top_ten(self):
        """
        机构股东
        :return:
        """
        sql_template = "SELECT t1.party_id, t1.party_full_name, t1.product_cnt, t1.t1_cgsl, t2.t2_cgsl, " \
                       "(t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, t1.t1_cgbl, t2.t2_cgbl, " \
                       "(t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (SELECT party_id, party_full_name, " \
                       "COUNT(CASE WHEN fund_id IS NOT NULL THEN 1 END) product_cnt, SUM(cgsl) t1_cgsl, " \
                       "SUM(cgbl) t1_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                       "AND record_date=%(current_time)s AND gdxz=1 AND party_id IS NOT NULL " \
                       "GROUP BY party_id) t1 LEFT JOIN (SELECT party_id, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl " \
                       "FROM ts_irm_shareholder WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s " \
                       "AND gdxz=1 AND party_id IS NOT NULL GROUP BY party_id) t2 " \
                       "ON t1.party_id=t2.party_id ORDER BY t1.t1_cgsl DESC LIMIT 10"

        return MySqlManager().get_list(sql_template, args=self.params)

    def product_dimensions_top_ten(self):
        """
        产品维度
        :return:
        """
        sql_template = "SELECT t1.fund_id, t1.party_id, t1.fund_full_name, t1.t1_cgsl, t2.t2_cgsl, " \
                       "(t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, t1.t1_cgbl, t2.t2_cgbl, " \
                       "(t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (" \
                       "SELECT fund_id, party_id, fund_full_name, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl " \
                       "FROM ts_irm_shareholder WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                       "AND fund_id IS NOT NULL GROUP BY fund_id) t1 LEFT JOIN (" \
                       "SELECT fund_id, party_id, fund_full_name, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl " \
                       "FROM ts_irm_shareholder WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s " \
                       "AND fund_id IS NOT NULL GROUP BY fund_id) t2 " \
                       "ON t1.fund_id=t2.fund_id ORDER BY t1.t1_cgsl DESC LIMIT 10"

        return MySqlManager().get_list(sql_template, args=self.params)

    def individual_shareholder_dimensions_top_ten(self):
        """
        个人股东
        :return:
        """
        sql_template = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, t2.t2_cgsl, (t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, " \
                       "t1.t1_cgbl, t2.t2_cgbl, (t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (" \
                       "SELECT ymth, zqzhmc, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                       "WHERE company_id=%(company_id)s AND record_date=%(current_time)s AND gdxz!=1 GROUP BY ymth) t1 " \
                       "LEFT JOIN (SELECT ymth, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl FROM ts_irm_shareholder " \
                       "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s " \
                       "AND gdxz!=1 GROUP BY ymth) t2 ON t1.ymth=t2.ymth ORDER BY t1.t1_cgsl DESC LIMIT 10"

        return MySqlManager().get_list(sql_template, args=self.params)

    def fund_manager_shareholder_dimensions_top_ten(self):
        # TODO: 接口还未返回数据，无法验证SQL语句
        pass


if __name__ == '__main__':
    d = TopTenShareholdersHoldingShares(774, 1701100800000, 1700409600000)
    print(d.product_dimensions_top_ten())
