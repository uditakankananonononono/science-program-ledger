"""Development-only HRF annotation thinning and pixel graph audit.
Requires Pillow, numpy, scipy, scikit-image. Does not infer physiology.
"""
import hashlib,io,json,zipfile
import numpy as np
from PIL import Image
from scipy.ndimage import label
from skimage.morphology import skeletonize
from mask_graph import mask_to_graph


def extract_member(archive,member):
    with zipfile.ZipFile(archive) as z:raw=z.read(member)
    with Image.open(io.BytesIO(raw)) as im:
        a=np.array(im)
    original_shape=list(a.shape)
    if a.ndim==3 and a.shape[2]==3:
        if not (np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,0],a[:,:,2])):
            raise ValueError('RGB annotation channels differ; no grayscale inference')
        a=a[:,:,0]
    if a.ndim!=2 or not set(np.unique(a)).issubset({0,255}):
        raise ValueError('requires 2D 0/255 annotation')
    mask=a==255
    skeleton=skeletonize(mask,method='zhang')
    structure=np.ones((3,3),dtype=int)
    before=label(mask,structure=structure)[1]
    after=label(skeleton,structure=structure)[1]
    if before!=after:raise ValueError('8-neighbor component count changed')
    graph=mask_to_graph(skeleton.astype(int).tolist(),8,1,0,(1,))
    if len(graph)!=int(skeleton.sum()):raise AssertionError('vertex count mismatch')
    degrees={}
    for edges in graph.values():degrees[str(len(edges))]=degrees.get(str(len(edges)),0)+1
    return {'member':member,'image_sha256':hashlib.sha256(raw).hexdigest(),'shape':list(a.shape),'original_shape':original_shape,
            'foreground_pixels':int(mask.sum()),'skeleton_pixels':int(skeleton.sum()),
            'components_8_before':before,'components_8_after':after,
            'vertices':len(graph),'directed_edges':sum(map(len,graph.values())),
            'degree_histogram':degrees,'skeleton_sha256':hashlib.sha256(skeleton.tobytes()).hexdigest(),
            'cost_scope':'unit pixel adjacency only; bidirectional, no diagonal correction or flow'},skeleton

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('archive');p.add_argument('member');args=p.parse_args()
    record,_=extract_member(args.archive,args.member)
    print(json.dumps(record,indent=2))
