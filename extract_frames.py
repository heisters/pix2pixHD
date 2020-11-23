#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import argparse
import shutil
from glob import glob
import video_utils
     
parser = argparse.ArgumentParser(description="""build a "frame dataset" from a given video""")
parser.add_argument('-video', '--input-video', dest="input_video", help='input video', required=True)
parser.add_argument('-name', '--dataset-name', dest="dataset_name", help='dataset name', required=True)
parser.add_argument('-p2pdir', '--pix2pix-dir', dest="pix2pix_dir", help='pix2pix directory', required=True)
parser.add_argument('-width', '--width', help='output width', type=int)
parser.add_argument('-height', '--height', help='output height', type=int)
parser.add_argument('-start', '--start', help='timecode to start from')
parser.add_argument('-to', '--to', help='timecode to end at')
parser.add_argument('--extract-train', dest='extract_train', action='store_true')
parser.add_argument('--no-extract-train', dest='extract_train', action='store_false')
parser.add_argument('--extract-test', dest='extract_test', action='store_true')
parser.add_argument('--no-extract-test', dest='extract_test', action='store_false')
parser.set_defaults(extract_train=True, extract_test=True)
args = parser.parse_args()

if not os.path.isfile(args.input_video):
    raise Exception("video does not exist")

if not os.path.isdir(args.pix2pix_dir):
    raise Exception("pix2pix directory does not exist")

if ( args.width is not None and (args.width % 32 !=0) ) or ( args.height is not None and (args.height % 32 !=0) ):
	raise Exception("please use width and height values that are divisible by 32")

print("creating the dataset structure")
dataset_dir = os.path.realpath(args.pix2pix_dir) + '/datasets/' + args.dataset_name
os.mkdir(dataset_dir)
if args.extract_train: os.mkdir(dataset_dir + "/train_frames") 
if args.extract_test: os.mkdir(dataset_dir + "/test_frames") 

if args.extract_train:
    video_utils.extract_frames_from_video(
            os.path.realpath(args.input_video),
            dataset_dir + "/train_frames",
            output_shape=(args.width, args.height),
            start=args.start,
            to=args.to
    )

    if args.extract_test:
        # copy first few frames to, for example, start the generated videos
        for frame in sorted(glob(dataset_dir + "/train_frames/*.jpg"))[:60]:
            shutil.copy(
                frame,
                dataset_dir + "/test_frames"
            )
elif args.extract_test:
    video_utils.extract_frames_from_video(
            os.path.realpath(args.input_video),
            dataset_dir + "/test_frames",
            output_shape=(args.width, args.height),
            start=args.start,
            to=args.to
    )
