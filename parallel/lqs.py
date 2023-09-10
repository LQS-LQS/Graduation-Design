from PIL import Image
import os

base_path = "D:/MyCode-Git/Graduation-Design/parallel/Images"


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return size / 1024


def compress_image(infile, outfile=None, mb=9.43, step=10, quality=100):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    if outfile is None:
        outfile = infile
    o_size = get_size(infile)
    # 如果图片本身小于想要压缩的大小
    if o_size <= mb:
        im = Image.open(infile)
        im.save(outfile)

    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)


def resize_image(infile, outfile='', x_s=800):
    """修改图片尺寸
    :param infile: 图片源文件
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:
    """
    im = Image.open(infile)
    x, y = im.size
    y_s = int(y * x_s / x)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)

    out.save(outfile)


if __name__ == '__main__':
    # 源路径      # 压缩后路径
    variables = ["agricultural", "airplane", "baseballdiamond", "beach", "buildings",
                 "denseresidential", "forest", "freeway", "golfcourse", "harbor",
                 "intersection", "mediumresidential", "mobilehomepark", "overpass", "parkinglot",
                 "river", "runway", "sparseresidential", "storagetanks", "tenniscourt"]
    for item in variables:
        for num in range(1, 100, 1):
            img1_path = f"{base_path}/{item}/{item}{num:02}.tif"
            img2_path = f"{base_path}/{item}/{item}{num:02}_2000.jpg"
            compress_image(img1_path, img2_path)
        print(item)
        # 源路径      # 压缩后路径
    # resize_image(r"D:\\MyCode-Git\\Diff\\1.jpg", r"D:\\MyCode-Git\\Diff\\33.jpg")
