---
#author: "Hugo Authors"
title: "Kaggle：SETIコンペ参加記（ソロ銅：71th/768 teams）"
date: "2021-08-19"
#description: "Sample article showcasing basic Markdown syntax and formatting for HTML elements."
tags: ["kaggle"]
categories: ["kaggle"]
series: ["kaggle"]
aliases: ["/kaggle_seti"]
ShowToc: true
TocOpen: true
draft: false
---

![](images/2021-08-18-14-51-56.png#center)

[SETI Breakthrough Listen - E.T. Signal Search](https://www.kaggle.com/c/seti-breakthrough-listen/overview)というKaggleの**画像分類コンペ**に参加しました。

## 結果
![](images/2021-08-18-17-41-09.png#center)
774チーム中74位でソロ銅でした。

## コンペの概要

[Overviewのページ](https://www.kaggle.com/c/seti-breakthrough-listen/overview)には
> In this competition, use your data science skills to help **identify anomalous signals in scans of Breakthrough Listen targets**. Because there are no confirmed examples of alien signals to use to train machine learning algorithms, the team included some simulated signals (that they call “needles”) in the haystack of data from the telescope. They have identified some of the hidden needles so that you can train your model to find more. 

とあって、要するにSETI（Search for Extra Terrestrial Intelligence；地球外知的生命体探査）の研究グループ（Listenチーム）が取得した大量の望遠鏡の信号のデータ（2次元データ）をシミュレーションによる擬似的な信号（needle）が加えられたデータ（Positive）と無いデータ（Negative）に分類し、そのAUCスコアを競うコンペです。地球外知的生命体からの信号発見用の機械学習アルゴリズムを開発するという何ともロマンのあるコンペです。

コンペで使用するデータの例をNegative, Positiveで2つずつ挙げると（縦軸は時間、横軸は周波数）

![](images/2021-08-18-15-16-48.png#center)

![](images/2021-08-18-15-19-15.png#center)

のようになっており、たしかにPositiveデータの方にはneedleらしい特徴が視認できます（赤矢印）。上のデータはわかりやすいデータをあげましたが、実際には少なくとも目で見る限りはNeedleらしい特徴なんてどこにもないPositiveデータもたくさんありました。シグナルよりも圧倒的にノイズが大きいデータもありました。実際の観測データでは、望遠鏡を信号を発する方向に向けた際のデータをONデータ、別の方向に向けた際のデータOFFデータとしているため、今回のデータではPositiveのONデータにのみシミュレーションによって生成した擬似的なneedle（信号）をうまく混ぜてあるようです。

![](images/2021-08-18-15-55-16.png#center)

## 参加記

### 2021年6月
*  本業に余裕ができたので5年ぶりにKaggleを真面目にやりたいと思い立つ。画像コンペに参加したことが無かったので、画像コンペを中心に漁り始める。SIIMとSETIの2つのコンペを発見した。最初にSIIMをやり始めたが、厳しそうだったのですぐに撤退。
* Google Colab Proを契約
*  Kagglerたちは皆Pytorchを使っているようなのでPytorchを勉強し始めた。深層学習もすっかり忘れていたので復習した。
*  世の中にはtimmという神ライブラリがあることを知り、転移学習を覚えた。
*  とりあえずPytorchで一通り書けるようになりまともなスコアが出るようになったので、公開カーネルとディスカッションを読みはじめる。
* 入力はONチャネルだけにした。
*  4xGrandmasterの[@abhishek](https://www.kaggle.com/abhishek)さんが作った[Tez](https://github.com/abhishekkrthakur/tez)というエコシステムを知り、これを利用しつつ、自分で一からエコシステムを作ったりしてPytorchの理解を深めた。
*  mixupというdata augumentationを知る。

### リーク発覚
*  ローカルに落としたファイルのtime stampなどから正解ラベルが特定できる[リークが発覚](https://www.kaggle.com/c/seti-breakthrough-listen/discussion/246772)＝＞3-4週間後にコンペ再スタート

### 2021年7月
* [@ttahara](https://www.kaggle.com/ttahara)さんが公開されていた[pytorch-pfn-extra](https://github.com/pfnet/pytorch-pfn-extras)を使った[Code](https://www.kaggle.com/ttahara/rerun-seti-e-t-resnet18d-baseline)を発見して、便利さに感動したが、web上にpytorch-pfn-extraの説明があまりなく、すべての解読はまだできていない。
* *mixupのalphaを0.5から1.5に変えるとefficientnetb0でPublic scoreが0.760から0.766に上がった。
* 何もいいアイディアが思い浮かばないので、データの加工（標準化、正規化）、モデルの変更（efficientnet family, resnet family, vgg16bn, mobilenet）などを試すがあまり劇的な効果は得られなかったが、efficientnetb3が若干良いスコアを出すことが分かった。
* リーク前のデータでpretrainしたら少しスコアが上がった。
* これまでのモデルのスコアをアンサンブルをしたら一時期15位くらいまで上昇した（残り1ヶ月）

  
### 2021年8月
* TTA, アンサンブル、スタッキングなどを試す。TTAしてからアンサンブルするとTTA無しのアンサンブルよりもスコアが下がって謎だった。
* positiveデータだけリーク前のデータから追加したが、スコアが下がった。
* Pseudo labelingも試したがうまくいかなかった。
* スタッキングを試すがPublic scoreで0.780を超えない。
* [Google Colab Pro＋にアップグレード](https://zenn.dev/yseeker/articles/21c34b00052aad)
* ラスト3日で銀圏から銅圏に追い出される。
* 最終的に512x512の画像サイズで学習し、mixup alphaを1-1.5で変えたりして、efficientnetb3 x 6 + efficientnetb0 x 3 + resnet34d x 2 + effnetb1 x 1 + effnetb5 x 1 + XGBoostのスタッキングの単純平均アンサンブルを提出。
  
## 上位陣の解法

### 1位 <b>Watercooled</b> チーム（[@philippsinger](https://www.kaggle.com/philippsinger)さん、[@philippsinger](https://www.kaggle.com/philippsinger)さん、[@philippsinger](https://www.kaggle.com/philippsinger)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266385]

* "Magic"を使って最終的に2位に大差をつけて優勝。
* モデルは First convolution stride (1, 2) + eca_nf_net
_l2 + GeM Pooling

1. <b>Magic1</b>: testセットにのみ現れるsin波を生成して学習させる（=> LB 0.800）
2. <b>Magic2</b>. バックグラウンドノイズの量を大幅減らすため（S/N ratioを上げるため？）のデータ処理　(LB=>0.853)

### 2位 <b>未知との遭遇</b> チーム（[@hirune924](https://www.kaggle.com/hirune924)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266397]

* Pytorch lighteningを用いた圧倒的に簡潔なコード
*  logical OR用のmixup：`y = y + y[index] - (y * y[index])` (これでpseudo lebelのときのsoft targetになるらしい。)


### 3位 <b>knj</b>チーム（[@knjcode](https://www.kaggle.com/knjcode)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266403]

* [Convolutional Triplet Attention Module](https://arxiv.org/abs/2010.03045)をEfficient Netに使った解法
* backboneは EfficientNet B1-- B4
* GeM Pooling (p=4)
* Focal Loss (gamma=0.5)
* MADGRAD optimizer
  * Initial Lr 1e-4 LinearWarmupCosineAnnealingLR (warmup_epochs=5)

### 4位 <b>Steven Signal</b> チーム（[@sherlockkay](https://www.kaggle.com/sherlockkay)さん, [@kulyabin](https://www.kaggle.com/kulyabin)さん, [@bakeryproducts](https://www.kaggle.com/bakeryproducts)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266396]

* 工夫したmixupとcutmix
* FocalLoss, gamma=2, alpha=.7
* モデル: nf-regnetb1, nf-regnetb1, HRNet18,
* timm EMA

### 5位 <b>SETIの壁</b> チーム（[@kzkt0713](https://www.kaggle.com/kzkt0713)さん, [@sinpcw](https://www.kaggle.com/sinpcw)さん, [@sunakuzira](https://www.kaggle.com/sunakuzira)さん）

[https://www.kaggle.com/c/seti-breakthrough-listen/discussion/266394]

* モデル: eca_nfnet_l2 (4fold) + efficientnet_v2_m (4fold)
* SHOT (https://github.com/tim-learn/SHOT)
* pseudo labeling 

上位陣の手法を身に着けて精進していきたいです。
CPMPさんとか僕がのほほんとサンタコンペ出た5年前からずっと存在感があってすごい。
