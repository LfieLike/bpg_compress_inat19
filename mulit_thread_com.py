import concurrent.futures as cf
import os    
import time
import sys,getopt
import threading
import json
from typing_extensions import runtime
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
def getpath(root='.',is_train=True):
    path_json = os.path.join(root, f'{"train" if is_train else "val"}{2019}.json')
    with open(path_json) as json_file:
        datas = json.load(json_file)
        samples = []
        for elem in datas['images']:
            cut = elem['file_name'].split('/')
            path_current = os.path.join(cut[1], cut[2], cut[3])
            samples.append(path_current)
        return samples
def my_compress(src_dir,dst_dir,relative_path,encode="bpgenc",decode='bpgdec',quantit=1):
    src = os.path.join(src_dir,relative_path)
    dst = os.path.join(dst_dir,relative_path[:-4]+".bpg")
    dst_dec = os.path.join(dst_dir,relative_path[:-4]+".PNG")
    #print(encode+" -f 444 -o "+ dst+" -q "+str(quantit)+" "+src )
    os.system(encode+" -f 444 -o "+ dst+" -q "+str(quantit)+" "+src )
    os.system(decode+" -o "+dst_dec +" "+dst)


def main(argv):
    #walkFile("/mnt/imagenet_data/PNG/val",  ,"n01440764",1)
    inputfile = ''
    outputfile = ''
    dec = "bpgdec"
    enc = "bpgenc"
    quant = 0
    thread = 16
    try:
        opts, args = getopt.getopt(argv,"q:i:o:d:e:j:",["quant","ifile=","ofile=","dec=","enc=","thread="])
    except getopt.GetoptError:
        print ('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-q","--quant"):
            quant = int(arg)
        elif opt in ("-d","--dec"):
            dec = arg
        elif opt in ("-e","--enc"):
            enc = arg
        elif opt in ("-j","--thread"):
            thread = int(arg)
    tp = cf.ThreadPoolExecutor(thread) # 设置线程数16
    futures = []
    startTime = time.time()
    print(inputfile)
    dirs = getpath(inputfile)
    for dir in dirs:
        creat_dir(outputfile,dir)
    for dir in dirs:
        future = tp.submit(my_compress,inputfile,outputfile, dir,enc,dec,quant)
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
