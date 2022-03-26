---
#author: "Hugo Authors"
title: "nvcr.io/nvidia/pytorchのイメージからdockerコンテナを作成したときのNOTE"
date: "2022-03-23"
tags:
  [
    "Pytorch",
    "python",
    "docker",
    "nvcr.io/nvidia/pytorch",
    "NGC",
    "--ipc=host",
    "--ulimit memlock=-1",
    "--ulimit stack=67108864",
  ]
categories: ["Tech", "Linux"]
ShowToc: true
TocOpen: true
draft: false
---

## NGC 提供の Pytorch イメージを使って docker コンテナを立ち上げる。

[NVIDIA NGC | CATALOG](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch)から NGC(NVIDIA GPU CLOUD)が提供している、Pytorch の docker イメージをとりあえず`docker run`をしてみる。

```bash
docker run --gpus all -it --rm nvcr.io/nvidia/pytorch:21.12-py3 /bin/bash
```

すると、下記のような NOTE が一番下に現れたので調べてみた。

```
NOTE: The SHMEM allocation limit is set to the default of 64MB.
This may be insufficient for PyTorch.  NVIDIA recommends the use
of the following flags: docker run --gpus all --ipc=host --ulimit
memlock=-1 --ulimit stack=67108864 ...
```

### The SHMEM allocation limit is set to the default of 64MB

一時ファイル領域の`/dev/shm` のサイズでデフォルト値は 64GB。`--shm-size 2g` みたいにしておけばよい。

### --ipc=host

コンテナとホスト間でメモリ共有するためにつけるらしい。自分の場合は普段使わなそう。

### --ulimit memlock=-1

占有可能なメモリスペースを無限にする。

### --ulimit stack=67108864

スタック領域サイズの上限いっぱいまであげる。

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="Docs » Engine リファレンス » コマンドライン・リファレンス » run" src="https://hatenablog-parts.com/embed?url=http://docs.docker.jp/v19.03/engine/reference/commandline/run.html" frameborder="0" scrolling="no"></iframe>
