---
#author: "Hugo Authors"
title: "AzureでA100x8（V100x4）のVMの環境構築とエラー対処"
date: "2022-01-11"
#description: "Sample article showcasing basic Markdown syntax and formatting for HTML elements."
tags: ["Azure", "GPU", "cuda", "docker", "A100x8"]
categories: ["技術", "エラー"]
ShowToc: true
TocOpen: true
draft: false
---

## Azure の web で VM インスタンスを作成

VM インスタンスの作成は[こちら](https://docs.microsoft.com/ja-jp/azure/virtual-machines/linux/quick-create-portal)
秘密鍵をダウンロードして、read 権限を与えていおく。

```bash
cp ~/Downloads/your_key_name.pem ~/.ssh/keys/azure_vm_key.pem
chmod 400 ~/.ssh/keys/azure_vm_key.pem
```

ssh を使って VM にアクセス

```bash
ssh -i ~/.ssh/keys/azure_vm_key.pem azureuser@[public ip address of VM instance]
```

## Cuda をインストール

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/11.5.0/local_installers/cuda-repo-ubuntu1804-11-5-local_11.5.0-495.29.05-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804-11-5-local_11.5.0-495.29.05-1_amd64.deb
sudo apt-key add /var/cuda-repo-ubuntu1804-11-5-local/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
```

## bandwidthTest を行う（A100x8 ではここでエラーが出る、V100x4 では出ない）

```
git clone https://github.com/NVIDIA/cuda-samples.git
cd cuda-samples/Samples/bandwidthTest
make
./bandwidthTest
```

## A100x8 の場合のエラー対策

詳細は、[こちら](https://github.com/pytorch/pytorch/issues/35710#issuecomment-901013741)を参照

A100x8 の場合は上の bandwidth テストで下記のようなエラーが出る。

```
cudaGetDeviceProperties returned 802
-> system not yet initialized
CUDA error at bandwidthTest.cu:256 code=802(cudaErrorSystemNotReady) "cudaSetDevice(currentDevice)"
it means that the Data Center GPU manager is not installed. What you want to do is to install the nvidia DCGM, fetch the repository keys:
```

Data Center GPU manager をインストールする

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --keyserver-options http-proxy=http://proxy-chain.intel.com:911 --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
```

```
Executing: /tmp/apt-key-gpghome.qjhmgicscb/gpg.1.sh --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
gpg: requesting key from 'https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub'
gpg: WARNING: unable to fetch URI https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub: Connection timed out
you may need to manually set the proxy:
```

sudo apt-key adv --keyserver-options http-proxy=<PROXY-ADDRESS:PORT> --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
then you can install the repository and the package:

sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get install -y datacenter-gpu-manager
terminate the host engine:

sudo nv-hostengine -t
and start the fabricmanager

sudo service nvidia-fabricmanager start

Failed to start nvidia-fabricmanager.service: Unit nvidia-fabricmanager.service not found.
install the fabric manager and start it:

sudo apt-get install cuda-drivers-fabricmanager-<version>
sudo service nvidia-fabricmanager start

sudo nv-hostengine -t

sudo service nvidia-fabricmanager start

sudo apt-get install -y cuda-drivers-fabricmanager-495
sudo service nvidia-fabricmanager start

./bandwidthTest

#docker install イメージチェック
sudo apt update
sudo apt install -y docker.io
sudo docker pull nvcr.io/nvidia/pytorch:21.10-py3

sudo docker run -it --gpus all --shm-size 16g --rm -v $PWD:/work -w /work 030c24bd72ba /bin/bash

import torch
torch.cuda.is_available()

# error 対処２

curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt-get install -y nvidia-container-runtime
sudo service docker restart

#データ転送
cd
git clone -b rosinality https://github.com/dtgrid/stylegan2-pytorch stylegan2-pytorch-rosinality

# local

mkdir results data
scp -r saito@192.168.3.254:/home/saito/jpface005_lmdb ~/Downloads/
scp -r -i ~/.ssh/keys/yusaito12.pem ~/Downloads/jpface005_lmdb azureuser@20.97.53.123:stylegan2-pytorch-rosinality/data/
scp -r -i ~/.ssh/keys/yusaito12.pem /Users/yusaito/Downloads/checkpoint/250000.pt azureuser@20.97.53.123:stylegan2-pytorch-rosinality/checkpoint/

tmux new -s pytorch
sudo docker run -it --gpus all --shm-size 16g --rm -v $PWD:/work -w /work 030c24bd72ba /bin/bash

python -m torch.distributed.launch --nproc_per_node=8 --master_port=8890 train.py --ckpt checkpoint/250000.pt --batch 8 --iter 380000 --augment --no_pl_reg data/jpface005_lmdb
python -m torch.distributed.launch --nproc_per_node=8 --master_port=8890 train.py --batch 16 --iter 68000 --name 20211222_jpfac13_512 --size 512 --augment --no_pl_reg data/jpface013_512_lmdb2
