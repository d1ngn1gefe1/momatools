import argparse
import os
from pathlib import Path
import sys

import preproc


def proc_anns(args):
    # generates anns/taxonomy/
    taxonomy_parser = preproc.TaxonomyParser(args.dir_moma)
    taxonomy_parser.dump(verbose=False)

    # generates anns/anns.json
    ann1 = preproc.AnnPhase1(args.dir_moma, args.fname_ann1)
    ann1.inspect(verbose=False)

    ann2 = preproc.AnnPhase2(args.dir_moma, args.fname_ann2)
    ann2.inspect(verbose=False)

    ann_merger = preproc.AnnMerger(args.dir_moma, ann1, ann2)
    ann_merger.dump()

    # generates anns/splits/
    split_generator = preproc.SplitGenerator(args.dir_moma)
    split_generator.generate_standard_splits(ratio=0.8)
    split_generator.generate_few_shot_splits()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir-moma", type=str, default="/media/hdd/moma-lrg")
    parser.add_argument(
        "-f1", "--fname_ann1", type=str, default="video_anns_phase1_processed.json",
    )
    parser.add_argument(
        "-f2", "--fname_ann2", type=str, default="MOMA-videos-0209-all.jsonl"
    )
    args = parser.parse_args()

    proc_anns(args)


if __name__ == "__main__":
    main()
