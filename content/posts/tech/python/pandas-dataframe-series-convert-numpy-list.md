---
#author: "Hugo Authors"
title: "Template"
date: "2022-03-19"
tags: ["template"]
categories: ["Tech", "template"]
ShowToc: true
TocOpen: true
draft: false
---

## Pandas.DataFrame/Series と numpy.ndarray と list の相互変換

### (複数の) list から pd.DataFrame へ変換

大きく２つの方法がある。

```python
df = pd.DataFrame({'list_1':list_1, 'list_2':list_2, 'list_3'=list_3})
df = pd.DataFrame(data=zip(list_1,list_2,list_3),columns=['list_1','list_2','list_3'])
```

### numpy.ndarray から pd.DataFrame へ変換

```python
# numpy_array
# [[ 0  1  2]
#  [ 3  4  5]
#  [ 6  7  8]]
df = pd.DataFrame(data=numpy_array,columns=['col_1','col_2','col_3'])

#   col_1 col_2 col_3
# 0  0.0   1.0   2.0
# 1  3.0   4.0   5.0
# 2  6.0   7.0   8.0
```

### pd.DataFrame（Series） から list へ変換

```python
# pandas.DataFrame to numpy.ndarray to list
list_2d = df.to_numpy().tolist()

# pandas.Series to numpy.ndarray to list
list_1d = df["list_1d"].to_numpy().tolist()
```

#### 注意

`df.values` でも `numpy.ndarray` が取得できるが、現在は非推奨であり、`df.to_numpy()` が推奨されている。

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="Take multiple lists into dataframe" src="https://hatenablog-parts.com/embed?url=https://stackoverflow.com/questions/30522724/take-multiple-lists-into-dataframe" frameborder="0" scrolling="no"></iframe>
