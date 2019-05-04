# week3practice.py

１．将１～２０的偶数用filter生成可迭代对象后，将可迭代对象生成的数据在于列表中
    最终结果：
    l = [2,4,6,8,10...18,20]

    l = list(filter(lambda x:x % 2 == 0,range(1,21)))

２．用filter函数将１～１００之间所有的素数放入到列表l中
    print(l)    # [2,3,5,7,11....]

    def su(x):
        if x < 2:
            return False
        for y in range(2,x):
            if x % y == 0:
                return False
        return True
    l = list(filter(su,range(100)))
    print(l)

练习：
    names = ['Tom','Jerry','Spike','Tyke']
    排序的依据为字符串的反序
            'moT'     'yrreJ'     'ekipS'     'ekyT'

    结果：　['Spike','Tyke','Tom','Jerry']

    l = sorted()

    def k(s):
        return s[::-1]

    l = sorted(names,key=k)
    print(l)