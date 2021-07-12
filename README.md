# bpg_compress_inat19

use
python resize_inat19.py -i /home/yangxv/train_val2019 -o resize_inat19

cp /home/yangxv/train_val2019/train2019.json resize_inat19/tran2019.json
cp /home/yangxv/train_val2019/val2019.json resize_inat19/val2019.json


python mulit_thread_com.py -i resize_inat19 -o test_inat19 -q 1

-i input file dir
-o output file dir
-q quantity
-d decode path
-e encode path
-j thread num
