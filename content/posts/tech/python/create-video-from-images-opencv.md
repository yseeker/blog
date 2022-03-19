---
#author: "Hugo Authors"
title: "PythonとOpenCVで画像リストから動画を作成"
date: "2022-03-19"
description: "cv2.VideoWriterを使う."
tags: ["python", "video", "opencv", "動画", "画像", "mp4", "cv2.VideoWriter"]
categories: ["Tech", "Python", "OpenCV"]
ShowToc: true
TocOpen: true
draft: false
---

## openCV を使って画像リストから動画を作成する。

```python
from pathlib import Path
from typing import List

import cv2


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


def create_mp4_video_from_image_path_list(
    output_video_path: str,
    image_path_list: List[str],
    fps: int,
) -> None:
    """
    Create mp4 video file from a image path list

    Parameters
    ----------
    output_video_path : str
        Path of the output video
    image_path_list : List[str]
        Path of image file list
    fps : int
        fps (frames per second)

    """
    height, width, _ = cv2.imread(image_path_list[0]).shape
    writer = cv2.VideoWriter(
        output_video_path,
        cv2.VideoWriter_fourcc("m", "p", "4", "v"),
        fps,
        (width, height),
        True,
    )
    for image_file_path in image_path_list:
        writer.write(cv2.imread(image_file_path))
    writer.release()
    cv2.destroyAllWindows()


file_list = list_file_paths("images")
create_mp4_video_from_image_path_list("output.mp4", file_list, 30)
```
