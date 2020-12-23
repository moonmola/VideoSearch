from __future__ import print_function
from sort import *
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
mh = mm.metrics.create()

# 이미지 경로
office = "room_ser.jpg"

# 이미지 읽어오기
# frame = cv2.imread(office)
# cv2.imshow("",frame)

# 입력 사이즈 리스트 (Yolo 에서 사용되는 네크워크 입력 이미지 사이즈)
size_list = [320, 416, 608]

# all train
args = parse_args()
display = args.display
phase = args.phase
print(args)
total_time = 0.0
total_frames = 0
colours = np.random.rand(32, 3)  # used only for display

acc = mm.MOTAccumulator(auto_id=True)

# Call update once for per frame. For now, assume distances between
# frame objects / hypotheses are given.
acc.update(
    [1, 2],                     # Ground truth objects in this frame
    [1, 2, 3],                  # Detector hypotheses in this frame
    [
        [0.1, np.nan, 0.3],     # Distances from object 1 to hypotheses 1, 2, 3
        [0.5,  0.2,   0.3]      # Distances from object 2 to hypotheses 1, 2, 3
    ]
)

if (display):
    if not os.path.exists('mot_benchmark'):
        print(
            '\n\tERROR: mot_benchmark link not found!\n\n    Create a symbolic link to the MOT benchmark\n    (https://motchallenge.net/data/2D_MOT_2015/#download). E.g.:\n\n    $ ln -s /path/to/MOT2015_challenge/2DMOT2015 mot_benchmark\n\n')
        exit()
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(111, aspect='equal')

if not os.path.exists('output1'):
    os.makedirs('output1')
pattern = os.path.join(args.seq_path, phase, '*', 'det', 'det.txt')
for seq_dets_fn in glob.glob(pattern):
    mot_tracker = Sort(max_age=args.max_age,
                       min_hits=args.min_hits,
                       iou_threshold=args.iou_threshold)  # create instance of the SORT tracker
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
                im = io.imread(fn)
                ax1.imshow(im)
                plt.title(seq + ' Tracked Targets')

            start_time = time.time()
            trackers = mot_tracker.update(dets)
            cycle_time = time.time() - start_time
            total_time += cycle_time

            for d in trackers:
                print('%d,%d,%.2f,%.2f,%.2f,%.2f,1,-1,-1,-1' % (frame, d[4], d[0], d[1], d[2] - d[0], d[3] - d[1]),
                      file=out_file)
                if (display):
                    d = d.astype(np.int32)
                    ax1.add_patch(patches.Rectangle((d[0], d[1]), d[2] - d[0], d[3] - d[1], fill=False, lw=3,
                                                    ec=colours[d[4] % 32, :]))

            if (display):
                fig.canvas.flush_events()
                plt.draw()
                ax1.cla()

print("Total Tracking took: %.3f seconds for %d frames or %.1f FPS" % (
total_time, total_frames, total_frames / total_time))

if (display):
    print("Note: to get real runtime results run without the option: --display")
# print(mh.list_metrics_markdown())


print(acc.events)
# start_time = timeit.default_timer()
# frame = yolo.yolo(frame=frame, size=size_list[0], score_threshold=0.4, nms_threshold=0.4)
# terminate_time = timeit.default_timer()  # 종료 시간 체크

# print("%f초 걸렸습니다." % (terminate_time - start_time))
# cv2.imshow("Output_Yolo", frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

