---
#author: "Hugo Authors"
title: "Template"
date: "2022-03-19"
tags: ["template"]
categories: ["Tech", "template"]
ShowToc: true
TocOpen: true
draft: true
---

### list から pd.DataFrame へ変換

```python
df = pd.DataFrame({'list_1':list_1, 'list_2':list_2, 'list_3'=list_3})
df = pd.DataFrame(data=zip(list_1,list_2,list_3),columns=['list_1','list_2','list_3'])
```

### pd.DataFrame（Series） から list へ変換

```python
list_2d = df.to_numpy().tolist()
list_1d = df["list_1d"].to_numpy().tolist()

print(df_index.index.tolist())
print(df_index.columns.tolist())
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="PIL IOError: image file truncated with big images" src="Take multiple lists into dataframe=https://stackoverflow.com/questions/30522724/take-multiple-lists-into-dataframe" frameborder="0" scrolling="no"></iframe>
