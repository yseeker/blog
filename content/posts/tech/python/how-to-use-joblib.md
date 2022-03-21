---
#author: "Hugo Authors"
title: "joblibの使い方"
date: "2022-03-15"
tags:
  [
    "joblib",
    "キャッシュ",
    "並列化",
    "使い方",
    "Parallel",
    "delayed",
    "joblib.load",
    "joblib.dump",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

joblib には主な機能として、1) 時間がかかる処理のキャッシュ化, 2)並列処理, 3)圧縮書き出しと読み込み、がある。

## [joblib のインストール](https://joblib.readthedocs.io/en/latest/installing.html)

```bash
pip install joblib
```

## [joblib の主な機能](https://joblib.readthedocs.io/en/latest/index.html#main-features)

### 時間がかかる処理のキャッシュ化 (Memory)

途中で止まってしまったら困る数分とか数時間とかかかる処理のキャッシュをとっておきたいときに使う。

```python
from joblib import Memory
cachedir = 'cache_dir'
mem = Memory(cachedir)
square = mem.cache(heavy_task_func)
b = do_time_consuming_func(a)
```

### 並列処理 (Parallel, delayed)

デフォルトはマルチプロセスだが、マルチスレッドも選択可能。

#### マルチプロセス（デフォルト）

```python
from joblib import Parallel, delayed
Parallel(n_jobs=-1)(delayed(task_func)(param) for param in iterator)
```

#### マルチスレッド

```python
Parallel(n_jobs=-1, backend='threading')(delayed(task_func)(param) for param in iterator)
```

### オブジェクトの圧縮書き出し（永続化）と読み込み（dump, load）

#### 書き出し（永続化）

```
joblib.dump(object,file_path,compress=3)
```

#### 読み込み

```
object = joblib.load(file_path)
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:720px;" title="Joblib: running Python functions as pipeline jobs" src="https://hatenablog-parts.com/embed?url=https://joblib.readthedocs.io/en/latest/" frameborder="0" scrolling="no"></iframe>
