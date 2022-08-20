import argparse
import os
from pathlib import Path
import sys

import preproc


def proc_videos(args):
    video_processor = preproc.VideoProcessor(args.dir_moma)
    video_processor.select()
    video_processor.trim_act(resize=True)
    video_processor.trim_sact(resize=True)
    video_processor.trim_hoi(resize=True)
    video_processor.sample_hoi()
    video_processor.sample_hoi_frames()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir-moma", type=str, default="/media/hdd/moma-lrg")
    args = parser.parse_args()

    proc_videos(args)


if __name__ == "__main__":
    main()
