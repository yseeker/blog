---
#author: "Hugo Authors"
title: "Python高速化メモ"
date: "2021-08-19"
#description: "Sample article showcasing basic Markdown syntax and formatting for HTML elements."
tags: ["Kaggle", "SETI"]
categories: ["Kaggle"]
ShowToc: true
TocOpen: true
draft: true
---

ubuntu 導入

ログインエラー　
ctrl + alt + F2 tty 仮想コンソール

```bash
dpkg -l | grep nvidia
```

```bash
sudo ubuntu-drivers install
sudo reboot
```

cuda も入った。
cuda が入らなかった場合, セキュアブートをオフ

```

```

## 言語を直しておく

https://tech.librastudio.co.jp/entry/index.php/2017/12/20/post-1756/

## docker 導入

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
DRY_RUN=1 sh ./get-docker.sh
```

docker 自動起動
sudo systemctl start docker && sudo systemctl enable docker

```sh
sudo groupadd docker
sudo usermod -aG docker <username>
newgrp docker
```

## ssh 導入

https://frute.hatenablog.com/entry/2018/11/19/003056

ssh-keygen -t ed25519 -C "[maxwell8313@gmail.com](mailto:maxwell8313@gmail.com)"

config の設定

```
Host github github.com
    HostName github.com
    IdentityFile ~/.ssh/github_rsa
    User git
```

sudo 無しで docker を利用する
yusaito@yusaito-ubuntu20:~$ sudo groupadd docker
[sudo] password for yusaito:
groupadd: group 'docker' already exists
yusaito@yusaito-ubuntu20:~$ sudo usermod -aG docker yusaito
yusaito@yusaito-ubuntu20:~$ newgrp docker

メモリ　 free -h
cpu lscpu
cat /proc/meminfo
sudo dmidecode -t baseboard
gpu nvidia -smi
sudo parted -l
確認

scp 遅い対策
/etc/ssh/sshd_config
IPQoS none

.ssh/config
Host \*
IPQoS none

vscode 設定
ファイルの上限を上げておく
black, mypy, flake8, isort をインストール
/usr/bin/python3 -m pip install -U mypy
USER ではなく、ssh 側を設定
