import itertools
from collections import defaultdict


def fix_cname(cname):
  cname = cname.replace('(', '（').replace(')', '）').replace(',', '，')
  cname = cname.replace(' ', '').replace('·', '').replace('蓝球', '篮球')
  return cname


def fix_iid(iid):
  iid = iid.replace('（', '(').replace('）', ')').replace('，', ',')
  iid = iid.replace(' ', '').replace('\n', '').upper()
  iid = iid.replace('.', ',').replace(',,', ',')
  return iid


class BBox:
  def __init__(self, bbox_raw):
    x_tl = round(bbox_raw['topLeft']['x'])
    y_tl = round(bbox_raw['topLeft']['y'])
    x_tr = round(bbox_raw['topRight']['x'])
    y_tr = round(bbox_raw['topRight']['y'])
    x_bl = round(bbox_raw['bottomLeft']['x'])
    y_bl = round(bbox_raw['bottomLeft']['y'])
    x_br = round(bbox_raw['bottomRight']['x'])
    y_br = round(bbox_raw['bottomRight']['y'])

    assert x_tl == x_bl and x_tr == x_br and y_tl == y_tr and y_bl == y_br, \
        '[BBox] inconsistent coordinates {}'.format(bbox_raw)

    # FIXME: fix negative size error
    self.x = min(x_tl, x_tr)
    self.y = min(y_tl, y_bl)
    self.width = abs(x_tr-x_tl)
    self.height = abs(y_bl-y_tl)

  def __repr__(self):
    return f'({self.x}, {self.y}, {self.width}, {self.height})'


class Entity:
  def __init__(self, entity_raw, cn2en):
    """ type """
    type = cn2en[entity_raw['slot']['label']]

    """ cname """
    cname = entity_raw['children'][0]['input']['value']
    cname = fix_cname(cname)
    assert cname in cn2en, '[Entity] unseen cname {}'.format(cname)

    """ iid """
    iid = entity_raw['children'][1]['input']['value']
    iid = fix_iid(iid)

    """ bbox """
    bbox = BBox(entity_raw['slot']['plane'])

    self.type = type
    self.cname = cn2en[cname]
    self.iid = iid
    self.bbox = bbox


class Description:
  def __init__(self, description_raw, cn2en):
    """ type """
    type = cn2en[description_raw['slot']['label']]

    """ cname """
    cname = description_raw['children'][0]['input']['value']
    cname = fix_cname(cname)
    assert cname in cn2en, '[Description] unseen cname {}'.format(cname)

    """ iids_associated """
    iids_associated = description_raw['children'][1]['input']['value']
    iids_associated = fix_iid(iids_associated)

    self.type = type
    self.cname = cn2en[cname]
    self.iids_associated = iids_associated

  def breakdown(self):
    if self.type == 'binary description':
      iids_src = self.iids_associated[1:-1].split('),(')[0].split(',')
      iids_trg = self.iids_associated[1:-1].split('),(')[1].split(',')
      return list(itertools.product(iids_src, iids_trg, [self.cname]))
    elif self.type == 'unary description':
      iids_src = self.iids_associated.split(',')
      return list(itertools.product(iids_src, [self.cname]))
    else:
      assert False


class bidict(dict):
  """
  A many-to-one bidirectional dictionary
  Reference: https://stackoverflow.com/questions/3318625/how-to-implement-an-efficient-bidirectional-hash-table
  """
  def __init__(self, *args, **kwargs):
    super(bidict, self).__init__(*args, **kwargs)
    self.inverse = {}
    for key, value in self.items():
      self.inverse.setdefault(value, set()).add(key)

  def __setitem__(self, key, value):
    if key in self:
      self.inverse[self[key]].remove(key)
    super(bidict, self).__setitem__(key, value)
    self.inverse.setdefault(value, set()).add(key)

  def __delitem__(self, key):
    self.inverse[self[key]].remove(key)
    if len(self.inverse[self[key]]) == 0:
      del self.inverse[self[key]]
    super(bidict, self).__delitem__(key)


def defaultdict_to_dict(d):
  if isinstance(d, defaultdict):
    d = {k: defaultdict_to_dict(v) for k, v in d.items()}
  return d