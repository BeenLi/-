import datetime as dt


def time_true(time):
    if time == "now":
        return True
    elif time == "x" * 12:
        return True
    format_ = "%Y%m%d%H%M%S"
    try:
        dt.datetime.strptime("20" + time, format_)
    except ValueError:
        print("\n您输入的时间不合法!!!\n")
        return False
    else:
        now = dt.datetime.now()
        now = now.strftime(format_)[2:]
        if CardItems.time_diff(time, now):
            return True
        else:
            print("\n您输入的时间在未来，不合法!!!\n")
            return False


""" Carditems 类 """


class CardItems:
    def __init__(self, plate, cardtype, intime, outtime):
        self.plate = plate
        self.cardtype = cardtype
        self.intime = intime
        self.outtime = outtime

    """ 修改记录  """

    def edit_intime(self, intime):
        if time_true(intime):
            self.intime = intime

    def edit_intime_now(self):
        format_ = "%Y%m%d%H%M%S"
        now = dt.datetime.now()
        now = now.strftime(format_)[2:]
        self.intime = now

    def edit_outtime(self, outtime):
        if time_true(outtime):
            self.outtime = outtime

    def edit_outtime_now(self):
        format_ = "%Y%m%d%H%M%S"
        now = dt.datetime.now()
        now = now.strftime(format_)[2:]
        self.outtime = now

    def edit_plate(self, plate):
        self.plate = plate

    def edit_staffid(self, stuffid):
        pass

    """ 计算缴费 ; 如果是次卡就输出剩余次数;年卡就输出到期时间"""

    def get_expense(self):
        pass

    @classmethod  # 返回俩个时间间隔，单位是小时
    def time_diff(cls, start, stop):
        format_ = "%Y%m%d%H%M%S"  # "20200207212045"
        start_ = dt.datetime.strptime(("20" + start), format_)
        stop_ = dt.datetime.strptime(("20" + stop), format_)
        return (stop_ - start_).total_seconds() // (60 * 60)


""" 临时卡类 """


class TmpCard(CardItems):
    def __init__(self, plate, cardtype, intime, outtime):
        CardItems.__init__(self, plate, cardtype, intime, outtime)

    def get_expense(self):
        hours = self.time_diff(self.intime, self.outtime)
        return 5 if hours == 0 else (5 + 3 * (hours - 1))

    def show(self):
        return self.plate + "   " + self.cardtype + "    " + self.intime + "   " + self.outtime


""" 次卡类 """


class AmtCard(CardItems):
    def __init__(self, plate, cardtype, intime, outtime, staffid, res_time):
        CardItems.__init__(self, plate, cardtype, intime, outtime)
        self.staffid = staffid
        self.res_time = res_time

    def get_expense(self):
        number = int(self.res_time)
        if number < 5:
            print("您的卡剩余次数不足五次，请尽快充值")
        if number == 1:
            self.res_time = "0"
            print("警告：您的卡本次消费过后就没有次数可用，即将冻结。如若想再用，请返回充值")
        else:
            self.res_time = str(number - 1)
            return "还剩余次数:" + self.res_time

    def edit_staffid(self, staffid):
        self.staffid = staffid

    def edit_res_time(self, res_time):
        self.res_time = res_time

    @classmethod
    def register(cls, plate, staffid, res_time):  # 办次卡
        return cls(plate=plate, cardtype="1", intime=("x" * 12), outtime=("x" * 12), staffid=staffid, res_time=res_time)

    def show(self):
        return self.plate + "   " + self.cardtype + "    " + self.intime + "   " + self.outtime + "   " + self.staffid \
               + "      " + self.res_time


""" 年卡 """


class YearCard(CardItems):
    def __init__(self, plate, cardtype, intime, outtime, staffid, expire_date):
        CardItems.__init__(self, plate, cardtype, intime, outtime)
        self.staffid = staffid
        self.expire_date = expire_date

    def get_expense(self):
        interval = (dt.datetime.strptime(("20" + self.expire_date), "%Y%m%d") - dt.datetime.now()).days
        if interval < 10:
            print("您的卡剩余天数不足十天，请尽快充值")
        if interval == 0:
            print("您的卡还剩余一天, 明天即将冻结；如想继续使用，请返回充值")
        else:
            return "到期时间:" + self.expire_date + "; 剩余天数" + str(interval)

    def edit_staffid(self, staffid):
        self.staffid = staffid

    @classmethod
    def register(cls, plate, staffid, num_year):  # 办年卡需要：车牌号，工号，年限。
        curr_time = dt.datetime.now()  # 当前时间
        expire_date = str(curr_time.year + num_year)[2:] + curr_time.strftime("%m%d")
        return cls(plate=plate, cardtype="2", intime=("x" * 12), outtime=("x" * 12), staffid=staffid,
                   expire_date=expire_date)

    def edit_expire_date(self, expire_date):
        if 0 < int(expire_date) <= 100:
            curr_time = dt.datetime.now()
            self.expire_date = str(curr_time.year + int(expire_date))[2:] + curr_time.strftime("%m%d")
            return True
        if len(expire_date) != 6:
            print("日期应该是6位数，而你输入了{}位数\n".format(len(expire_date)))
            return False
        else:
            try:
                interval = (dt.datetime.strptime(("20" + expire_date), "%Y%m%d") - dt.datetime.now()).days
            except ValueError:
                print("输入的日期不合法,请重新输入\n")
                return False
            else:
                if interval < 0:
                    print("您输入的日期在过去，没有任何效用，系统不允许!!!\n")
                    return False
                else:
                    self.expire_date = expire_date
                    return True

    def show(self):
        return self.plate + "   " + self.cardtype + "    " + self.intime + "   " + self.outtime + "   " + self.staffid \
               + "      " + self.expire_date


if __name__ == "__main__":
    card1 = "A66666 2 200124140329 200124150423 458135 200918"
    card1 = card1.split()
    print(card1)
    if card1[1] == "2":
        card1 = YearCard(*card1)
        print("员工卡为:", card1.staffid)
        print("到期时间为:", card1.expire_date)
    print("该年卡到期时间为:", card1.get_expense())
