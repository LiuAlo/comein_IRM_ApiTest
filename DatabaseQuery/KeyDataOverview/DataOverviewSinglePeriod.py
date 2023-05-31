from common.MySql_manage import MySqlManager


class DataOverviewSinglePeriod(object):
    """
    股东管理——关键数据总览——统计模块
    """
    def __init__(self, company_id, number_of_periods):
        self.company_id = company_id
        self.number_of_periods = number_of_periods

    @staticmethod
    def make_execute_sql(params):
        sql_template = "SELECT {} FROM ts_irm_shareholder_count " \
                       "WHERE company_id={} AND record_date={}"
        execute_sql = sql_template.format(*params)
        return MySqlManager().get_one(execute_sql)

    def overview_of_roster_data(self):
        overview_resulf = {}
        overview_resulf.update(self.TotalHouseholds())
        overview_resulf.update(self.InstitutionalHouseholds())
        overview_resulf.update(self.IndividualHouseholds())
        overview_resulf.update(self.CreditShareholdersHouseholds())
        overview_resulf.update(self.TotalNumberOfShares())
        overview_resulf.update(self.InstitutionalNumberOfShares())
        overview_resulf.update(self.IndividualNumberOfShares())
        overview_resulf.update(self.CreditShareholdersNumberOfShares())
        overview_resulf.update(self.CirculateHouseholds())
        overview_resulf.update(self.CirculateNumberOfShares())
        return overview_resulf

    # params = (输出字段, 公司ID, 名册期数)
    def TotalHouseholds(self):
        """
        总户数
        :return:
        """
        params = ('gdzs', self.company_id, self.number_of_periods)
        return self.make_execute_sql(params)

    def InstitutionalHouseholds(self):
        """
        机构户数
        :return:
        """
        params = ('jggdzs', self.company_id, self.number_of_periods)
        return self.make_execute_sql(params)

    def IndividualHouseholds(self):
        """
        个人户数
        :return:
        """
        gdzs = self.TotalHouseholds()
        jggdzs = self.InstitutionalHouseholds()
        return {'grgdzs': int(gdzs["gdzs"]) - int(jggdzs["jggdzs"])}

    def CirculateHouseholds(self):
        """
        流通户数
        :return:
        """
        params = ('ltgdzs', self.company_id, self.number_of_periods)
        return self.make_execute_sql(params)

    def CreditShareholdersHouseholds(self):
        """
        信用股东户数
        :return:
        """
        params = ('xygdzs', self.company_id, self.number_of_periods)
        return self.make_execute_sql(params)

    def TotalNumberOfShares(self):
        """
        总股数
        :return:
        """
        params = ('gdzgs', self.company_id, self.number_of_periods)
        return self.make_execute_sql(params)

    def InstitutionalNumberOfShares(self):
        """
        机构股数、占比
        :return:
        """
        params = ('jggdzgs', self.company_id, self.number_of_periods)
        jggdzgs = self.make_execute_sql(params)
        gdzgs = self.TotalNumberOfShares()
        proportion = {'jggdzgs_proportion': round(int(jggdzgs['jggdzgs']) / int(gdzgs["gdzgs"]) * 100, 2)}
        jggdzgs.update(proportion)
        return jggdzgs

    def IndividualNumberOfShares(self):
        """
        个人股数
        :return:
        """
        gdzgs = self.TotalNumberOfShares()
        jggdzgs = self.InstitutionalNumberOfShares()
        grzgs = int(gdzgs["gdzgs"]) - int(jggdzgs["jggdzgs"])
        return {'grzgs': grzgs, 'grzgs_proportion': round(grzgs / int(gdzgs["gdzgs"]) * 100, 2)}

    def CirculateNumberOfShares(self):
        """
        流通股数、占比
        :return:
        """
        params = ('ltgdzgs', self.company_id, self.number_of_periods)
        ltgdzgs = self.make_execute_sql(params)
        gdzgs = self.TotalNumberOfShares()
        proportion = {'ltgdzgs_proportion': round(int(ltgdzgs['ltgdzgs']) / int(gdzgs["gdzgs"]) * 100, 2)}
        ltgdzgs.update(proportion)
        return ltgdzgs

    def CreditShareholdersNumberOfShares(self):
        """
        信用股东股数
        :return:
        """
        params = ('xygdzgs', self.company_id, self.number_of_periods)
        xygdzgs = self.make_execute_sql(params)
        gdzgs = self.TotalNumberOfShares()
        proportion = {'xygdzgs_proportion': round(int(xygdzgs['xygdzgs']) / int(gdzgs["gdzgs"]) * 100, 2)}
        xygdzgs.update(proportion)
        return xygdzgs


if __name__ == '__main__':
    d = DataOverviewSinglePeriod(774, 1701100800000)
    print(d.overview_of_roster_data())
