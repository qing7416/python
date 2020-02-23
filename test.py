#1、传递参数时候不要使用列表
def foo(num,age=[]):
  age.append(num)
  print("num",num)
  return age

#--打印出三个数组[1],[2],[3]。
print(foo(1))
print(foo(2))
print(foo(3))


#--解决
def foo(num, age=None):
    if not age:
        age = []
    age.append(num)
    print("num", num)
    return age
print(foo(1))
print(foo(2))
print(foo(3))

#2、for-else 的使用场景
#--输出 100 以内的所有素数，素数之间以一个空格区分（注意，最后一个数字之后不能有空格）

import math
num = [] #存放 1-100 之间的素数
for i in range(2, 100):
    for j in range(2, int(math.sqrt(i)) + 1):
        if i % j == 0:
            break
    else:
        num.append(i) #根据定义如果都无法正常才加入
for index, i in enumerate(num):
    if index == len(num) - 1:
        print(i)
    else:
        print(i, end=" ")

#3、字典赋值
#--Python 中的字典是通过检查键值是否相等以及哈希值来确定两个键是否相同. 具有相同值的不可变对象在 Python 中始终具有相同的哈希值. 因为 1=1.0 所以 hash(1)==hash(1.0)
a = {}
a[1] = "A"
a[1.0] = "B"
a[2] = "C"
print(a)
#--hash(1)==hash(1.0)==hash(True)



#4、对象的属性赋值
#--
class A():
    def __init__(self,dicts):
        self.name=dicts["name"]
        self.age=dicts["age"]
        self.sex=dicts["sex"]
        self.hobby=dicts["hobby"]
        print(self.__dict__)
if __name__ == '__main__':
     dicts={"name":"lisa","age":23,"sex":"women","hobby":"hardstyle"}
     a=A(dicts)

#--大量字典键时
class A():
    def __init__(self,dicts):
        self.__dict__.update(dicts)
        print(self.__dict__)

if __name__ == '__main__':
     dicts={"name":"lisa","age":24,"sex":"women","hobby":"hardstyle"}
     a=A(dicts)

#5、闭包中的坑：python 的惰性计算
#--以为它会输出[0],[1],[4]，实际输出全是[16]
ls = []
for x in range(5):
    ls.append(lambda: x**2)
print(ls[0]())
print(ls[1]())
print(ls[2]())

#6、执行文件路径和当前路径

import os
print(os.getcwd())

#--获取文件的执行路径
import sys
print(sys.path[0])


#7、使用 eval 转整的时候数字前不能有 0
eval("02")


#8、处理长的字符串
("""多文本""")


#9、关于 requests 模块的编码问题
#--自动识别网页编码的代码,在获取 res(请求的对象),获取源码之前使用 下面的代码即可获取正确的网站编码。

res.encoding=res.apparent_encoding