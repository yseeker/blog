---
#author: "Hugo Authors"
title: "Kaggle：SETIコンペ参加記（ソロ銅：71th/768 teams）"
date: "2021-08-19"
tags: ["Kaggle", "SETI", "画像コンペ"]
categories: ["Kaggle"]
ShowToc: true
TocOpen: true
draft: false
aliases:
  - /posts/kaggle/seti/
  - /posts/tech/kaggle/seti/
---

![](images/2021-08-18-14-51-56.png#center)

[SETI Breakthrough Listen - E.T. Signal Search](https://www.kaggle.com/c/seti-breakthrough-listen/overview)という Kaggle の**画像分類コンペ**に参加しました。

## 結果

![](images/2021-08-18-17-41-09.png#center)
774 チーム中 74 位でソロ銅でした。

## コンペの概要

[Overview のページ](https://www.kaggle.com/c/seti-breakthrough-listen/overview)には

> In this competition, use your data science skills to help **identify anomalous signals in scans of Breakthrough Listen targets**. Because there are no confirmed examples of alien signals to use to train machine learning algorithms, the team included some simulated signals (that they call “needles”) in the haystack of data from the telescope. They have identified some of the hidden needles so that you can train your model to find more.

とあって、要するに SETI（Search for Extra Terrestrial Intelligence；地球外知的生命体探査）の研究グループ（Listen チーム）が取得した大量の望遠鏡の信号のデータ（2 次元データ）をシミュレーションによる擬似的な信号（needle）が加えられたデータ（Positive）と無いデータ（Negative）に分類し、その AUC スコアを競うコンペです。地球外知的生命体からの信号発見用の機械学習アルゴリズムを開発するという何ともロマンのあるコンペです。

コンペで使用するデータの例を Negative, Positive で 2 つずつ挙げると（縦軸は時間、横軸は周波数）

![](images/2021-08-18-15-16-48.png#center)

![](images/2021-08-18-15-19-15.png#center)

のようになっており、たしかに Positive データの方には needle らしい特徴が視認できます（赤矢印）。上のデータはわかりやすいデータをあげましたが、実際には少なくとも目で見る限りは Needle らしい特徴なんてどこにもない Positive データもたくさんありました。シグナルよりも圧倒的にノイズが大きいデータもありました。実際の観測データでは、望遠鏡を信号を発する方向に向けた際のデータを ON データ、別の方向に向けた際のデータ OFF データとしているため、今回のデータでは Positive の ON データにのみシミュレーションによって生成した擬似的な needle（信号）をうまく混ぜてあるようです。

![](images/2021-08-18-15-55-16.png#center)

## 参加記

### 2021 年 6 月

- 本業に余裕ができたので 5 年ぶりに Kaggle を真面目にやりたいと思い立つ。画像コンペに参加したことが無かったので、画像コンペを中心に漁り始める。SIIM と SETI の 2 つのコンペを発見した。最初に SIIM をやり始めたが、厳しそうだったのですぐに撤退。
- Google Colab Pro を契約
- Kaggler たちは皆 Pytorch を使っているようなので Pytorch を勉強し始めた。深層学習もすっかり忘れていたので復習した。
- 世の中には timm という神ライブラリがあることを知り、転移学習を覚えた。
- とりあえず Pytorch で一通り書けるようになりまともなスコアが出るようになったので、公開カーネルとディスカッションを読みはじめる。
- 入力は ON チャネルだけにした。
- 4xGrandmaster の[@abhishek](https://www.kaggle.com/abhishek)さんが作った[Tez](https://github.com/abhishekkrthakur/tez)というエコシステムを知り、これを利用しつつ、自分で一からエコシステムを作ったりして Pytorch の理解を深めた。
- mixup という data augumentation を知る。

### リーク発覚

- ローカルに落としたファイルの time stamp などから正解ラベルが特定できる[リークが発覚](https://www.kaggle.com/c/seti-breakthrough-listen/discussion/246772)＝＞ 3-4 週間後にコンペ再スタート

### 2021 年 7 月

- [@ttahara](https://www.kaggle.com/ttahara)さんが公開されていた[pytorch-pfn-extra](https://github.com/pfnet/pytorch-pfn-extras)を使った[Code](https://www.kaggle.com/ttahara/rerun-seti-e-t-resnet18d-baseline)を発見して、便利さに感動したが、web 上に pytorch-pfn-extra の説明があまりなく、すべての解読はまだできていない。
- \*mixup の alpha を 0.5 から 1.5 に変えると efficientnetb0 で Public score が 0.760 から 0.766 に上がった。
- 何もいいアイディアが思い浮かばないので、データの加工（標準化、正規化）、モデルの変更（efficientnet family, resnet family, vgg16bn, mobilenet）などを試すがあまり劇的な効果は得られなかったが、efficientnetb3 が若干良いスコアを出すことが分かった。
- リーク前のデータで pretrain したら少しスコアが上がった。
- これまでのモデルのスコアをアンサンブルをしたら一時期 15 位くらいまで上昇した（残り 1 ヶ月）

### 2021 年 8 月

- TTA, アンサンブル、スタッキングなどを試す。TTA してからアンサンブルすると TTA 無しのアンサンブルよりもスコアが下がって謎だった。
- positive データだけリーク前のデータから追加したが、スコアが下がった。
- Pseudo labeling も試したがうまくいかなかった。
- スタッキングを試すが Public score で 0.780 を超えない。
- [Google Colab Pro ＋にアップグレード](https://zenn.dev/yseeker/articles/21c34b00052aad)
- ラスト 3 日で銀圏から銅圏に追い出される。
- 最終的に 512x512 の画像サイズで学習し、mixup alpha を 1-1.5 で変えたりして、efficientnetb3 x 6 + efficientnetb0 x 3 + resnet34d x 2 + effnetb1 x 1 + effnetb5 x 1 + XGBoost のスタッキングの単純平均アンサンブルを提出。

## 上位陣の解法

### 1 位 <b>Watercooled</b> チーム（[@philippsinger](https://www.kaggle.com/philippsinger)さん、[@philippsinger](https://www.kaggle.com/philippsinger)さん、[@philippsinger](https://www.kaggle.com/philippsinger)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266385]

- "Magic"を使って最終的に 2 位に大差をつけて優勝。
- モデルは First convolution stride (1, 2) + eca_nf_net
  \_l2 + GeM Pooling

1. <b>Magic1</b>: test セットにのみ現れる sin 波を生成して学習させる（=> LB 0.800）
2. <b>Magic2</b>. バックグラウンドノイズの量を大幅減らすため（S/N ratio を上げるため？）のデータ処理　(LB=>0.853)

### 2 位 <b>未知との遭遇</b> チーム（[@hirune924](https://www.kaggle.com/hirune924)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266397]

- Pytorch lightening を用いた圧倒的に簡潔なコード
- logical OR 用の mixup：`y = y + y[index] - (y * y[index])` (これで pseudo lebel のときの soft target になるらしい。)

### 3 位 <b>knj</b>チーム（[@knjcode](https://www.kaggle.com/knjcode)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266403]

- [Convolutional Triplet Attention Module](https://arxiv.org/abs/2010.03045)を Efficient Net に使った解法
- backbone は EfficientNet B1-- B4
- GeM Pooling (p=4)
- Focal Loss (gamma=0.5)
- MADGRAD optimizer
  - Initial Lr 1e-4 LinearWarmupCosineAnnealingLR (warmup_epochs=5)

### 4 位 <b>Steven Signal</b> チーム（[@sherlockkay](https://www.kaggle.com/sherlockkay)さん, [@kulyabin](https://www.kaggle.com/kulyabin)さん, [@bakeryproducts](https://www.kaggle.com/bakeryproducts)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266396]

- 工夫した mixup と cutmix
- FocalLoss, gamma=2, alpha=.7
- モデル: nf-regnetb1, nf-regnetb1, HRNet18,
- timm EMA

### 5 位 <b>SETI の壁</b> チーム（[@kzkt0713](https://www.kaggle.com/kzkt0713)さん, [@sinpcw](https://www.kaggle.com/sinpcw)さん, [@sunakuzira](https://www.kaggle.com/sunakuzira)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266394]

- モデル: eca_nfnet_l2 (4fold) + efficientnet_v2_m (4fold)
- SHOT (https://github.com/tim-learn/SHOT)
- pseudo labeling

上位陣の手法を身に着けて精進していきたいです。
CPMP さんとか僕がのほほんとサンタコンペ出た 5 年前からずっと存在感があってすごい。
