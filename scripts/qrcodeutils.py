import base64
import codecs
import io
import struct
import zlib
from typing import Optional

import base45
import cv2
from numpy import ndarray, array, uint8, fromstring
import qrcode
from PIL import Image
from pyzbar import pyzbar


def rawBytes(s) -> bytes:
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


def bytesToQRCode(bytQr: bytes) -> Image:
    return qrcode.make(base64.b64encode(bytqr))


def imageToBytesArray(image: Image) -> bytes:
    imgByteArray = io.BytesIO()
    image.save(imgByteArray)
    imgByteArray = imgByteArray.getvalue()
    return imgByteArray


def imageFromBytesArray(imgByteArray: bytes) -> Image:
    image = Image.open(io.BytesIO(imgByteArray))
    image.save("sesh.png")

    return image


def getQRCodeBytesArrayFromText(text: str) -> Optional[Image]:
    if isinstance(text, str):
        return imageFromBytesArray(imgByteArray = imageToBytesArray(image = textToQRCode(text = text)))


def imageToNumpy(img: Image) -> Optional[ndarray]:
    npArray = fromstring(img.tobytes(), dtype = uint8)
    return npArray


def detectTextFromQRCodeImg(img: Image) -> bytes:
    # Convert RGB to BGR
    opencvImage = cv2.cvtColor(array(img.convert('RGB')), cv2.COLOR_RGB2BGR)

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


# just  a test

byt = "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"
bytedcBin = byt.encode("ascii")
# print(decodeQRCode(bytedcBin))




