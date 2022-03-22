---
#author: "Hugo Authors"
title: "Python : itertoolsの使い方 -その２-"
date: "2021-12-21"
tags:
  [
    "itertools",
    "itertools product",
    "itertools permutations",
    "itertools 組み合わせ",
    "itertools groupby",
    "itertools isslice",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

product は便利そうだけど、starmap は一行別で生成したほうが分かりやすそう。

### itertools.groupby

同じキーをもつような要素からなる イテレーターのグループに対して、キーとグループを返すようなイテレータを作成する。通常、イテレーターは同じキー関数でソート済みである必要がある。

#### 使い方

```python
for k, g in itertools.groupby('AAAABBBCCDAABBB'):
    print(k)
# --> A B C D A B

for k, g in itertools.groupby('AAAABBBCCD'):
    print(list(g))
# --> AAAA BBB CC D
```

### itertools.islice

要素を選択・スライスして返すイテレータを生成。

#### 使い方

```python
for n in itertools.islice('ABCDEFG', 2):
    print(n)
# --> A B
```

### itertools.pairwise

隣同士をペアにしたイテレータを返す。

#### 使い方

```python
for n in itertools.pairwise('ABCDEFG'):
    print(n)
# --> AB BC CD DE EF FG
```

### itertools.permutations

特定の長さの順列を返す。

#### 使い方

```python
for n in itertools.permutations('ABCD', 2):
    print(n)
# --> AB AC AD BA BC BD CA CB CD DA DB DC
```

### itertools.product

#### 使い方

```python
for n in itertools.product('ABCD', 'xy'):
    print(n)
# --> ('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'), ('C', 'y'), ('D', 'x'), ('D', 'y')

for n in itertools.product(range(2), repeat=3):
    print(n)
# --> (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)
```

### itertools.repeat

繰り返しのイテレータを生成

#### 使い方

```python
for n in itertools.repeat(10, 3):
    print(n)
# --> A B C D E F
```

### itertools.starmap

イテレータ の要素を引数として 関数 を計算するイテレータを作成します

#### 使い方

```python
for n in itertools.starmap(pow, [(2,5), (3,2), (10,3)]):
    print(n)
# --> 32 9 1000
```

### itertools.takewhile

predicate が真である限り iterable から要素を返すイテレータを作成する

#### 使い方

```python
for n in itertools.takewhile(lambda x: x<5, [1,4,6,4,1]):
    print(n)
# --> 1 4
```

### itertools.zip_longest

通常の zip は短いイテレータの合わされるが、長い方に合わせる用。

#### 使い方

```python
for n in itertools.zip_longest('ABCD', 'xy', fillvalue='-'):
    print(n)
# --> Ax By C- D-
```

```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="itertools --- 効率的なループ実行のためのイテレータ生成関数" src="https://hatenablog-parts.com/embed?url=https://docs.python.org/ja/3/library/itertools.html" frameborder="0" scrolling="no"></iframe>
```
