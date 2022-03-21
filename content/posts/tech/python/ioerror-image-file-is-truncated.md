---
#author: "Hugo Authors"
title: "エラーメモ：IOError: image file is truncated"
date: "2022-01-03"
tags:
  [
    "python",
    "Pillow",
    "IOError: image file is truncated",
    "ImageFile.LOAD_TRUNCATED_IMAGES = True",
  ]
categories: ["Tech", "Python", "Pillow", "エラー"]
ShowToc: true
TocOpen: true
draft: false
aliases:
  - /posts/tech/python/ioe-image-file-is-truncated/
---

## IOError: image file is truncated

jpg で結構大きめの画像を Pillow で読み込むときに下記のエラーが出た。

```
IOError: image file is truncated
```

### 解決策

```python
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:720px;" title="PIL IOError: image file truncated with big images" src="https://hatenablog-parts.com/embed?url=https://stackoverflow.com/questions/12984426/pil-ioerror-image-file-truncated-with-big-images" frameborder="0" scrolling="no"></iframe>
