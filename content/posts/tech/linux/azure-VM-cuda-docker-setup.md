---
#author: "Hugo Authors"
title: "AzureでA100x8（V100x4）のPytorch環境構築とエラー対処"
date: "2022-01-11"
description: "Azure A100x8の特有のエラーに遭遇"
tags:
  [
    "Azure",
    "GPU",
    "cuda",
    "docker",
    "A100x8",
    "Data Center GPU manager",
    "fabricmanager",
    "CUDA error",
    "docker: Error response from daemon: could not select device driver “” with capabilities: [[gpu]]",
  ]
categories: ["Tech", "エラー"]
ShowToc: true
TocOpen: true
draft: false
aliases:
  - /posts/tech/azure_vm_setup/
  - /posts/tech/linux/azure_vm_setup/
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
ssh -i ~/.ssh/keys/azure_vm_key.pem azureuser@<public ip address of VM instance>
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

## Data Center GPU manager のインストール（A100x8 の場合）

### bandwidthTest を行う

詳細は、[こちら](https://github.com/pytorch/pytorch/issues/35710#issuecomment-901013741)を参照。
A100x8 ではここでエラーが出る、V100x4 では出ない

```bash
git clone https://github.com/NVIDIA/cuda-samples.git
cd cuda-samples/Samples/bandwidthTest
make
./bandwidthTest
```

### エラー：CUDA error at bandwidthTest.cu:256 code=802(cudaErrorSystemNotReady) "cudaSetDevice(currentDevice)"

```
cudaGetDeviceProperties returned 802
-> system not yet initialized
CUDA error at bandwidthTest.cu:256 code=802(cudaErrorSystemNotReady) "cudaSetDevice(currentDevice)"
it means that the Data Center GPU manager is not installed. What you want to do is to install the nvidia DCGM, fetch the repository keys:
```

### Data Center GPU manager のインストール

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --keyserver-options http-proxy=http://proxy-chain.intel.com:911 --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
```

### エラー：Connection timed out 　 you may need to manually set the proxy:

```
Executing: /tmp/apt-key-gpghome.qjhmgicscb/gpg.1.sh --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
gpg: requesting key from 'https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub'
gpg: WARNING: unable to fetch URI https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub: Connection timed out
you may need to manually set the proxy:
```

### マニュアルでプロキシを設定し、再度 Data center GPU manger をインストール

```bash
sudo apt-key adv --keyserver-options http-proxy=<PROXY-ADDRESS:PORT> --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt-get update
sudo apt-get install -y datacenter-gpu-manager
```

### ホストエンジンの停止

```bash
sudo nv-hostengine -t
```

### fabricmanager を再起動

```bash
sudo service nvidia-fabricmanager start
```

### エラー：Failed to start nvidia-fabricmanager.service: Unit nvidia-fabricmanager.service not found.

```
Failed to start nvidia-fabricmanager.service: Unit nvidia-fabricmanager.service not found.
install the fabric manager and start it:
```

### fabricmanager のインストール

```bash
sudo apt-get install cuda-drivers-fabricmanager-495
sudo service nvidia-fabricmanager start
```

### bandwidthTest を行ってエラーが無いことを確認

```bash
./bandwidthTest
```

### VM インスタンス立ち上げ時にホストエンジンを停止し、fabric manager を再起動 （VM 立ち上げ２回目以降）

```bash
sudo nv-hostengine -t
sudo service nvidia-fabricmanager start
```

## Docker インストールと Pytorch コンテナの確認

```bash
sudo apt update
sudo apt install -y docker.io
sudo docker pull nvcr.io/nvidia/pytorch:21.10-py3
```

```bash
sudo docker run -it --gpus all --shm-size 8g --rm -v $PWD:/work -w /work 030c24bd72ba /bin/bash
```

### エラー:　 docker: Error response from daemon: could not select device driver “” with capabilities: [[gpu]].

```
docker: Error response from daemon: could not select device driver “” with capabilities: [[gpu]]
```

### 解決方法

[こちら](https://www.yurui-deep-learning.com/2021/08/17/docker-error-response-from-daemon-could-not-select-device-driver-with-capabilities-gpu/)を参照

```bash
curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey | sudo apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list | sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
sudo apt-get update
sudo apt-get install -y nvidia-container-runtime
sudo service docker restart
```
