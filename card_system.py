from data_presentation import *
from carditems import *

card_type_dict = {"0": "临时卡", "1": "次卡", "2": "年卡"}


class CardSystem:
    def __init__(self, filename, data=None):
        self.filename = filename
        self.data = data  # data就是SSList类

    @staticmethod  # 构造函数: 从txt文件读入数据组成CardSystem类
    def readfromtxt(filename):
        data = SLList()  # 存储数据的链表
        try:
            with open(filename, "r") as f:
                line = f.readline().split()
                while line:
                    if line[1] == "0":
                        data.prepend(TmpCard(*line))
                    elif line[1] == "1":
                        data.prepend(AmtCard(*line))
                    else:
                        data.prepend(YearCard(*line))
                    line = f.readline().split()
        except IndexError:
            print("文件里面没有任何数据")
        return CardSystem(filename, data)

    """ 功能0: 检索 """

    def search(self, value, staffid=False):
        return self.data.search(value, staffid)

    """ 功能1: 办卡 """

    def register_yearcard(self, plate, staffid, num_years):  # 确保每名员工只能办一张卡、且没有重复的车牌号。
        card = self.search(staffid, True)
        if not card:
            print("您还没有办过卡。将马上处理您的订单，请稍等...")
            if self.search(plate):
                print("你输入的车牌号有误，车辆管理系统里面已经存在该车牌号的车主。请重新输入")
                return True
            else:
                self.data.prepend(YearCard.register(plate, staffid, num_years))
                print("operate successfully")
                print("您的流水单如下:\n")
                print(self.data.get_head().elem.show() + "\n")
                return False
        else:
            print("抱歉:您已经办过一张卡。如果您想把卡更换到另一台车上请返回,选择``修改``即可")
            return True

    def register_amtcard(self, plate, staffid, res_times):
        card = self.search(staffid, True)
        if not card:  # 当该员工没有办理过卡时
            print("您还没有办过卡。将马上处理您的订单，请稍等...")
            if self.search(plate):  # 当该车辆绑定了员工时
                print("你输入的车牌号有误，车辆管理系统里面已经存在该车牌号的车主。请重新输入")
                return True
            else:
                self.data.prepend(AmtCard.register(plate, staffid, res_times))
                print("operate successfully")
                print("您的流水单如下:")
                print(self.data.get_head().elem.show() + "\n")
                return False
        else:
            print("抱歉:您已经办过一张卡。如果您想把卡更换到另一台车上请先返回,再选择``修改``操作进行")
            return True

    def register(self):
        while True:
            y = input("输入办卡类型(0、返回;1、次卡;2、年卡):")
            try:
                if y == "1":
                    print("\n输入6位车牌号,6位工号,次数.//示例(58次):EW4578 457815 58")
                    plate, staffid, res_times = input("依次输入车牌,工号,次数(空格隔开):").split()
                    if self.register_amtcard(plate, staffid, res_times):
                        continue
                    else:
                        break
                elif y == "2":
                    print("\n输入6位车牌号,6位工号,年限.//示例(2年):EW4578 457815 2")
                    plate, staffid, num_years = input("依次输入车牌,工号,年限(空格隔开):").split()
                    if self.register_yearcard(plate, staffid, num_years):
                        continue
                    else:
                        break
                elif y == "0":
                    break
                else:
                    print("\n输入有误,请重新输入")
            except ValueError:
                print("\n输入格式不对, 请重新输入.")
                continue

    """ 功能2: 浏览记录 """

    def show_data(self):
        self.data.show_cars()

    """ 功能3: 车辆进场 """

    def car_entry(self, plate, intime):
        car = self.search(plate)
        if car:  # 如果该车牌在系统中有记录
            if not (car[0].outtime != "x" * 12 or car[0].intime != "x" * 12):  # 刚进场
                if intime == "now":
                    car[0].edit_intime_now()
                else:
                    car[0].edit_intime(intime)
                car[0].edit_outtime("x" * 12)
                print("进场操作成功，您的流水单如下:")
                print(car[0].show())
            else:
                print("该车已经进场，无需多次进场")
        else:
            print("该车未进入过停车场，将马上为您办理临时卡...")
            car = TmpCard(plate, "0", intime, "x" * 12)  # 创建一个临时卡
            if intime == "now":
                car.edit_intime_now()
            self.data.prepend(car)
            print("办理成功,流水单如下")
            print(self.data.get_head().elem.show() + "\n")

    def vehicle_entry(self):
        while True:
            try:
                print("\n输入6位车牌号,12位进场时间,中间用空格隔开(退出请按q回车)")
                print("示例:E7845F 200207172058(当前时间可以用now替代)")
                info = input("请依次输入车牌,进场时间:")
                if info == "q":
                    break
                plate, intime = info.split()
                if len(plate) != 6:
                    print("输入的车牌号位数不对,请重新输入")
                    continue
                elif time_true(intime):  # 输入时间正确
                    self.car_entry(plate, intime)
                    break
                else:
                    continue
            except ValueError:
                print("输入格式不对, 请重新输入.")
                continue

    """ 功能4：车辆离场 """

    def car_exit(self, plate, outtime):
        car = self.search(plate)
        if not car:
            print("输入车牌号系统不存在，请重新输入")
        else:
            if car[0].intime == "x" * 12:
                print("该车还没有进场,系统不允许出场")
            else:
                if outtime == "now":
                    car[0].edit_outtime_now()
                else:
                    car[0].edit_outtime(outtime)
                print("此车办理的卡为：" + card_type_dict[car[0].cardtype] + "\n" + "停车代价: " + str(car[0].get_expense()))

    def vehicle_leave(self):
        while True:
            try:
                print("\n输入6位车牌号,12位出场时间,中间用空格隔开(退出请按q回车)")
                print("示例:E7845F 200207172058(当前时间可以用now替代)")
                info = input("请依次输入车牌,出场时间:")
                if info == "q":
                    break
                plate, outtime = info.split()
                if len(plate) != 6:
                    print("输入的车牌号位数不对,请重新输入")
                    continue
                elif time_true(outtime):  # 输入时间正确
                    self.car_exit(plate, outtime)
                    break
                else:
                    continue
            except ValueError:
                print("\n输入格式不对, 请重新输入.")
                continue

    """ 功能5: 修改记录 """

    @staticmethod
    def amend(car):
        if car:
            car = car[0]
            print("恭喜：检索成功,您的信息如下\n")
            print("%-5s%-6s%-11s%-8s%-6s%-6s" % ("车牌号", "类型", "进场时间", "出场时间", "职工号码", "剩余次数/到期时间"))
            print(car.show() + "\n")
            while True:
                if car.cardtype == "2":
                    print("修改项目为:1:车牌号, 2:进场时间, 3:出场时间, 4:职工号码, 5:到期时间(可以直接1:代表离现在的一年后)")
                elif car.cardtype == "1":
                    print("修改项目为:1:车牌号, 2:进场时间, 3:出场时间, 4:职工号码, 5:剩余次数")
                else:
                    print("修改项目为:1:车牌号, 2:进场时间, 3:出场时间")
                print("!!!示例(修改车牌号为E45712):1 E45742")
                try:
                    num, amend = input("请输入您要修改的项目和修改的值(空格隔开):").split()
                except ValueError:
                    print("\n你输入不合法,请按要求输入\n")
                else:
                    if num == "1":
                        if len(amend) != 6:
                            print("\n车牌号应该是六位数,而您输入的是{}位数。请重新输入\n".format(len(amend)))
                            continue
                        else:
                            car.edit_plate(amend)

                    elif num == "2":
                        if not time_true(amend):
                            continue
                        else:
                            if amend == "now":
                                car.edit_intime_now()
                            else:
                                car.edit_intime(amend)

                    elif num == "3":
                        if not time_true(amend):
                            continue
                        else:
                            if amend == "now":
                                car.edit_outtime_now()
                            else:
                                car.edit_outtime(amend)

                    elif num == "4":
                        if len(amend) != 6:
                            print("\n教工号应该是六位数,而您输入的是{}位数。请重新输入\n".format(len(amend)))
                            continue
                        else:
                            car.edit_staffid(amend)

                    elif num == "5":
                        if car.cardtype == "2":
                            if not car.edit_expire_date(amend):
                                continue
                            else:
                                pass
                        else:
                            car.edit_res_time(amend)
                    else:
                        print("\n输入有误，重新输入\n")
                        continue
                    print("恭喜您，修改成功;修改后:")
                    print(car.show() + "\n")
                    break

        else:
            print("抱歉:您检索的项目不存在,请重新输入...\n")

    def modify_record(self):
        while True:
            print("检索模式>>>1:车牌号码  2:员工号码  3:返回上一级")
            m = input("请输入你要检索的项目:")
            if m == "1":
                plate = input("请输入您的车牌号:")
                car = self.search(plate, False)
                print("正在检索中....")
                self.amend(car)
            elif m == "2":
                staffid = input("请输入您的工号:")
                car = self.search(staffid, True)
                print("正在检索中....")
                self.amend(car)
            elif m == "3":
                break
            else:
                print("您输入的模式不对，请重新输入.\n")
                continue

    """ 功能6: 数据排序 """

    @staticmethod
    def _sort(_head, func):
        return MergeSort(_head, func).merge_sort()

    @staticmethod
    def _sort2(_head):  # 按停车卡的类型分类
        x0 = SLList()
        x1 = SLList()
        x2 = SLList()
        p = _head.get_head()
        while p:
            if p.elem.cardtype == "0":
                x0.prepend(p.elem)
            elif p.elem.cardtype == "1":
                x1.prepend(p.elem)
            else:
                x2.prepend(p.elem)
            p = p.next
        p = x1.get_head()
        while p:
            x0.append(p.elem)
            p = p.next
        p = x2.get_head()
        while p:
            x0.append(p.elem)
            p = p.next
        x0.show_cars()
        return x0

    def card_sort(self):
        while True:
            print("\n排序关键字:1.车牌号;2.类型;3.进场时间;4.出场时间;5.职工号码;6.剩余次数;7.到期时限;8.返回")
            sort_flag = int(input("请输入你要比较的关键字:"))
            if sort_flag == 8:
                break
            else:
                print("正在排序中....")
                head = self.data.get_head()  # 取头结点
                if sort_flag == 1:  # 比较牌照
                    def func1(x):
                        return x.plate

                    self.data = self._sort(head, func1)
                    break

                elif sort_flag == 2:
                    self.data = self._sort2(self.data)
                    break

                elif sort_flag == 3:
                    def func3(x):
                        if x.intime == ("x" * 12):
                            return False
                        else:
                            return x.intime

                    self.data = self._sort(head, func3)
                    break

                elif sort_flag == 4:
                    def func4(x):
                        if x.outtime == ("x" * 12):
                            return False
                        else:
                            return x.outtime

                    self.data = self._sort(head, func4)
                    break

                elif sort_flag == 5:
                    def func5(x):
                        flag = x.cardtype
                        if flag == "0":
                            #   print("临时卡", x.show())
                            return False
                        else:
                            return x.staffid

                    self.data = self._sort(head, func5)
                    break

                elif sort_flag == 6:
                    def func6(x):
                        flag = x.cardtype
                        if flag == "0":
                            #   print("临时卡", x.show())
                            return False
                        elif flag == "1":
                            return x.res_time
                        else:
                            #   print("年卡", x.show())
                            return False

                    self.data = self._sort(head, func6)
                    break

                elif sort_flag == 7:
                    def func7(x):
                        flag = x.cardtype
                        if flag == "0":
                            #   print("临时卡", x.show())
                            return False
                        elif flag == "1":
                            #   print("次卡", x.show())
                            return False
                        else:
                            return x.expire_date

                    self.data = self._sort(head, func7)
                    break

                else:
                    print("输入不合法的数字，请重新输入")
                    continue

    """ 功能7: 退出系统 """

    def exit(self):
        p = self.data.get_head()  # self.data: SLList 链表
        f = open(self.filename, "w")
        while p:
            f.write(p.elem.show() + "\n")
            p = p.next
        f.close()
        return None
