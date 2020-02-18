from card_system import *

while True:
    try:
        filename = input("请输入存储数据的文件名称:")
        system = CardSystem.readfromtxt(filename)
    except FileNotFoundError:
        print("文件找不到,请重新输入.\n")
        continue
    else:
        break


while system:
    print("\n1:办卡  2:浏览  3.进场  4.出场  5.修改  6.排序  7.退出")
    x = input("请输入号码:")
    if x == "1":
        system.register()

    elif x == "2":
        system.show_data()

    elif x == "3":
        system.vehicle_entry()

    elif x == "4":
        system.vehicle_leave()

    elif x == "5":
        system.modify_record()

    elif x == "6":
        system.card_sort()

    elif x == "7":
        system = system.exit()

    else:
        print("输入有误,请重新输入")
