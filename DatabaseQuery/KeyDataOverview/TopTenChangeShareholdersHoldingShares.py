from common.MySql_manage import MySqlManager


# TODO: 需要确认“变动”是否都用绝对值
class TopTenChangeShareholdersHoldingShares(object):
    """
    前十变动排行
    """

    def __init__(self, company_id, current_time, contrast_time):
        self.params = {"company_id": company_id,
                       "current_time": current_time,
                       "contrast_time": contrast_time}

    def all_shareholder_dimensions_top_ten_change(self):
        """
        全部股东
        :return:
        """
        increase_changelist = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, t2.t2_cgsl, (t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, " \
                              "t1.t1_cgbl, t2.t2_cgbl, (t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (" \
                              "SELECT ymth, zqzhmc, SUM(IFNULL(cgsl,0)) t1_cgsl, SUM(IFNULL(cgbl,0)) t1_cgbl " \
                              "FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(current_time)s GROUP BY ymth) t1 LEFT JOIN (" \
                              "SELECT ymth, zqzhmc, SUM(IFNULL(cgsl,0)) t2_cgsl, SUM(IFNULL(cgbl,0)) t2_cgbl " \
                              "FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(contrast_time)s GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                              "WHERE t1.t1_cgsl!=0 AND t2.t2_cgsl!=0 AND (t1.t1_cgsl - t2.t2_cgsl) > 0 " \
                              "GROUP BY t1.ymth ORDER BY diff_cgsl DESC LIMIT 10"
        decrease_changelist = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, t2.t2_cgsl, (t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, " \
                              "t1.t1_cgbl, t2.t2_cgbl, (t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (" \
                              "SELECT ymth, zqzhmc, SUM(IFNULL(cgsl,0)) t1_cgsl, SUM(IFNULL(cgbl,0)) t1_cgbl " \
                              "FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(current_time)s GROUP BY ymth) t1 LEFT JOIN (" \
                              "SELECT ymth, zqzhmc, SUM(IFNULL(cgsl,0)) t2_cgsl, SUM(IFNULL(cgbl,0)) t2_cgbl " \
                              "FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(contrast_time)s GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                              "WHERE t1.t1_cgsl!=0 AND t2.t2_cgsl!=0 AND (t1.t1_cgsl - t2.t2_cgsl) < 0 " \
                              "GROUP BY t1.ymth ORDER BY diff_cgsl ASC LIMIT 10"
        new_entry_changelist = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, IFNULL(t2.t2_cgsl,0) t2_cgsl, " \
                               "(t1.t1_cgsl - IFNULL(t2.t2_cgsl,0)) diff_cgsl, t1.t1_cgbl, IFNULL(t2.t2_cgbl,0) t2_cgbl, " \
                               "(t1.t1_cgbl - IFNULL(t2.t2_cgbl,0)) diff_cgbl FROM (" \
                               "SELECT ymth, zqzhmc, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                               "WHERE company_id=%(company_id)s AND record_date=%(current_time)s GROUP BY ymth) t1 " \
                               "LEFT JOIN (SELECT ymth, zqzhmc, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl " \
                               "FROM ts_irm_shareholder WHERE company_id=%(company_id)s AND " \
                               "record_date=%(contrast_time)s GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                               "WHERE t1.t1_cgsl!=0 AND IFNULL(t2.t2_cgsl,0)=0 GROUP BY t1.ymth " \
                               "ORDER BY diff_cgsl DESC LIMIT 10"
        exit_changelist = "SELECT t2.ymth, t2.zqzhmc, IFNULL(t1.t1_cgsl,0) t1_cgsl, t2.t2_cgsl, " \
                          "(IFNULL(t1.t1_cgsl,0) - t2.t2_cgsl) diff_cgsl, IFNULL(t1.t1_cgbl,0) t1_cgbl, t2.t2_cgbl, " \
                          "(IFNULL(t1.t1_cgbl,0) - t2.t2_cgbl) diff_cgbl FROM (SELECT ymth, zqzhmc, SUM(cgsl) t1_cgsl, " \
                          "SUM(cgbl) t1_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                          "AND record_date=%(current_time)s GROUP BY ymth) t1 RIGHT JOIN (" \
                          "SELECT ymth, zqzhmc, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl FROM ts_irm_shareholder " \
                          "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s GROUP BY ymth) t2 " \
                          "ON t1.ymth=t2.ymth WHERE IFNULL(t1.t1_cgsl,0)=0 AND t2.t2_cgsl!=0 " \
                          "GROUP BY t2.ymth ORDER BY diff_cgsl ASC LIMIT 10"
        output_template = {
            "increase_changelist": MySqlManager().get_list(increase_changelist, args=self.params),
            "decrease_changelist": MySqlManager().get_list(decrease_changelist, args=self.params),
            "new_entry_changelist": MySqlManager().get_list(new_entry_changelist, args=self.params),
            "exit_changelist": MySqlManager().get_list(exit_changelist, args=self.params)
        }
        return output_template

    def institution_shareholder_dimensions_top_ten_change(self):
        """
        机构股东
        :return:
        """
        increase_changelist = "SELECT t1.party_id, t1.party_full_name, t1.t1_cgsl, t2.t2_cgsl, " \
                              "(t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, t1.t1_cgbl, t2.t2_cgbl, " \
                              "(t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (SELECT party_id, party_full_name, " \
                              "SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                              "AND gdxz=1 AND party_id IS NOT NULL GROUP BY party_id) t1 LEFT JOIN (" \
                              "SELECT party_id, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s AND gdxz=1 " \
                              "AND party_id IS NOT NULL GROUP BY party_id) t2 ON t1.party_id=t2.party_id " \
                              "WHERE t1.t1_cgsl != 0 AND t2.t2_cgsl != 0  AND (t1.t1_cgsl - t2.t2_cgsl) > 0 " \
                              "ORDER BY diff_cgsl DESC LIMIT 10"
        decrease_changelist = "SELECT t1.party_id, t1.party_full_name, t1.t1_cgsl, t2.t2_cgsl, " \
                              "(t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, t1.t1_cgbl, t2.t2_cgbl, " \
                              "(t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (SELECT party_id, party_full_name, " \
                              "SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(current_time)s AND gdxz=1 " \
                              "AND party_id IS NOT NULL GROUP BY party_id) t1 LEFT JOIN (" \
                              "SELECT party_id, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s AND gdxz=1 " \
                              "AND party_id IS NOT NULL GROUP BY party_id) t2 ON t1.party_id=t2.party_id " \
                              "WHERE t1.t1_cgsl != 0 AND t2.t2_cgsl != 0  AND (t1.t1_cgsl - t2.t2_cgsl) < 0 " \
                              "ORDER BY diff_cgsl ASC LIMIT 10"
        new_entry_changelist = "SELECT t1.party_id, t1.party_full_name, t1.t1_cgsl, IFNULL(t2.t2_cgsl,0) t2_cgsl, " \
                               "(t1.t1_cgsl - IFNULL(t2.t2_cgsl,0)) diff_cgsl, t1.t1_cgbl, IFNULL(t2.t2_cgbl,0) t2_cgbl, " \
                               "(t1.t1_cgbl - IFNULL(t2.t2_cgbl,0)) diff_cgbl FROM (" \
                               "SELECT party_id, party_full_name, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl " \
                               "FROM ts_irm_shareholder WHERE company_id=%(company_id)s AND " \
                               "record_date=%(current_time)s AND gdxz=1 AND party_id IS NOT NULL " \
                               "GROUP BY party_id) t1 LEFT JOIN (SELECT party_id, SUM(cgsl) t2_cgsl, " \
                               "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                               "AND record_date=%(contrast_time)s AND gdxz=1 AND party_id IS NOT NULL " \
                               "GROUP BY party_id) t2 ON t1.party_id=t2.party_id WHERE t1.t1_cgsl != 0 " \
                               "AND IFNULL(t2.t2_cgsl,0) = 0 ORDER BY diff_cgsl DESC LIMIT 10"
        exit_changelist = "SELECT t2.party_id, t2.party_full_name, IFNULL(t1.t1_cgsl,0) t1_cgsl, t2.t2_cgsl, " \
                          "(IFNULL(t1.t1_cgsl,0) - t2.t2_cgsl) diff_cgsl, IFNULL(t1.t1_cgbl,0) t1_cgbl, t2.t2_cgbl, " \
                          "(IFNULL(t1.t1_cgbl,0) - t2.t2_cgbl) diff_cgbl FROM (SELECT party_id, SUM(cgsl) t1_cgsl, " \
                          "SUM(cgbl) t1_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                          "AND record_date=%(current_time)s AND gdxz=1 AND party_id IS NOT NULL " \
                          "GROUP BY party_id) t1 RIGHT JOIN (SELECT party_id, party_full_name, SUM(cgsl) t2_cgsl, " \
                          "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                          "AND record_date=%(contrast_time)s AND gdxz=1 AND party_id IS NOT NULL GROUP BY party_id) t2 " \
                          "ON t1.party_id=t2.party_id WHERE IFNULL(t1.t1_cgsl,0) = 0 AND t2.t2_cgsl != 0 " \
                          "ORDER BY diff_cgsl ASC LIMIT 10"
        output_template = {
            "increase_changelist": MySqlManager().get_list(increase_changelist, args=self.params),
            "decrease_changelist": MySqlManager().get_list(decrease_changelist, args=self.params),
            "new_entry_changelist": MySqlManager().get_list(new_entry_changelist, args=self.params),
            "exit_changelist": MySqlManager().get_list(exit_changelist, args=self.params)
        }
        return output_template

    def product_dimensions_top_ten_change(self):
        """
        产品维度
        :return:
        """
        increase_changelist = "SELECT t1.fund_id, t1.party_id, t1.fund_full_name, t1.t1_cgsl, t2.t2_cgsl, " \
                              "(t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, t1.t1_cgbl, t2.t2_cgbl, " \
                              "(t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (SELECT fund_id, party_id, fund_full_name, " \
                              "SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                              "AND fund_id IS NOT NULL GROUP BY fund_id) t1 LEFT JOIN (" \
                              "SELECT fund_id, party_id, fund_full_name, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl " \
                              "FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(contrast_time)s AND fund_id IS NOT NULL GROUP BY fund_id) t2 " \
                              "ON t1.fund_id=t2.fund_id WHERE t1.t1_cgsl !=0 AND t2.t2_cgsl != 0 " \
                              "AND (t1.t1_cgsl - t2.t2_cgsl) > 0 ORDER BY diff_cgsl DESC LIMIT 10"
        decrease_changelist = "SELECT t1.fund_id, t1.party_id, t1.fund_full_name, t1.t1_cgsl, t2.t2_cgsl, " \
                              "(t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, t1.t1_cgbl, t2.t2_cgbl, " \
                              "(t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (SELECT fund_id, party_id, fund_full_name, " \
                              "SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                              "AND fund_id IS NOT NULL GROUP BY fund_id) t1 LEFT JOIN (SELECT fund_id, party_id, " \
                              "fund_full_name, SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s " \
                              "AND fund_id IS NOT NULL GROUP BY fund_id) t2 ON t1.fund_id=t2.fund_id " \
                              "WHERE t1.t1_cgsl !=0 AND t2.t2_cgsl != 0 AND (t1.t1_cgsl - t2.t2_cgsl) < 0 " \
                              "ORDER BY diff_cgsl ASC LIMIT 10"
        new_entry_changelist = "SELECT t1.fund_id, t1.party_id, t1.fund_full_name, t1.t1_cgsl, " \
                               "IFNULL(t2.t2_cgsl,0) t2_cgsl, (t1.t1_cgsl - IFNULL(t2.t2_cgsl,0)) diff_cgsl, t1.t1_cgbl, " \
                               "IFNULL(t2.t2_cgbl,0) t2_cgbl, (t1.t1_cgbl - IFNULL(t2.t2_cgbl,0)) diff_cgbl FROM (" \
                               "SELECT fund_id, party_id, fund_full_name, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl " \
                               "FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                               "AND record_date=%(current_time)s AND fund_id IS NOT NULL GROUP BY fund_id) t1 " \
                               "LEFT JOIN (SELECT fund_id, party_id, fund_full_name, SUM(cgsl) t2_cgsl, " \
                               "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                               "AND record_date=%(contrast_time)s AND fund_id IS NOT NULL GROUP BY fund_id) t2 " \
                               "ON t1.fund_id=t2.fund_id WHERE t1.t1_cgsl !=0 AND IFNULL(t2.t2_cgsl,0) = 0 " \
                               "ORDER BY diff_cgsl DESC LIMIT 10"
        exit_changelist = "SELECT t2.fund_id, t2.party_id, t2.fund_full_name, IFNULL(t1.t1_cgsl,0) t1_cgsl, t2.t2_cgsl, " \
                          "(IFNULL(t1.t1_cgsl,0) - t2.t2_cgsl) diff_cgsl, IFNULL(t1.t1_cgbl,0) t1_cgbl, t2.t2_cgbl, " \
                          "(IFNULL(t1.t1_cgbl,0) - t2.t2_cgbl) diff_cgbl FROM (SELECT fund_id, party_id, " \
                          "fund_full_name, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                          "WHERE company_id=%(company_id)s AND record_date=%(current_time)s AND fund_id IS NOT NULL " \
                          "GROUP BY fund_id) t1 RIGHT JOIN (SELECT fund_id, party_id, fund_full_name, " \
                          "SUM(cgsl) t2_cgsl, SUM(cgbl) t2_cgbl FROM ts_irm_shareholder " \
                          "WHERE company_id=%(company_id)s AND record_date=%(contrast_time)s " \
                          "AND fund_id IS NOT NULL GROUP BY fund_id) t2 " \
                          "ON t1.fund_id=t2.fund_id WHERE IFNULL(t1.t1_cgsl,0) =0 AND t2.t2_cgsl != 0 " \
                          "ORDER BY diff_cgsl ASC LIMIT 10"
        output_template = {
            "increase_changelist": MySqlManager().get_list(increase_changelist, args=self.params),
            "decrease_changelist": MySqlManager().get_list(decrease_changelist, args=self.params),
            "new_entry_changelist": MySqlManager().get_list(new_entry_changelist, args=self.params),
            "exit_changelist": MySqlManager().get_list(exit_changelist, args=self.params)
        }
        return output_template

    def individual_shareholder_dimensions_top_ten_change(self):
        """
        个人股东
        :return:
        """
        increase_changelist = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, t2.t2_cgsl, (t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, " \
                              "t1.t1_cgbl, t2.t2_cgbl, (t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (" \
                              "SELECT ymth, zqzhmc, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                              "AND gdxz!=1 GROUP BY ymth) t1 LEFT JOIN (SELECT ymth, SUM(cgsl) t2_cgsl, " \
                              "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(contrast_time)s AND gdxz!=1 GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                              "WHERE t1.t1_cgsl != 0 AND t2.t2_cgsl != 0 AND (t1.t1_cgsl - t2.t2_cgsl) > 0 " \
                              "ORDER BY diff_cgsl DESC LIMIT 10"
        decrease_changelist = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, t2.t2_cgsl, (t1.t1_cgsl - t2.t2_cgsl) diff_cgsl, " \
                              "t1.t1_cgbl, t2.t2_cgbl, (t1.t1_cgbl - t2.t2_cgbl) diff_cgbl FROM (" \
                              "SELECT ymth, zqzhmc, SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                              "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                              "AND gdxz!=1 GROUP BY ymth) t1 LEFT JOIN (SELECT ymth, SUM(cgsl) t2_cgsl, " \
                              "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                              "AND record_date=%(contrast_time)s AND gdxz!=1 GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                              "WHERE t1.t1_cgsl != 0 AND t2.t2_cgsl != 0 AND (t1.t1_cgsl - t2.t2_cgsl) < 0 " \
                              "ORDER BY diff_cgsl ASC LIMIT 10"
        new_entry_changelist = "SELECT t1.ymth, t1.zqzhmc, t1.t1_cgsl, IFNULL(t2.t2_cgsl,0) t2_cgsl, " \
                               "(t1.t1_cgsl - IFNULL(t2.t2_cgsl,0)) diff_cgsl, t1.t1_cgbl, IFNULL(t2.t2_cgbl,0) t2_cgbl, " \
                               "(t1.t1_cgbl - IFNULL(t2.t2_cgbl,0)) diff_cgbl FROM (SELECT ymth, zqzhmc, " \
                               "SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                               "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                               "AND gdxz!=1 GROUP BY ymth) t1 LEFT JOIN (SELECT ymth, SUM(cgsl) t2_cgsl, " \
                               "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                               "AND record_date=%(contrast_time)s AND gdxz!=1 GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                               "WHERE t1.t1_cgsl != 0 AND IFNULL(t2.t2_cgsl,0) = 0 ORDER BY diff_cgsl DESC LIMIT 10"
        exit_changelist = "SELECT t2.ymth, t2.zqzhmc, IFNULL(t1.t1_cgsl,0) t1_cgsl, t2.t2_cgsl, " \
                          "(IFNULL(t1.t1_cgsl,0) - t2.t2_cgsl) diff_cgsl, IFNULL(t1.t1_cgbl,0) t1_cgbl, t2.t2_cgbl, " \
                          "(IFNULL(t1.t1_cgbl,0) - t2.t2_cgbl) diff_cgbl FROM (SELECT ymth, zqzhmc, " \
                          "SUM(cgsl) t1_cgsl, SUM(cgbl) t1_cgbl FROM ts_irm_shareholder " \
                          "WHERE company_id=%(company_id)s AND record_date=%(current_time)s " \
                          "AND gdxz!=1 GROUP BY ymth) t1 RIGHT JOIN (SELECT ymth, zqzhmc, SUM(cgsl) t2_cgsl, " \
                          "SUM(cgbl) t2_cgbl FROM ts_irm_shareholder WHERE company_id=%(company_id)s " \
                          "AND record_date=%(contrast_time)s AND gdxz!=1 GROUP BY ymth) t2 " \
                          "ON t1.ymth=t2.ymth WHERE IFNULL(t1.t1_cgsl,0) = 0 " \
                          "AND t2.t2_cgsl != 0 ORDER BY diff_cgsl ASC LIMIT 10"
        output_template = {
            "increase_changelist": MySqlManager().get_list(increase_changelist, args=self.params),
            "decrease_changelist": MySqlManager().get_list(decrease_changelist, args=self.params),
            "new_entry_changelist": MySqlManager().get_list(new_entry_changelist, args=self.params),
            "exit_changelist": MySqlManager().get_list(exit_changelist, args=self.params)
        }
        return output_template

    def fund_manager_shareholder_dimensions_top_ten_change(self):
        """
        基金经理
        :return:
        """
        # TODO: 接口还未返回数据，无法验证SQL语句
        pass


if __name__ == '__main__':
    d = TopTenChangeShareholdersHoldingShares(1018, 1690473600000, 1687190400000)
    print(d.individual_shareholder_dimensions_top_ten_change())
