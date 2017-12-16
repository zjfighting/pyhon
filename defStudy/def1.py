#统计字符在字符串出现的次数
def count(str):
    result = {}
    for char in str:
         number = result.get(char)
         if number == None:
             result[char] = 1
         else:
             result[char] = number + 1
    for key,value in result.items():
        print("{}:{}".format(key,value))
s = input("Please input string:")
print("the result is")
count(s)
