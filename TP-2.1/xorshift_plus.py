## https://gist.github.com/amano41/4d254198333d890e6ef7ba622923e87c

def xorshift128plus():
    '''xorshift+
    https://en.wikipedia.org/wiki/Xorshift#xorshift+
    シフト演算で使用している 3 つの数値は元論文 Table.1 参照
    http://vigna.di.unimi.it/ftp/papers/xorshiftplus.pdf
    doi:10.1016/j.cam.2016.11.006
    '''

    s0 = 1
    s1 = 2

    def _random():
        nonlocal s0, s1
        x, y = s0, s1
        x = x ^ ((x << 23) & 0xFFFFFFFFFFFFFFFF)  # 64bit
        x = (x ^ (x >> 17)) ^ (y ^ (y >> 26))
        s0, s1 = y, x
        return s0 + s1

    return _random


def main():

    r = xorshift128plus()

    for i in range(10):
        print(r())


if __name__ == '__main__':
    main()