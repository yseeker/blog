---
#author: "Hugo Authors"
title: "プログラムではPathlibで相対パスを有効活用する"
date: "2022-03-18"
description: "pathlibは便利"
tags:
  [
    "Pathlib",
    "Path",
    "Python",
    "相対パス",
    "自走プログラマー~Python の先輩が教えるプロジェクト開発のベストプラクティス 120",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

[自走プログラマー~Python の先輩が教えるプロジェクト開発のベストプラクティス 120](https://amzn.to/3iA52lL)を読んだのでその中で気になった「ファイルパスはプログラムからの相対パスで組み立てるという箇所は実践的でとても勉強になったのでメモしておく。

```
├──　run.py
├──　data
  ├── input.txt
  └── images
```

みたいなディレクトリがある場合は

```python
import csv
from pathlib import Path

current_dir = Path(__file__).parent
image_path = current_dir / "data" / "images"
inuput_path = current_dir / "input_txt"
```

とすればよい。
