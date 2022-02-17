import os
from pathlib import Path
from pprint import pprint

import momaapi
import preproc


def proc_anns(dir_moma, fname_ann_phase1, fname_ann_phase2):
  taxonomy_parser = preproc.TaxonomyParser(dir_moma)
  taxonomy_parser.dump(verbose=False)

  ann_phase1 = preproc.AnnPhase1(dir_moma, fname_ann_phase1)
  ann_phase1.inspect(verbose=False)

  ann_phase2 = preproc.AnnPhase2(dir_moma, fname_ann_phase2)
  ann_phase2.inspect(verbose=False)

  ann_merger = preproc.AnnMerger(dir_moma, ann_phase1, ann_phase2)
  ann_merger.dump()


def proc_videos(dir_moma):
  video_processor = preproc.VideoProcessor(dir_moma)
  video_processor.select()
  video_processor.trim_act()
  video_processor.trim_sact()
  video_processor.trim_hoi()


def generate_splits(dir_moma):
  moma = momaapi.MOMA(dir_moma)
  moma.write_splits(*momaapi.split_ids_act(moma.get_ids_act()))

  stats_overall_train, stats_per_class_train = momaapi.get_stats(moma, 'train')
  stats_overall_val, stats_per_class_val = momaapi.get_stats(moma, 'val')

  dists_overall = momaapi.get_dist_overall(stats_overall_train, stats_overall_val)
  dists_per_class = momaapi.get_dist_per_class(stats_per_class_train, stats_per_class_val)

  print('The quality of our split (cosine distance b/w train & val, the smaller the better):')
  pprint(dists_overall)
  pprint(dists_per_class)


def main():
  dir_moma = os.path.join(Path.home(), 'data/moma')
  fname_ann_phase1 = 'video_anns_phase1_processed.json'
  fname_ann_phase2 = 'MOMA-videos-0209-all.jsonl'

  proc_anns(dir_moma, fname_ann_phase1, fname_ann_phase2)
  proc_videos(dir_moma)
  generate_splits(dir_moma)


if __name__ == '__main__':
  main()
