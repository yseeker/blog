---
#author: "Hugo Authors"
title: "PythonとopenCVで並列化"
date: "2022-03-18"
#description: "cv2.setNumThreads(0)＆マルチプロセスをやめる"
tags:
  [
    "multithreading",
    "並列化",
    "高速化",
    "マルチスレッド",
    "マルチプロセス",
    "openCV",
    "ThreadPoolExecuter",
    "cv2.setNumThreads",
    "ProcessPoolExecuter",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## openCV でマルチプロセス化しようとしてもシングルプロセスになっている問題に遭遇

Python で openCV を使った処理をマルチプロセス化してみたのだが、どうもシングルプロセスになってしまうという問題に遭遇した。

### 解決策：cv2.setNumThreads(0)＆マルチプロセスをやめる。

```python
cv2.setNumThreads(0)
```

を加えて、かつマルチスレッド化（例えば、`concurrent.future.ThreadPoolExecuter`など）することで効率的に並列処理可能になることが分かった。
`cv2.setNumThreads(0)`有りでも`concurrent.future.ProcessPoolExecuter`では、正しくマルチプロセスされなかった。

以下テンプレート。

```python
import cv2
from concurrent.futures import ThreadPoolExecutor

cv2.setNumThreads(0)

def task_using_cv2(param):
    do_some_process_using_cv2()
    return

with ThreadPoolExecutor() as executor:
    results = list(executor.map(task_using_cv2, param))
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:720px;" title="opencv × multiprocessing がどうもうまくいかない【cv2.cvtColor】" src="https://hatenablog-parts.com/embed?url=https://twdlab.hatenablog.com/entry/2018/08/13/015842" frameborder="0" scrolling="no"></iframe>

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:720px;" title="OpenCV + Python multiprocessing breaks on OSX #5150" src="https://hatenablog-parts.com/embed?url=https://github.com/opencv/opencv/issues/5150" frameborder="0" scrolling="no"></iframe>
