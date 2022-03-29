---
#author: "Hugo Authors"
title: "Pythonでjpgからpngへ一括変換"
date: "2021-12-29"
tags:
  [
    "Pathlib",
    "image convert",
    "multiprocess",
    "ProcessPoolExecutor",
    "拡張子変換",
    "png",
    "jpg",
    "マルチプロセス",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## jpg から png への一括変換 (マルチプロセス)

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import List
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def list_file_paths(dir_path: str) -> List[str]:
    """
    List file paths in a directory.

    Parameters
    ----------
    dir_path : str
        Path of the directory

    Returns
    -------
    List[str]
        List of the file paths in the directory
    """
    return sorted([str(path) for path in Path(dir_path).rglob("*") if path.is_file()])


def jpg2png(file_path):
    img = Image.open(file_path)
    img.save(f"{file_path[:-4]}.png")

def multiprocess_jpg2png(jpg2png, file_path_list):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(
            jpg2png,
            file_path_list
        ))

file_path_list = list_file_paths("./image_file_dir")
multiprocess_jpg2png(jpg2png, file_path_list)
```
