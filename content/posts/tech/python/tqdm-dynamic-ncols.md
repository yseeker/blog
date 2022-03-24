---
#author: "Hugo Authors"
title: "tqdmでターミナルの横幅を狭めるとバグる問題を解消する"
date: "2022-02-17"
tags: ["python", "tqdm", "logging", "print", "dynamic_ncols", "標準出力"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## 問題 : tqdm を標準出力している状態でターミナルの横幅を狭めるとバグる

### 解決策 : dynamic_ncols=True にする

下記のように tqdm を定義すればよい（[参考](https://github.com/tqdm/tqdm/issues/370)）

```python
from functools import partial
from tqdm import tqdm as std_tqdm
tqdm = partial(std_tqdm, dynamic_ncols=True)
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="Make dynamic_ncols=True the default #370" src="https://hatenablog-parts.com/embed?url=https://github.com/tqdm/tqdm/issues/370" frameborder="0" scrolling="no"></iframe>
