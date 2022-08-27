---
#author: "Hugo Authors"
title: "Pythonで並列処理 : MPIREの使い方"
date: "2022-03-09"
tags:
  [
    "Python",
    "マルチプロセス",
    "並列化",
    "MPIRE",
    "MPIRE for Python: MultiProcessing Is Really Easy",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: true
---

Python では joblib や concurrent.futures などで簡単にマルチプロセスできるが、"MultiProcessing Is Really Easy"という名の [MPIRE](https://slimmer-ai.github.io/mpire/) というライブラリを見つけたので備忘録として残しておく。[この記事](https://towardsdatascience.com/mpire-for-python-multiprocessing-is-really-easy-d2ae7999a3e9)によると、特定の場合では joblib や concurrent.futures よりも性能が良いらしい。

## [MPIRE のインストール](https://slimmer-ai.github.io/mpire/getting_started.html)

```bash
pip install mpire
```

## MPIRE の使い方

```python
from mpire import WorkerPool

def time_consuming_function(param):
    return None

with WorkerPool(n_jobs=8) as pool:
    results = pool.map_unordered(time_consuming_function, interator, progress_bar=True)

```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="MPIRE for Python: MultiProcessing Is Really Easy" src="https://hatenablog-parts.com/embed?url=https://towardsdatascience.com/mpire-for-python-multiprocessing-is-really-easy-d2ae7999a3e9/" frameborder="0" scrolling="no"></iframe>
