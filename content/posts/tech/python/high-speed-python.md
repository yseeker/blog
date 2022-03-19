---
#author: "Hugo Authors"
title: "Python実装での個人的に意識していること"
date: "2021-08-19"
tags: ["Kaggle", "SETI"]
categories: ["Kaggle"]
ShowToc: true
TocOpen: true
draft: true
---

## 高速化

## ドットを使わない

- モジュール名まで含めてインストールしておき、内部処理でドットで関数を呼び出さない。

## for ループ時の処理

- 配列にアクセスしない。
- enumerate を使う。

## Global Interpreter Lock (GIL)

スレッドセーフを確保するために、複数スレッドで並列処理ができない。

## if 文の条件の順番

- if の条件のが厳しいものを最初に置く

## 計算の高速化

- cython
- numba.jit, numba.cuda.jit

## 変数名

https://qiita.com/sotasato/items/cc36a532ba6487dd3dba#1-1-python%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%97%E3%83%88%E3%81%AE%E6%9B%B8%E3%81%8D%E6%96%B9%E3%82%92%E8%A6%8B%E7%9B%B4%E3%81%99
https://cafeunder.github.io/rosenblock-chainers-blog/2018/04/24/Python-Tips.html
https://qiita.com/shaka/items/f180ae4dc945dc7b9066#21-%E5%8F%82%E7%85%A7%E3%81%AE%E4%BB%95%E6%96%B9%E3%81%AB%E6%B3%A8%E6%84%8F
https://nonbiri-tereka.hatenablog.com/entry/2016/09/01/072402#%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E7%94%9F%E6%88%90
