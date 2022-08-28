---
#author: "Hugo Authors"
title: "Hugo : PaperModのテーマでjavascriptを非同期で読み込んで高速化"
date: "2022-03-03"
tags: ["Hugo", "PaperMod", "prism.js", "javascript", "defer"]
categories: ["Tech", "Hugo"]
ShowToc: true
TocOpen: true
draft: true
---

この web サイトは [PaperMod](https://adityatelange.github.io/hugo-PaperMod/) というテンプレートから作成しているのが、シンタックスハイライトをいい感じにする Prism.js を導入したら[PageSpeed Insights](https://pagespeed.web.dev/)のパフォーマンスが悪くなったので改善メモ。

## Javascript の読み込み時に defer を導入

### Before

モバイルでのパフォーマンスは、**40-50** くらいだった。

```html
<script src="{{ .Site.BaseURL }}/js/prism.js"></script>
```

### After

モバイルでのパフォーマンスが、**65-75** くらいに改善した。

```html
<script
  type="text/javascript"
  defer
  src="{{ .Site.BaseURL }}/js/prism.js"
></script>
```

## 余談

ちなみに PaperMod はデフォルトでパフォーマンスが**90-99**くらい出る超高速なテンプレートである。（Prism.js の読み込みで大幅に速度が低下した。）

上の javascript の読み込み部分をコメントアウトするとパフォーマンスは 90 以上まで戻る（笑）

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="JavaScriptの読み込み方を工夫することで、表示を高速化しよう！" src="https://hatenablog-parts.com/embed?url=https://digitalidentity.co.jp/blog/engineerblog/web-performance/how-to-read-javascript.html" frameborder="0" scrolling="no"></iframe>
