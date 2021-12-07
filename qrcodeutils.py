import base64
import codecs
import io

import cv2
import numpy
import qrcode
from PIL import Image
import struct
from pyzbar import pyzbar

import base45
import zlib



def rawbytes(s) -> bytes:
    """Convert a string to raw bytes without encoding"""
    outlist = []
    for cp in s:
        num = ord(cp)
        if num < 255:
            outlist.append(struct.pack('B', num))
        elif num < 65535:
            outlist.append(struct.pack('>H', num))
        else:
            b = (num & 0xFF0000) >> 16
            H = num & 0xFFFF
            outlist.append(struct.pack('>bH', b, H))
    return b''.join(outlist)


def textToQRCode(text: str) -> Image:
    return qrcode.make(text)


def bytesToQRCode(byt: bytes) -> Image:
    return qrcode.make(base64.b64encode(byt))


def imageToBytesArray(image: Image) -> bytes:
    imgByteArray = io.BytesIO()
    image.save(imgByteArray)
    imgByteArray = imgByteArray.getvalue()
    return imgByteArray


def imageFromBytesArray(imgByteArray: bytes) -> Image:
    image = Image.open(io.BytesIO(imgByteArray))
    image.save("sesh.png")

    return image


def getQRCodeBytesArrayFromText(text: str):
    if isinstance(text, str):
        return imageFromBytesArray(imgByteArray = imageToBytesArray(image = textToQRCode(text = text)))


def imageToNumpy(img: Image):
    nparray = numpy.fromstring(img.tobytes(), dtype = numpy.uint8)
    return nparray


def detectTextFromQRCodeImg(img: Image) -> bytes:

    # Convert RGB to BGR
    opencvImage = cv2.cvtColor(numpy.array(img.convert('RGB')), cv2.COLOR_RGB2BGR)

    val = pyzbar.decode(opencvImage)[0].data
    return base64.b64decode(val)


def decodeQRCode(encodedQRCode: bytes) -> str:

    firstDecode = base64.b64decode(encodedQRCode)
    imageQRCode = imageFromBytesArray(imgByteArray = firstDecode)
    text = detectTextFromQRCodeImg(img = imageQRCode)
    zobj = zlib.decompressobj()
    textDecompressed = zobj.decompress(text)
    textDecompressedDecoded64 = base45.b45decode(textDecompressed)
    textDecompressedDecoded64Decoded = codecs.decode(textDecompressedDecoded64)

    return textDecompressedDecoded64Decoded