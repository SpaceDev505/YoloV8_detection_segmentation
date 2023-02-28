from screeninfo import get_monitors
# i = 0
# str1 = str(get_monitors)
# print(str1)
# print(str1[8:15])
for m in get_monitors():
    print(str(m))
    str1 = str(m)
    print('width',str1[24:28])
    print('height', str1[37:41])
    print('width_mm', str1[52:55])
    print('height_mm', str1[67:71])
