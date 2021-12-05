import io
import qrcode
from PIL import Image


def textToQRCode(text: str) -> Image:
    return qrcode.make(text)


def imageToBytesArray(image: Image) -> bytes:
    imgByteArray = io.BytesIO()
    image.save(imgByteArray, format = image.format)
    imgByteArray = imgByteArray.getvalue()
    return imgByteArray


def imageFromBytesArray(imgByteArray: bytes) -> Image:
    image = Image.open(io.BytesIO(imgByteArray))
    #  image.save("prova.png")
    return image


def getQRCodeBytesArrayFromText(text: str):
    if isinstance(text, str):
        return imageFromBytesArray(imgByteArray = imageToBytesArray(image = textToQRCode(text = text)))