from __future__ import print_function
from sort import *
from yolo import *
import timeit

import os
import numpy as np
import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io

import glob
import time
import argparse
from filterpy.kalman import KalmanFilter
import motmetrics as mm

import cv2
import timeit


# 입력 사이즈 리스트 (Yolo 에서 사용되는 네크워크 입력 이미지 사이즈)
size_list = [320, 416, 608]

args = parse_args()
display = args.display = True
phase = args.phase
print(args)
total_time = 0.0
total_frames = 0
colours = np.random.rand(32, 3)  # used only for display

class_now = ""

# start_time = timeit.default_timer()
# frame = yolo.yolo(frame=frame, size=size_list[0], score_threshold=0.4, nms_threshold=0.4)
# terminate_time = timeit.default_timer()  # 종료 시간 체크

# print("%f초 걸렸습니다." % (terminate_time - start_time))
# cv2.imshow("Output_Yolo", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

if not os.path.exists('output1'):
    os.makedirs('output1')
pattern = os.path.join(args.seq_path, phase, '*', 'det', 'det.txt')
for seq_dets_fn in glob.glob(pattern):
    seq_dets = np.loadtxt(seq_dets_fn, delimiter=',')
    seq = seq_dets_fn[pattern.find('*'):].split(os.path.sep)[0]

    with open(os.path.join('output', '%s.txt' % (seq)), 'w') as out_file:
        print("Processing %s." % (seq))
        for frame in range(int(seq_dets[:, 0].max())):
            frame += 1  # detection and frame numbers begin at 1
            dets = seq_dets[seq_dets[:, 0] == frame, 2:7]
            dets[:, 2:4] += dets[:, 0:2]  # convert to [x1,y1,w,h] to [x1,y1,x2,y2]
            total_frames += 1

            if (display):
                fn = os.path.join('mot_benchmark', phase, seq, 'img1', '%06d.jpg' % (frame))
                frame1 = cv2.imread(fn)
                frame1 = yolo(frame=frame1, size=size_list[0], score_threshold=0.4, nms_threshold=0.4)
                # cv2.imshow("Output_Yolo", frame1)
                cv2.imwrite('output1/' +seq+ str(class_now) + str(frame) + '.jpg', frame1)
                print('output1/' +seq+ str(class_now) + str(frame) + '.jpg')
                plt.title(seq + ' Tracked Targets')

            start_time = time.time()
            cycle_time = time.time() - start_time
            total_time += cycle_time


print("Total Tracking took: %.3f seconds for %d frames or %.1f FPS" % (
total_time, total_frames, total_frames / total_time))

