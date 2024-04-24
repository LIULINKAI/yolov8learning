import json
import os
from PIL import Image
from tqdm import tqdm
import shutil
if __name__ == '__main__':
    f = open("datasets/train.json")
    datadict = json.loads(f.read())
    imgdict = {}
    # clsdict = {
    #     "Car":0,
    #     "LargeBus":1,
    #     "BiCyclist":2,
    #     "Pedestrian":3
    # }
    clsdict = {}
    cls_id = 0
    # alldatanum = min(5000, len(datadict['annotations']))
    alldatanum = len(datadict['annotations'])
    val_split_id = int(alldatanum * 0.9)
    dstdir = "./datasets"
    phase = "train"
    dstimgdir = os.path.join(dstdir, "images", phase)
    dstlabeldir = os.path.join(dstdir, "labels", phase)
    if not os.path.exists(dstimgdir):
        os.makedirs(dstimgdir, exist_ok=True)
    if not os.path.exists(dstlabeldir):
        os.makedirs(dstlabeldir, exist_ok=True)
    print(datadict.keys())
    val_names = []
    for i in tqdm(range(alldatanum)):
        item = datadict['annotations'][i]
        srcpath = os.path.join("./datasets", item['filename'])
        img = Image.open(srcpath)
        w, h = img.size
        filename = item['filename'].split(os.sep)[-1][:-4]
        cls_name = item['label']
        if cls_name not in clsdict.keys():
            clsdict[cls_name] = cls_id
            # continue
            cls_id += 1
        if i > val_split_id:
            phase = "val"
            val_names.append(filename)
            dstimgdir = os.path.join(dstdir, "images", phase)
            if not os.path.exists(dstimgdir):
                os.makedirs(dstimgdir, exist_ok=True)
        dstimgpath = os.path.join(dstimgdir, item['filename'].split(os.sep)[-1])
        shutil.copyfile(srcpath, dstimgpath)
        if filename not in imgdict.keys():
            imgdict[filename] = []
        if item['box']['xmin'] is None:
            continue
        xmin = item['box']['xmin'] / w
        ymin = item['box']['ymin'] / h
        xmax = item['box']['xmax'] / w
        ymax = item['box']['ymax'] / h
        xc, yc, w, h = (xmin + xmax) / 2, (ymin + ymax) / 2, xmax-xmin, ymax-ymin
        linestr = "{} {} {} {} {}\n".format(clsdict[cls_name],xc, yc, w, h)
        imgdict[filename].append(linestr)
    f.close()
    for idx,filename in enumerate(imgdict.keys()):
        if filename in val_names:
            phase = "val"
            dstlabeldir = os.path.join(dstdir, "labels", phase)
            if not os.path.exists(dstlabeldir):
                os.makedirs(dstlabeldir, exist_ok=True)
        filepath = os.path.join(dstlabeldir, "{}.txt".format(filename))
        f = open(filepath, "w")
        for line in imgdict[filename]:
            f.write(line)
        f.close()
    for k,v in clsdict.items():
        print("{}: {}".format(v, k))