#!/usr/bin/env python3
"""
make-knitwise-sheet.py — Capsule I art onto a Knitwise size template.

Usage: python3 make-knitwise-sheet.py "Unisex M.bmp" [more sizes...]
Expects templates in ~/Downloads/base/ (AA_KNIT_TPL_DIR to override) and
the assembled band at /tmp/capsule1_band_flat.png (run chart-extract +
assemble-band first; see PRINT_SPECS.md).

Template anatomy (Knitwise K01): green = waste, red = knittable panels
(front/back/sleeves), magenta = trims (yarn color picked in the Yarns
tab), blue/yellow = annotations. We paint ONLY inside red. Front animal
band is placed below the neckline depth so no mammoth is bisected.
Composition: compass peerie at yoke, mammoth procession, strata at hems,
sleeves get strata at cuff only. Scale 2 template px per stitch.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage

OB=(13,13,18); CH=(201,168,76); AM=(232,185,96); IV=(240,238,233)
NAMES=[OB,CH,AM,IV]
TPL_DIR = os.environ.get("AA_KNIT_TPL_DIR", os.path.expanduser("~/Downloads/base"))
BAND = "/tmp/capsule1_band_flat.png"
SC = 2

def band_blocks():
    im = np.asarray(Image.open(BAND).convert("RGB"))
    S=12
    rows, cols = im.shape[0]//S, im.shape[1]//S
    grid = np.zeros((rows,cols),dtype=int)
    pal = np.array(NAMES,dtype=float)
    for r in range(rows):
        for c in range(cols):
            cell = im[r*S+3:(r+1)*S-3, c*S+3:(c+1)*S-3].reshape(-1,3).mean(0)
            grid[r,c] = ((pal-cell)**2).sum(1).argmin()
    runs=[];start=None
    for i,v in enumerate(((grid==1).mean(1))>0.04):
        if v and start is None: start=i
        if not v and start is not None: runs.append((start,i)); start=None
    if start is not None: runs.append((start,rows))
    a,b = max(runs,key=lambda t:t[1]-t[0])
    return grid[2:16,:37], grid[a:b,:37], grid[b+2:b+15,:37]

P2RGB = {0:np.array(OB),1:np.array(CH),2:np.array(AM),3:np.array(IV)}

def tile_into(mask, art, y_top, base):
    ys, xs = np.where(mask)
    x0, x1 = xs.min(), xs.max()
    reps = (x1-x0+1)//(art.shape[1]*SC)+2
    strip = np.tile(art,(1,reps))[:, :((x1-x0+1)//SC)+1]
    for r in range(strip.shape[0]):
        for c in range(strip.shape[1]):
            if strip[r,c]==0: continue
            yy, xx = y_top+r*SC, x0+c*SC
            blk = (slice(yy,yy+SC), slice(xx,xx+SC))
            sub = mask[blk]
            base[blk][sub] = P2RGB[strip[r,c]]

def build(size_file):
    compass, animal, strata = band_blocks()
    arr = np.asarray(Image.open(os.path.join(TPL_DIR,size_file)).convert("RGB")).copy()
    red = (arr[:,:,0]>200)&(arr[:,:,1]<60)&(arr[:,:,2]<60)
    lab, n = ndimage.label(red)
    panels={}
    boxes=[]
    for i in range(1,n+1):
        ys,xs = np.where(lab==i)
        if len(ys)<2000: continue
        boxes.append((i,ys,xs))
    # classify: front = topmost wide panel, back = bottom wide, sleeves = sides
    wide = sorted([b for b in boxes if (b[2].max()-b[2].min())>340], key=lambda b: b[1].min())
    side = sorted([b for b in boxes if (b[2].max()-b[2].min())<=340], key=lambda b: b[2].min())
    panels["front"], panels["back"] = (lab==wide[0][0]), (lab==wide[1][0])
    panels["sleeveL"], panels["sleeveR"] = (lab==side[0][0]), (lab==side[1][0])
    for m in panels.values(): arr[m]=OB
    fm=panels["front"]; fys,fxs=np.where(fm)
    cx=(fxs.min()+fxs.max())//2
    neck_bottom=np.where(fm[:,cx])[0].min()
    tile_into(fm, compass, fys.min()+24, arr)
    tile_into(fm, animal, neck_bottom+16, arr)
    tile_into(fm, strata, fys.max()-strata.shape[0]*SC-20, arr)
    bm=panels["back"]; bys,_=np.where(bm)
    tile_into(bm, compass, bys.min()+24, arr)
    tile_into(bm, animal, bys.min()+24+compass.shape[0]*SC+20, arr)
    tile_into(bm, strata, bys.max()-strata.shape[0]*SC-20, arr)
    for k in ("sleeveL","sleeveR"):
        sm=panels[k]; sys_,_=np.where(sm)
        tile_into(sm, strata, sys_.max()-strata.shape[0]*SC-20, arr)
    out = size_file.replace(".bmp","").replace(" ","-")
    Image.fromarray(arr).save(f"knitwise-{out}-painted-ones.png", dpi=(96,96))
    print("✓", f"knitwise-{out}-painted-ones.png")

if __name__ == "__main__":
    for f in sys.argv[1:]:
        build(f)
