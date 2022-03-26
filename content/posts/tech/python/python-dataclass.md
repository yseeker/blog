---
#author: "Hugo Authors"
title: "Python : Dataclassを試してみる"
date: "2022-01-18"
tags: ["Python", "dataclass"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

Python3.7 から加わった Dataclass に関して全く知らなかったので参考煮上げた記事を読みながらメモ.

## 通常の class と Dataclass の比較

### 通常の class

```python
class Person:
    def __init__(self, age = 20, gender = "female"):
        self.gender = gender
        self.age = age
```

### Dataclass

```python
from dataclasses import dataclass
@dataclass
class DataclassPerson:
    gender: str = "female"
    age: int = 20
```

## DataClass の利点

- 可読性が高まる。
- 型アノテーションができる。
- asdict で（ネストされたものでも）辞書に変換可能

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="Python3.7以上のデータ格納はdataclassを活用しよう" src="https://hatenablog-parts.com/embed?url=https://qiita.com/ttyszk/items/01934dc42cbd4f6665d2" frameborder="0" scrolling="no"></iframe>
