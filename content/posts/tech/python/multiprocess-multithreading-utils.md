---
#author: "Hugo Authors"
title: "Pythonでファイルリストからの並列処理"
date: "2022-02-03"
tags:
  [
    "Pathlib",
    "Path",
    "multiprocess",
    "joblib",
    "ProcessPoolExecutor",
    "ThreadPoolExecutor",
    "マルチプロセス",
    "マルチスレッド",
  ]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## ファイルのリストを受け取って何らかの並列処理をする。

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import List

def list_file_paths(dir_path: str) -> List[str]:
    """
    List file paths in a directory.

    Parameters
    ----------
    dir_path : str
        Path of the directory

    Returns
    -------
    List[str]
        List of the file paths in the directory
    """
    return sorted([str(path) for path in Path(dir_path).rglob("*") if path.is_file()])


def task(same_value, same_value2, diffent_values):
    return None

def multiprocess_task(task, same_value, same_value2, diffent_values):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(
            partial(task, same_value, same_value2),
            different_values
        ))

def multithreading_task(task, same_value, same_value2, diffent_values):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(
            partial(task, same_value, same_value2),
            different_values
        ))

def joblib_multiprocess_task(task : function, same_value, same_value2, diffent_values):
    results = joblib.Parallel(n_jobs=-1)(
        joblib.delayed(partial(task, same_value, same_value2))(different_value) for different_value in different_values)
```
