try:
    print("aaa")
except FileNotFoundError:
    print("file not exit")
except ValueError:
    print("string to number error")