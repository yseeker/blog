---
#author: "Hugo Authors"
title: "Ubuntu 20.04 LTSセットアップ（自宅サーバー用）とリモート環境用の諸々の初期設定（docker + cuda + ssh + vscode）"
date: "2022-03-05"
tags:
  [
    "Ubunu",
    "自宅サーバー",
    "ubuntu20.04",
    "cuda",
    "nvidia-driver",
    "docker",
    "ssh",
    "openssh-server",
    "vscode",
  ]
categories: ["Tech", "Linux"]
ShowToc: true
TocOpen: true
draft: false
aliases:
  - /posts/tech/ubuntu_install/
  - /posts/tech/linux/ubuntu_install/
---

## Ubuntu 20.04 LTS の導入

[こちらの記事](https://qiita.com/koba-jon/items/019a3b4eac4f60ca89c9)に従って、Ubuntu 20.04 LTS を入れた。

### ライブ USB の作成

- Rufus をダウンロード
- ubuntu の iso ファイルをダウンロード
- USB を挿して、Rufus を使ってライブ USB を作成

### Ubuntu 20.04 LTS のインストール

- 細かい設定は[こちらの記事](https://qiita.com/koba-jon/items/019a3b4eac4f60ca89c9)を参照

### インストール後にログインループになってログインできなくなった

- `ctrl + alt + F2`で tty 仮想コンソールを開く
- Nvidia ドライバ, cuda があるかどうか確認

```bash
dpkg -l | grep nvidia
dpkg -l | grep cuda
```

※もしですでにある場合は削除しておく

```bash
sudo apt-get --purge remove nvidia-*
sudo apt-get --purge remove cuda-*
```

- Nvidia ドライバが無かったら下記で Nvidia ドライバと cuda を入れる

```bash
sudo ubuntu-drivers install
sudo reboot
```

または version 指定して入れる。

```bash
sudo apt-get install cuda-drivers-<branch>
```

以上のプロセスでログインできるようになった。またこのときに cuda も一緒に入った。（`nvidia-smi`で確認）

ログインループに陥らなかった場合は別途自分で nvidia ドライバと cuda を入れる必要がある。

一旦きれいににしてから nvidia-driver を入れる

```bash
sudo apt-get --purge remove nvidia-*
sudo apt-get --purge remove cuda-*
sudo ubuntu-drivers install
sudo reboot
```

`nvidia-smi`で確認して、必要であれば cuda を[公式のやり方](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=deb_local)に従って入れる。

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.6.1/local_installers/cuda-repo-ubuntu2004-11-6-local_11.6.1-510.47.03-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2004-11-6-local_11.6.1-510.47.03-1_amd64.deb
sudo apt-key add /var/cuda-repo-ubuntu2004-11-6-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
```

### CPU 情報などを確認

```bash
cpu lscpu
cat /proc/meminfo
sudo dmidecode -t baseboard
gpu nvidia -smi
sudo parted -l
```

## 言語を直しておく

https://tech.librastudio.co.jp/entry/index.php/2017/12/20/post-1756/

## docker 導入

### docker のインストール

```bash
# https://docs.docker.com/engine/install/ubuntu/
curl -fsSL https://get.docker.com -o get-docker.sh
DRY_RUN=1 sh ./get-docker.sh
```

### docker が自動起動するようにしておく

```bash
sudo systemctl start docker && sudo systemctl enable docker
```

### sudo 無しで docker を使えるようにする

```bash
sudo groupadd docker
sudo usermod -aG docker <username>
newgrp docker
```

## ssh 導入

### ssh サーバーのインストール

```bash
sudo apt install openssh-server
```

パスワードでログイン可能にしておく

```bash
sudo vi /etc/ssh/sshd_config
```

```
PasswordAuthentication yes
```

ssh を再起動する

```bash
sudo systemctl restart sshd.service
```

### 鍵を生成して転送

- クライアント側で鍵を生成

```bash
ssh-keygen -t ed25519 -C "username@servername"
```

- ローカル IP を調べる

```bash
hostname -I
```

- 鍵をサーバーに転送

```bash
scp ~/.ssh/my_key.pub ホスト名@<ローカルIP>:
```

- 公開鍵を authorized key に移動

```bash
cat my_key.pub >> .ssh/authorized_keys
rm id_ras.pub
sudo chmod 700 -R /home/user /home/user/.ssh
sudo chmod 600 /home/user/.ssh/authorized_keys
```

### セキュリティを上げておく

```bash
sudo vi /etc/ssh/sshd_config
```

```
PasswordAuthentication no #パスワードログインを許可しない
Port 56666　#ポートを変えておく
```

```bash
sudo systemctl restart sshd.service
```

ssh 接続できない場合はクライアント側の ssh config を設定する

```bash
vi /home/user/.ssh/config
```

```
Host remote-host
    HostName XXX.XX.XX.XX
    Port XXXXX
    IdentityFile ~/.ssh/my_key
    User user
```

※ホームの permission がおかしいと ssh アクセスできないので、アクセスできない場合は変更しておく。

```bash
sudo chown root:root /home
sudo chmod -R 755 /home
sudo chown user:user /home/user -R
sudo chmod 700 -R /home/user /home/user/.ssh
sudo chmod 600 /home/user/.ssh/authorized_keys
```

## リモート VScode の設定

Extention の　`Remote Development`をインストールしておく。
リモート VSCode でファイルの生成や削除で permission エラーが出るのでよく使うフォルダ or ワークスペースにのみ権限を与えておく `sudo chmod -R 777 ./workspace`

### 閲覧可能なファイル数の上限を最大にする

```bash
cat /proc/sys/fs/inotify/max_user_watches

vi /etc/sysctl.conf
# add "fs.inotify.max_user_watches=524288" at the end
sudo sysctl -p
```

### リンターとフォーマッター

- extention で Python をインストール
- black mypy isort flake8 　をインストール

```bash
pip3 install black mypy isort flake8
```

USER と ssh サーバーで下記を設定

- `Python › Formatting: Provider` -> `black`
- `Python › Linting: Mypy Enabled` -> check
- `Editor: Format On Save` -> check
- `Editor: Code Actions On Save` -> setting json

下記の箇所を

```
"editor.codeActionsOnSave": null
```

下記に変更する

```
"editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
```

### その他有用な extention

- **Error Lense** : setting から delay を 500 にしておく
- **pylance** : インタプリタを適切なものに設定しておく。
- **indent rainbow**
- **blacket pair** : いろいろある
- **paste image**
