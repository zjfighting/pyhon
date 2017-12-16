def sumNumber(*numbers):
    sum = 0
    for number in numbers:
        sum = sum + number
    print("the result is:{}".format(sum))

sumNumber(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
