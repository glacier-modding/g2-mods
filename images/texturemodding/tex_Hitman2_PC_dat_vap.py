from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Hitman 2 [PC]", ".dat;.vap")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    #noesis.logPopup()
    return 1

def noepyCheckType(data):
    return 1
    
def noepyLoadRGBA(data, texList):
    bs = NoeBitStream(data)
    bs.readUShort()
    bs.readUShort()
    fsize = bs.readUInt()
    bs.readUInt()
    imgWidth = bs.readUShort()            
    imgHeight = bs.readUShort()           
    imgFmt = bs.readUByte()
    print(imgWidth, "x", imgHeight, "-", hex(imgFmt), ":imgfmt")
    bs.readUByte()
    mips = bs.readUByte()
    bs.readUByte()
    bs.readUInt()
    datasize = bs.readUInt()
    bs.seek(0x88)
    dataOffset1 = bs.readUInt()
    dataOffset2 = bs.readUInt()
    if dataOffset1 == 0:
        bs.seek(dataOffset2)
    else:
        bs.seek(dataOffset1 + dataOffset2)
    data = bs.readBytes(datasize)      
    #R8G8 ???
    if imgFmt == 0x34:
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "r8 g8")
        texFmt = noesis.NOESISTEX_RGBA32
    #A8 ???
    elif imgFmt == 0x42:
        data = rapi.imageDecodeRaw(data, imgWidth, imgHeight, "a8")
        texFmt = noesis.NOESISTEX_RGBA32
    #BC1/DXT1
    elif imgFmt == 0x49:
        #data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC1)
        texFmt = noesis.NOESISTEX_DXT1
    #BC3/DXT5
    elif imgFmt == 0x4f:
        #data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC3)
        texFmt = noesis.NOESISTEX_DXT5
    #BC4/ATI1
    elif imgFmt == 0x52:
        #data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC4)
        data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_ATI1)
        texFmt = noesis.NOESISTEX_RGBA32
    #BC5/ATI2
    elif imgFmt == 0x55:
        #data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC5)
        data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_ATI2)
        texFmt = noesis.NOESISTEX_RGBA32
    #BC7
    elif imgFmt == 0x5a:
        data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC7) 
        texFmt = noesis.NOESISTEX_RGBA32
    texList.append(NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt))
    return 1