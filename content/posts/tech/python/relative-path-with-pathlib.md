---
#author: "Hugo Authors"
title: "プログラムでは相対パスを有効活用する"
date: "2022-03-17"
description: "cv2.setNumThreads(0)＆マルチプロセスをやめる"
tags:
  [
    "multithreading",
    "並列化",
    "高速化",
    "マルチスレッド",
    "openCV",
    "ThreadPoolExecuter",
    "cv2.setNumThreads",
    "ProcessPoolExecuter",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: true
---

```python
import csv
from pathlib import Path

this_dir = Path(__file__).parent
file_path = this_dir / "file.txt"

```
