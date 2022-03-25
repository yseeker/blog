---
#author: "Hugo Authors"
title: "Python : itertoolsの使い方 -その１-"
date: "2021-12-20"
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
draft: false
---

Atcoder などを昔解いていたときに itertools 便利だなーと思いつつも使いこなせていなかったので総まとめ。

## itertools の解説その１

### itertools.accumulate

累積和を返すイテレータを作成できる。

#### >使い方

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

### itertools.cycle

イテレータから無限にサイクルを生成する。

#### 使い方

```python
for n in itertools.cycle('ABCD'):
    print(n)
# --> A B C D A B C D A B C D
```

### itertools.dropwhile

predicate（第一引数）が真になるまで値を飛ばす。

#### 使い方

```python
for n in itertools.dropwhile(lambda x: x<5, [1,4,6,4,1]):
    print(n)
# --> 6 4 1
```

### itertools.filterfalse

イテレーターから predicate（第一引数） が False となる要素だけを返す。

#### 使い方

```python
for n in itertools.ilterfalse(lambda x: x%2, range(10)):
    print(n)
# --> 0 2 4 6 8
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="itertools --- 効率的なループ実行のためのイテレータ生成関数" src="https://hatenablog-parts.com/embed?url=https://docs.python.org/ja/3/library/itertools.html" frameborder="0" scrolling="no"></iframe>
