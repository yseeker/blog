---
#author: "Hugo Authors"
title: "Pandas : サイズの大きいcsvファイルをpickleかfeatherに変換 "
date: "2022-01-08"
tags: ["python", "pandas", "read_csv", "pickle", "feather"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## read_csv が遅い問題

20GB くらいの csv ファイルを `pandas.DataFrame` の `read_csv` で読み込んだ際に２分くらいかかったので、feather と pickle への書き出しを検討したのでその際のメモ。

- `read_csv` : 130sec
- `read_feather` : 5sec
- `read_pickle` : 2.5sec

```python
from contextlib import contextmanager
from time import time

import pandas as pd


@contextmanager
def timer(process_name):
    start = time()
    yield
    print(f"[{process_name}] done in {time() - start:.2f} s")


with timer("pkl"):
    df = pd.read_pickle("data/input/train.pkl")

with timer("feather"):
    df = pd.read_feather("data/input/train.feather")

with timer("csv"):
    df = pd.read_csv("data/input/train.csv")
```

ちなみに pickle の書き出しと、読み込みのときの pandas の version が違うと `AttributeError: Can't get attribute '_unpickle_block' on <module 'pandas._libs.internals' from '/opt/conda/lib/python3.8/site-packages/pandas/_libs/internals.cpython-38-x86_64-linux-gnu.so'>`というエラーが出るのでバージョンをあわせた状態で書き出しと読み込みを行う必要がある。

### 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="AttributeError: Can't get attribute 'new_block' on <module 'pandas.core.internals.blocks'>" src="https://hatenablog-parts.com/embed?url=https://stackoverflow.com/questions/68625748/attributeerror-cant-get-attribute-new-block-on-module-pandas-core-internal" frameborder="0" scrolling="no"></iframe>

## csv から pikcle / feather に変換を行う

```python
from pathlib import Path

import pandas as pd

def csv2pickle(input_path: str) -> None:
    _input_path = Path(input_path)
    df = pd.read_csv(_input_path)
    df.to_pickle(_input_path.with_suffix(".pkl"))

def csv2feather(input_path: str) -> None:
    _input_path = Path(input_path)
    df = pd.read_csv(_input_path)
    df.to_feather(_input_path.with_suffix(".feather"))
```

## コラム指定と型指定も同時に行う

```python
# ex usecols = ["name". "age", "gender"]
# dtypes = {"name" : str, "age", int8, "gender" : str}
def csv2pickle_custom(input_path: str, usecols: list, dtypes: dict) -> None:
    _input_path = Path(input_path)
    df = pd.read_csv(_input_path, usecols=usecols, dtype=dtypes)
    df.to_pickle(_input_path.with_suffix(".pkl"))

def csv2feather_custom(input_path: str, usecols: list, dtypes: dict) -> None:
    _input_path = Path(input_path)
    df = pd.read_csv(_input_path, usecols=usecols, dtype=dtypes)
    df.to_feather(_input_path.with_suffix(".feather"))
```
