---
#author: "Hugo Authors"
title: "Python : more-itertoolsの使い方 -その１-"
date: "2021-12-23"
tags:
  [
    "itertools",
    "itertools combinations",
    "itertools 組み合わせ",
    "itertools count",
    "itertools chain",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: true
---

Atcoder などを昔解いていたときに itertools 便利だなーと思いつつも使いこなせていなかったので総まとめ。

## itertools の解説その１

### itertools.accumulate

累積和を返すイテレータを作成できる。

#### 使い方

```python
for n in itertools.accumulate([1,2,3,4,5]):
    print(n)
# --> 1 3 6 10 15
```

### itertools.chain

２つのシーケンスを１つのシーケンスとして扱う。

#### 使い方

```python
for n in itertools.chain('ABC', 'DEF'):
    print(n)
# --> A B C D E F
```

### itertools.combinations

特定の長さの組み合わせを返す。出力は辞書式でソートされている。

#### 使い方

```python
for n in itertools.combinations('ABCD', 2):
    print(n)
# --> AB AC AD BC BD CD
```

### itertools.combinations_with_replacement

特定の長さの組み合わせを返す。出力は辞書式でソートされている。同じ要素が複数回現れることを許容。

#### 使い方

```python
for n in itertools.combinations_with_replacement('ABC', 2):
    print(n)
# --> AA AB AC BB BC CC
```

### itertools.compress

Bool のリストも入れて、真の値だけのものだけを返す。

#### 使い方

```python
for n in itertools.compress('ABCDEF', [1,0,1,0,1,1]):
    print(n)
#  --> A C E F
```

### itertools.count

あるかずでスタートして、等間隔の値を返すイテレータを作成する。

#### 使い方

```python
for n in itertools.count(2.5, 0.5):
    print(n)
# -> 2.5 3.0 3.5
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="PIL IOError: image file truncated with big images" src="https://hatenablog-parts.com/embed?url=https://stackoverflow.com/questions/12984426/pil-ioerror-image-file-truncated-with-big-images" frameborder="0" scrolling="no"></iframe>
