from common.timeFormat import timeFormat


def PeriodCombination(datelisy):
    """
    返回兩兩期數的組合
    :return:
    """
    if type(datelisy) is list:

        if datelisy[0] < datelisy[1]:
            datelisy = sorted(datelisy, reverse=True)

        result_list = []
        list_len = len(datelisy)
        for i in range(list_len):
            for j in range(i + 1, list_len):
                if datelisy[i] > datelisy[j]:
                    result_list.append((datelisy[i], datelisy[j]))
        return result_list
    else:
        return None


if __name__ == '__main__':
    a = [1673280000000, 1681142400000, 1682784000000, 1683648000000, 1687190400000, 1690473600000, 1700409600000,
         1701100800000]
    b = [timeFormat(i) for i in a]
    print(b)
    c = PeriodCombination(b)
    print(c)
