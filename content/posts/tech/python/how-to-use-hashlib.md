---
#author: "Hugo Authors"
title: "Python : hashlibを使って、ハッシュ値を求める"
date: "2022-03-20"
tags: ["python", "ハッシュ", "hashlib", "md5", "sha224"]
categories: ["Tech", "Python"]
ShowToc: true
TocOpen: true
draft: false
---

## [ハッシュ値を求める](https://docs.python.org/ja/3/library/hashlib.html)

<div style="border-radius: 10px; background: beige; padding: 10px;">
  Rounded
</div>

<fieldset><legend>Box Info</legend><ul><li>Name: <a href=https://app.hackthebox.eu/machines/Horizontall><code>Horizontall</code></a></li><li>OS: <code>Linux</code></li><li>Difficulty: <code>Easy</code></li><li>IP: <code>10.10.11.105</code></li><li>Points: <code>20</code></li><li>Machine Creator: <a href=https://app.hackthebox.eu/users/4005><code>wail99</code></a></li></ul></fieldset>

```python
import hashlib

file_name = "important_file.dat"

# MD5 ハッシュを生成する
hs = hashlib.md5(file_name.encode()).hexdigest()
# SHA224 ハッシュを生成する
hs = hashlib.sha224(file_name.encode()).hexdigest()
```

[自走プログラマー~Python の先輩が教えるプロジェクト開発のベストプラクティス 120](https://amzn.to/3iA52lL)の中でファイル名からハッシュ値を求め、そのハッシュ値の頭 3 文字を中間ディレクトリにして、１つのディレクトリにファイルを集中させないという手法が紹介されていた。

### 例

```python
file_name = "important_file.dat"
hs = hashlib.md5(file_name.encode()).hexdigest()
file_path = f"dir_name/{hs[:3]}/{file_name}"
```

## 参考

<iframe class="hatenablogcard" style="width:100%;height:155px;margin:15px 0;max-width:560px;" title="hashlib --- セキュアハッシュおよびメッセージダイジェスト" src="https://hatenablog-parts.com/embed?url=https://docs.python.org/ja/3/library/hashlib.html" frameborder="0" scrolling="no"></iframe>
