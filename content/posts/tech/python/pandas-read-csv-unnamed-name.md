---
#author: "Hugo Authors"
title: "Pandasでread_csvしたときに出現するUnnamed:0を消す方法"
date: "2022-02-25"
tags: ["python", "pandas", "read_csv", "コラム", "Unamed: 0"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: False
---

## 問題：Pandas で csv を読むと謎の Unnamed:0 というコラムが出現

### 解決策

#### その１ : pd.read_csv で index_col = 0 を指定

```python
df = pd.read_csv('test.csv', index_col=0)
```

#### その２ : そもそも保存するときに index を消す

```python
df = pd.to_csv('test.csv', index = False)
```

### pandas の中身

ちなみに `Unnamed:0` は[この辺り](https://github.com/pandas-dev/pandas/blob/ad190575aa75962d2d0eade2de81a5fe5a2e285b/pandas/tests/io/parser/test_mangle_dupes.py#L134-L135)で追加されているらしい。

```python
# ref. https://github.com/pandas-dev/pandas/blob/ad190575aa75962d2d0eade2de81a5fe5a2e285b/pandas/tests/io/parser/test_mangle_dupes.py#L120-L140
@skip_pyarrow
def test_mangled_unnamed_placeholders(all_parsers):
    # xref gh-13017
    orig_key = "0"
    parser = all_parsers

    orig_value = [1, 2, 3]
    df = DataFrame({orig_key: orig_value})

    # This test recursively updates `df`.
    for i in range(3):
        expected = DataFrame()

        for j in range(i + 1):
            col_name = "Unnamed: 0" + f".{1*j}" * min(j, 1)
            expected.insert(loc=0, column=col_name, value=[0, 1, 2])

        expected[orig_key] = orig_value
        df = parser.read_csv(StringIO(df.to_csv()))

        tm.assert_frame_equal(df, expected)

```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="pandas の to_csv -> read_csv で Unnamed: 0 が追加された場合の対処法" src="https://hatenablog-parts.com/embed?url=https://qiita.com/wariichi/items/988b16dc4941ccbe7af2" frameborder="0" scrolling="no"></iframe>
