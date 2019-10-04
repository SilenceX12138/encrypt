from PIL import Image


# 将图像rgb值均改为偶数
def EvenImage(image):
    pixels = list(image.getdata())
    evenpixels = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1, t >> 1 << 1)
                  for (r, g, b, t) in pixels]
    evenimage = Image.new(image.mode, image.size)
    evenimage.putdata(evenpixels)
    return evenimage


# 将字符串转化为二进制(中文产生以1开头的字节||>127)
def bistr(num):
    vac = (len(bin(num)) - 2) % 8
    if vac != 0:
        news = '0' * (8 - vac) + bin(num).replace('0b', '')
    else:
        news = bin(num).replace('0b', '')
    return news


# 将字符串编码进图片
def encode(image, data):
    evenimage = EvenImage(image)
    news = ''.join(map(bistr, bytearray(data, 'utf-8')))  # 返回的数组只能一个一个数字处理
    if len(news) > len(image.getdata()) * 4:
        return 'There isn\'t enough place to hold information.'
    else:
        encodedpixels = [
            (r + int(news[i * 4]), g + int(news[i * 4 + 1]),
             b + int(news[i * 4 + 2]),
             t + int(news[i * 4 + 3])) if i * 4 < len(news) else (r, g, b, t)
            for (i, (r, g, b, t)) in enumerate(list(evenimage.getdata()))
        ]
        encodedimage = Image.new(evenimage.mode, evenimage.size)
        encodedimage.putdata(encodedpixels)
        return encodedimage


# 将二进制串转化为'utf-8'
def utfstr(news):
    i = 0
    ans = ''

    def remain(x, i): return x[2:8] + (
        remain(x[8:], i - 1)  # 除去符号位的数据换算为十进制才有用
        if i > 1 else '') if x else ''

    def front(x, i): return x[i:8] + remain(x[8:], i - 1)

    while i < len(news):
        type = news[i:].index('0')
        if type == 0:  # 字符只占一个字节
            type = 1
        length = type * 8

        part = front(news[i:i + length], type)
        ascode = int(part, base=2)  # 把part看作base进制数然后转化为十进制
        ans += chr(ascode)
        i += length
    return ans


# 提取图片中的信息
def decode(image):
    pixels = list(image.getdata())
    lastpos = ''.join([
        str(int(r >> 1 << 1 != r)) + str(int(g >> 1 << 1 != g)) +
        str(int(b >> 1 << 1 != b)) + str(int(t >> 1 << 1 != t))
        for (r, g, b, t) in pixels
    ])

    tmpend = lastpos.index('0000000000000000')
    if tmpend % 8 != 0:
        end = tmpend + (8 - tmpend % 8)
    else:
        end = tmpend
    news = lastpos[:end]
    return utfstr(news)


def main():
    s = input('Please enter a str u want to add to the image:')
    path = input('Please enter the file\'s path:')
    path.replace('\\', '\\\\')
    with Image.open(path) as image:  # image.open才可以使用getdata()
        encode(image, s).save('encoded.png')
        with Image.open('encoded.png') as encodedimage:
            ans = decode(encodedimage)
            print(ans)


main()
