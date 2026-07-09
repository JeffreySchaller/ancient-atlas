#!/usr/bin/env python3
"""
add-music.py — duck an Artlist track under a finished Short.

The validated house recipe (2026-06-13): music sits UNDER the natural
audio via sidechain ducking, fades out before the ~3s end sting so the
ident breathes, whole mix normalized to YouTube's -14 LUFS. Emotional
target = reverent wonder, held unresolved (see memory/projects).

Usage:
    python3 add-music.py SHORT.mp4 "Artist - Track.wav" [--vol 0.5] [--out OUT.mp4]

Defaults: music volume 0.5, music fade-in 2s, fade-out starts 2.5s
before the video ends (keeps the sting clean). Tracks live in ~/Downloads
(Artlist WAVs, licensed to Jeff's account + Clearlist-whitelisted for
@AncientAtlasMap, so cleared on upload).
"""
import subprocess, sys, os
from pathlib import Path

def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())

def main():
    a = sys.argv[1:]
    if len(a) < 2:
        raise SystemExit(__doc__)
    short = Path(a[0]); track = Path(a[1])
    vol = float(a[a.index("--vol")+1]) if "--vol" in a else 0.5
    out = a[a.index("--out")+1] if "--out" in a else str(short.with_suffix("")) + "_music.mp4"
    D = dur(short)
    fo = max(0.5, D - 5.4)          # fade music out ~2.9s before end (sting safe)
    fc = (
      f"[0:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,asplit=2[o1][o2];"
      f"[1:a]atrim=0:{D:.2f},asetpts=PTS-STARTPTS,"
      f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,"
      f"afade=t=in:st=0:d=2,afade=t=out:st={fo:.2f}:d=2.5,volume={vol}[mus];"
      f"[mus][o1]sidechaincompress=threshold=0.04:ratio=6:attack=20:release=400[duck];"
      f"[duck][o2]amix=inputs=2:normalize=0:duration=first[pre];"
      f"[pre]loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
    )
    cmd = ["ffmpeg","-v","error","-i",str(short),"-i",str(track),
           "-filter_complex",fc,"-map","0:v","-map","[aout]",
           "-c:v","copy","-c:a","aac","-b:a","192k","-y",out]
    subprocess.run(cmd, check=True)
    print("✓", out)

if __name__ == "__main__":
    main()
