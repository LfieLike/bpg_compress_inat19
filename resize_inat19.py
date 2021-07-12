import concurrent.futures as cf
import os    
import time
import sys,getopt
import threading
from PIL import Image
import json
import cv2
import numpy as np
from torchvision import transforms
from typing_extensions import runtime
from timm.data.transforms import _pil_interp, RandomResizedCropAndInterpolation, ToNumpy, ToTensor
from timm.data.random_erasing import RandomErasing
def creat_dir(root,path):
    cuts = path.split('/')
    now_path = root
    if os.path.exists(now_path) == False:
        os.mkdir(now_path)
    for cut in cuts:
        if "." in cut:
            continue
        now_path = os.path.join(now_path , cut)
        if os.path.exists(now_path) == False:
            os.mkdir(now_path)
            print("creat:"+now_path)
def getpath(root='.',is_train=False):
    path_json = os.path.join(root, f'{"train" if is_train else "val"}{2019}.json')
    with open(path_json) as json_file:
        datas = json.load(json_file)
        samples = []
        for elem in datas['images']:
            cut = elem['file_name'].split('/')
            path_current = os.path.join(cut[1], cut[2], cut[3])
            samples.append(path_current)
        return samples
def my_resize(src_dir,dst_dir,relative_path):
    src = os.path.join(src_dir,relative_path)
    dst = os.path.join(dst_dir,relative_path[:-4]+".png")
    #print(src)
    #print(dst)
    #print(encode+" -f 444 -o "+ dst+" -q "+str(quantit)+" "+src )
    tfs = get_transforms()
    #print(1)
    im = cv2.imread(src)
    #print(len(im))
    #print("fuck")
    im = Image.fromarray(im) 
    #print(len(im))
    x = np.array(tfs(im))
    #print(x)
    cv2.imwrite(dst,x)
def get_transforms():
    interpolation='bicubic'
    tfl = [
            transforms.Resize(256, _pil_interp(interpolation)),
            transforms.CenterCrop(224),
        ]
    return transforms.Compose(tfl)

def main(argv):
    #walkFile("/mnt/imagenet_data/PNG/val",  ,"n01440764",1)
    inputfile = ''
    outputfile = ''
    thread = 16
    try:
        opts, args = getopt.getopt(argv,"i:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    tp = cf.ThreadPoolExecutor(thread) # 设置线程数16
    futures = []
    startTime = time.time()
    print(inputfile)
    dirs = getpath(inputfile,is_train=False)
    for dir in dirs:
        creat_dir(outputfile,dir)
    for dir in dirs:
        future = tp.submit(my_resize,inputfile,outputfile, dir)
        futures.append(future)
    dirs = getpath(inputfile,is_train=True)
    for dir in dirs:
        future = tp.submit(my_resize,inputfile,outputfile, dir)
        futures.append(future)
    count = 0
    total = len(dirs)
    for future in cf.as_completed(futures):
        count += 1
        if(count%100 == 0):
            print(str(count)+"/"+str(total))
            print(str(count*100.0/total)+"%")
            endTime = time.time()
            runTime = endTime-startTime
            print("cost time:%0.3f"%runTime)
    tp.shutdown()
    os.system('pause')

if __name__ == "__main__":
   main(sys.argv[1:])
