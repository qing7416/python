# coding=utf-8
'''
# 猜测平板密码
# 2020-04-18 08:00:00
'''
import datetime

password='412825'
hh=13
currTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
currHH = datetime.datetime.now().hour
print("\n当前时间是：" + currTime + '\n')
if currHH >= hh:
    print("已到中午",hh,"时，平板密码是：",password,"，愉快的使用平板吧！\n")
    exit()
else:
    print("未到中午",hh,"时，不能获取平板密码！\n")

#--guess
guesspassword = input("猜一猜密码:")
print('你猜测的密码是：\033[1;33;44m ',guesspassword,'\033[0m')

if guesspassword.isdigit() is False:
    print("密码只能是数字，退出!\n")
    exit()

if len(guesspassword) != 6:
    print("密码长度不正确，需要6位数字，退出!\n")
    exit()

if password == guesspassword:
    print("恭喜猜测密码正确，愉快的使用平板吧！\n")
else:
    print("猜测密码错误,稍会再试!\n")

