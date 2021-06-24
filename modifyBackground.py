# Модуль обработки изображения (удаление, размытие, замена фона)
from PIL import ImageFilter


# Удаление фона
def deleteBackground(img, mask):
    img = img.convert("RGBA")
    mask = mask.convert("RGBA")
    pixImg = img.load()
    pixMask = mask.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixMask[x, y] == (0, 0, 0, 255):
                pixImg[x, y] = (0, 0, 0, 0)
    return img


# Размытие фона
def blurBackground(img, mask, radius):
    blurImage = img.filter(ImageFilter.GaussianBlur(radius=radius))
    pngBackImage = deleteBackground(img, mask)
    blurImage.paste(pngBackImage, mask=pngBackImage)
    return blurImage


# Замена фона
def changeBackground(img, mask, background):
    background = background.crop((int(background.size[0] / 2 - img.size[0] / 2),
                                  int(background.size[1] / 2 - img.size[1] / 2),
                                  int(background.size[0] / 2 + img.size[0] / 2),
                                  int(background.size[1] / 2 + img.size[1] / 2)))
    pngBackImage = deleteBackground(img, mask)
    background.paste(pngBackImage, mask=pngBackImage)
    return background
