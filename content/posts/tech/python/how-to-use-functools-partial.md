---
#author: "Hugo Authors"
title: "Python:functools.partial 関数の引数を一部固定"
date: "2022-02-26"
tags: ["python", "functools.partial", "functools", "引数固定"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

functools.partial は、関数の特定の引数を固定したい場合に使う 個人的に concurrent.futures の ProcessPoolExecuter や ThreadPoolExecuter の map を使うときに併用することが多い。

## functools.partial の定義

```python
# ref. https://docs.python.org/ja/3/library/functools.html#functools.partial

def partial(func, /, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = {**keywords, **fkeywords}
        return func(*args, *fargs, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```

## 使い方：引数を固定する

```python
from functools import partial

def product_xyz(x, y, z):
    return x * y * z

# xとyの値を固定する
product_z = partial(product_xyz, x=2, y=3)
product_z(4)
# 24
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:720px;" title="https://docs.python.org/ja/3/library/functools.html#functools.partial" src="https://hatenablog-parts.com/embed?url=https://docs.python.org/ja/3/library/functools.html#functools.partial" frameborder="0" scrolling="no"></iframe>
