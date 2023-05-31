from common.MySql_manage import MySqlManager


class DataOverviewChangeStatistics(object):
    """
    持股变动统计--户数统计
    """

    def __init__(self, company_id, current_time, contrast_time):
        self.params = {"company_id": company_id,
                       "current_time": current_time,
                       "contrast_time": contrast_time}

    @staticmethod
    def make_execute_sql(params):
        sql_template = "SELECT {output_field} FROM (SELECT ymth, zqzhmc, SUM(IFNULL(cgsl,0)) s_cgsl, " \
                       "SUM(IFNULL(cgbl,0)) s_cgbl FROM ts_irm_shareholder " \
                       "WHERE company_id={company_id} AND record_date={current_time} GROUP BY ymth) t1 " \
                       "{connection_mode} " \
                       "(SELECT ymth, zqzhmc, SUM(IFNULL(cgsl,0)) s_cgsl, SUM(IFNULL(cgbl,0)) s_cgbl " \
                       "FROM ts_irm_shareholder WHERE company_id={company_id} " \
                       "AND record_date={contrast_time} GROUP BY ymth) t2 ON t1.ymth=t2.ymth " \
                       "WHERE {associated_conditions}"
        execute_sql = sql_template.format(**params)
        return MySqlManager().get_one(execute_sql)

    def OverviewHoldingsNumber(self):
        """
        总览
        :return:
        """
        overview_resulf = {}
        overview_resulf.update(self.IncreasedHoldingsNumber())
        overview_resulf.update(self.ReduceHoldingsNumber())
        overview_resulf.update(self.NewlyAddedHoldingsNumber())
        overview_resulf.update(self.ExitHoldingsNumber())
        overview_resulf.update(self.MaintainHoldingsNumber())

        overview_resulf.update(self.IncreasedSharesNumber())
        overview_resulf.update(self.ReduceSharesNumber())
        overview_resulf.update(self.NewlyAddedSharesNumber())
        overview_resulf.update(self.ExitSharesNumber())
        return overview_resulf

    def IncreasedHoldingsNumber(self):
        """
        增持户数
        :return:
        """
        associated_conditions_params = {
            "output_field": "COUNT(1) cnt",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND t2.s_cgsl!=0 AND (t1.s_cgsl - t2.s_cgsl) > 0"
        }
        associated_conditions_params.update(self.params)
        return {"IncreasedHoldingsNumber": self.make_execute_sql(associated_conditions_params)["cnt"]}

    def ReduceHoldingsNumber(self):
        """
        减持户数
        :return:
        """
        associated_conditions_params = {
            "output_field": "COUNT(1) cnt",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND t2.s_cgsl!=0 AND (t1.s_cgsl - t2.s_cgsl) < 0"
        }
        associated_conditions_params.update(self.params)
        return {"ReduceHoldingsNumber": self.make_execute_sql(associated_conditions_params)["cnt"]}

    def NewlyAddedHoldingsNumber(self):
        """
        新增户数
        :return:
        """
        associated_conditions_params = {
            "output_field": "COUNT(1) cnt",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND IFNULL(t2.s_cgsl,0) = 0"
        }
        associated_conditions_params.update(self.params)
        return {"NewlyAddedHoldingsNumber": self.make_execute_sql(associated_conditions_params)["cnt"]}

    def ExitHoldingsNumber(self):
        """
        退出户数
        :return:
        """
        associated_conditions_params = {
            "output_field": "COUNT(1) cnt",
            "connection_mode": "RIGHT JOIN",
            "associated_conditions": "IFNULL(t1.s_cgsl,0)=0 AND t2.s_cgsl!=0"
        }
        associated_conditions_params.update(self.params)
        return {"ExitHoldingsNumber": self.make_execute_sql(associated_conditions_params)["cnt"]}

    def MaintainHoldingsNumber(self):
        """
        维持户数
        :return:
        """
        associated_conditions_params = {
            "output_field": "COUNT(1) cnt",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND t2.s_cgsl!=0 AND (t1.s_cgsl - t2.s_cgsl) = 0"
        }
        associated_conditions_params.update(self.params)
        return {"maintainHoldingsNumber": self.make_execute_sql(associated_conditions_params)["cnt"]}

    def gdzgs(self):
        sql = "SELECT gdzgs FROM ts_irm_shareholder_count WHERE company_id={} AND record_date={}".format(
            self.params.get('company_id'), self.params.get('current_time'))
        return MySqlManager().get_one(sql)

    def IncreasedSharesNumber(self):
        """
        增持股数
        :return:
        """
        associated_conditions_params = {
            "output_field": "SUM(t1.s_cgsl - t2.s_cgsl) sum_cgsl",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND t2.s_cgsl!=0 AND (t1.s_cgsl - t2.s_cgsl) > 0"
        }
        associated_conditions_params.update(self.params)
        cgsl = self.make_execute_sql(associated_conditions_params)["sum_cgsl"]
        if cgsl is None:
            return {"IncreasedSharesNumber": 0,
                    "IncreasedSharesRatio": 0
                    }
        ratio = round(int(cgsl) / int(self.gdzgs()['gdzgs']) * 100, 2)
        return {"IncreasedSharesNumber": cgsl,
                "IncreasedSharesRatio": ratio
                }

    def ReduceSharesNumber(self):
        """
        减持股数
        :return:
        """
        associated_conditions_params = {
            "output_field": "SUM(ABS(t1.s_cgsl - t2.s_cgsl)) sum_cgsl",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND t2.s_cgsl!=0 AND (t1.s_cgsl - t2.s_cgsl) < 0"
        }
        associated_conditions_params.update(self.params)
        cgsl = self.make_execute_sql(associated_conditions_params)["sum_cgsl"]
        if cgsl is None:
            return {"ReduceSharesNumber": 0,
                    "ReduceSharesRatio": 0
                    }
        ratio = round(int(cgsl) / int(self.gdzgs()['gdzgs']) * 100, 2)
        return {"ReduceSharesNumber": cgsl,
                "ReduceSharesRatio": ratio
                }

    def NewlyAddedSharesNumber(self):
        """
        新增股数
        :return:
        """
        associated_conditions_params = {
            "output_field": "SUM(t1.s_cgsl) sum_cgsl",
            "connection_mode": "LEFT JOIN",
            "associated_conditions": "t1.s_cgsl!=0 AND IFNULL(t2.s_cgsl,0)=0"
        }
        associated_conditions_params.update(self.params)
        cgsl = self.make_execute_sql(associated_conditions_params)["sum_cgsl"]
        if cgsl is None:
            return {"NewlyAddedSharesNumber": 0,
                    "NewlyAddedSharesRatio": 0
                    }
        ratio = round(int(cgsl) / int(self.gdzgs()['gdzgs']) * 100, 2)
        return {"NewlyAddedSharesNumber": cgsl,
                "NewlyAddedSharesRatio": ratio
                }

    def ExitSharesNumber(self):
        """
        退出股数
        :return:
        """
        associated_conditions_params = {
            "output_field": "SUM(t2.s_cgsl) sum_cgsl",
            "connection_mode": "RIGHT JOIN",
            "associated_conditions": "IFNULL(t1.s_cgsl,0)=0 AND t2.s_cgsl!=0"
        }
        associated_conditions_params.update(self.params)
        cgsl = self.make_execute_sql(associated_conditions_params)["sum_cgsl"]
        if cgsl is None:
            return {"ExitSharesNumber": 0,
                    "ExitSharesRatio": 0
                    }
        ratio = round(int(cgsl) / int(self.gdzgs()['gdzgs']) * 100, 2)
        return {"ExitSharesNumber": cgsl,
                "ExitSharesRatio": ratio
                }


if __name__ == '__main__':
    d = DataOverviewChangeStatistics(774, 1701100800000, 1700409600000)
    print(d.OverviewHoldingsNumber())
