#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI Narrator Engine - 解说视频生成引擎（对标 NarratoAI）。"""
import argparse, json
from pathlib import Path

STORY_TPL = {"开场": "镜头扫过{subject}，{motion}。", "特写": "这里注意{subject}的细节——{detail}。", "收尾": "最后{subject}定格，故事收束。"}
SALES_TPL = {"开场": "先看{subject}，{motion}，3 秒抓住你。", "特写": "重点来了：{detail}。", "收尾": "想入手的看评论区。"}
BGM_RULES = {"快": "upbeat_electronic.mp3", "慢": "soft_piano.mp3"}

def gen_script(shots, mode):
    tpl = SALES_TPL if mode == "sales" else STORY_TPL
    out = []
    for s in shots:
        text = tpl.get(s["type"], tpl["特写"]).format(subject=s.get("subject", "画面"), motion=s.get("motion", "缓推"), detail=s.get("detail", "质感"))
        out.append({"shot_id": s["shot_id"], "start": s["start"], "end": s["end"], "narration": text, "bgm": BGM_RULES.get(s.get("pace", "慢"))})
    return out

def to_srt(script):
    srt = ""
    for i, seg in enumerate(script, 1):
        srt += f"{i}\n{_ts(seg['start'])} --> {_ts(seg['end'])}\n{seg['narration']}\n\n"
    return srt

def _ts(t):
    m, s = int(t // 60), t % 60
    return f"00:{m:02d}:{int(s):02d},{int(s % 1 * 1000):03d}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True); ap.add_argument("--mode", choices=["story", "sales"], default="story")
    ap.add_argument("--out", default="outputs")
    args = ap.parse_args()
    shots = json.loads(Path(args.plan).read_text(encoding="utf-8"))["shots"]
    script = gen_script(shots, args.mode)
    out = Path(args.out); out.mkdir(exist_ok=True)
    (out / "narration_plan.json").write_text(json.dumps(script, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "narration.srt").write_text(to_srt(script), encoding="utf-8")
    print(f"生成 {len(script)} 段解说 -> {out}/narration.srt")
    for seg in script[:3]:
        print(f"  [{seg['start']:.1f}-{seg['end']:.1f}s] {seg['narration']}")

if __name__ == "__main__":
    main()
