# -*- coding: utf-8 -*-
import imghdr
import sys
import os
import exifread
import shutil


class ReadFailException(Exception):  
    pass

def getImgType(fileName):
    ret = None
    try:
        ret = imghdr.what(fileName)
    except Exception, e:
        print fileName, e
    return ret

def getOriginalDate(filename):  
    try:  
        fd = open(filename, 'rb')  
    except:  
        raise ReadFailException, "unopen file[%s]\n" % filename  
    data = exifread.process_file( fd )  
    if data:  
        try:  
            t = data['EXIF DateTimeOriginal']  
            return str(t).replace(":",".").replace(" ", "_")#[:7]  
        except:  
            pass  

    return None


def classifyPictures(srcPath, dstPath, delOrigImg=False):  
    # 如果目录不存在，则创建目录
    if not os.path.exists(dstPath ):  
        os.mkdir(dstPath)  

    count = 0
    for root,dirs,files in os.walk(srcPath,True):  
        #dirs[:] = []  
        for filename in files:  
            filename = os.path.join(root, filename)  
            f,e = os.path.splitext(filename) 
            # 不是以下后缀名的文件，不做处理 
            #if e.lower() not in ('.jpg','.png','.mp4'):  
            imgType = getImgType(filename)
            if imgType is None:
                continue  

            t=None  
            try:  
                t = getOriginalDate( filename )  
            except Exception,e:  
                print e  
                continue  

            if t is not None:
                prefix = t
            else:
                t = "未知"
                prefix = str(count)
                count += 1

            dst = os.path.join(dstPath, prefix + "." + imgType)
            print "文件名:%s [拍摄时间:%s] 恢复到:%s" % (filename, t, dst)

            # 利用shell 的copy功能
            shutil.copy2( filename, dst )  

            # 删除文件
            if delOrigImg:
                os.remove( filename )  

classifyPictures(sys.argv[1], sys.argv[2])
