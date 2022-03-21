---
#author: "Hugo Authors"
title: "Pathlibの使い方"
date: "2022-01-19"
tags: ["Pathlib", "Path", "Python", "glob"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## 基本操作

### ファイル名取得

### ディレクトリ名取得

```python
from pathlib import Path
path = Path("./dir/filename.txt")
```

- ファイル名を取得 : `path.name`
- ファイル名拡張子抜き : `path.stem`
- ファイルの拡張子のみ : `path.suffix`
- ファイルのディレクトリを取得 : `path.parents` (list)
- パス連結 : `/` 演算子を使う（`path.joinpath()`）
- パスの存在確認：`path.exists()`
- ファイルかどうか確認 : `path.is_file()`
- ディレクトリかどうか確認 : `path.is_dir()`
- ディレクトリの作成 : `path.mkdir(exist_ok=True, parents=True)`
- ディレクトリの削除 : `path.rmdir()`
- ファイル/ディレクトリパス変更 : `path.replace(tgt)`
- ファイル/ディレクトリパス変更（末尾のみ）: `path.rename(new_file_apth)`
- 同じ階層に別名ファイルを作成 : `path.with_name('file_new.txt').touch()`
- 同じ階層に別拡張子ファイルを作成 : `path.with_suffix('png').touch()`
- 同じ階層のファイルとディレクトリ一覧を返す：`path.iterdir()`
- ファイルの存在ディレクトリのパスを取得：`Path(__file__).parent`

## 個人的によく使うモジュール

### ファイルを再帰的に探索

- Pathlib の場合

```python
# Pathlibの場合
from pathlib import Path
from typing import List

def list_file_paths(dir_path: str) -> List[str]:
    """
    List file paths in a directory.

    Parameters
    ----------
    dir_path : str
        Path for the directory

    Returns
    -------
    List[str]
        List of the file paths in the directory
    """
    return sorted([str(path) for path in Path(dir_path).rglob("*") if path.is_file()])
```

- os + glob の場合

```python
# os + globの場合
import os
import glob
from typing import List

def list_file_paths(dir_path: str) -> List[str]:
    """
    List file paths in a directory.

    Parameters
    ----------
    dir_path : str
        Path for the directory

    Returns
    -------
    List[str]
        List of the file paths in the directory
    """
    return sorted(
        [
            path
            for path in glob.glob(os.path.join(dir_path, "**"), recursive=True)
            if os.path.isfile(path)
        ]
    )
```

### ファイル名の一括変換

```python
def add_suffix_to_all_file_paths(dir_path: str) -> List[str]:
    """
    Add suffix to all the file name

    Parameters
    ----------
    dir_path : str
        Path for the directory

    Returns
    -------
    List[str]
        List of the file paths in the directory
    """
    return sorted(
        [
            str(
                path.rename(
                    str(path.parent / Path(path.stem + "_suffix" + path.suffix))
                )
            )
            for path in Path(dir_path).rglob("*")
            if path.is_file()
        ]
    )
```
