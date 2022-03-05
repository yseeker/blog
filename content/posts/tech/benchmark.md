---
#author: "Hugo Authors"
title: "Ryzen Threadripper 3970XとNVIDIA RTX 3090を使ってnumpy(Intel MKL and OpenBLAS)とcupyでベンチマーク"
date: "2022-03-05"
#description: "Sample article showcasing basic Markdown syntax and formatting for HTML elements."
tags:
  [
    "numpy",
    "cupy",
    "cuda",
    "Ryzen Threadripper 3970X",
    "NVIDIA RTX 3090",
    "ベンチマーク",
  ]
categories: ["技術", "ベンチマーク"]
ShowToc: true
TocOpen: true
draft: false
---

## numpy でベンチマーク

```python
# ファイル名: numpy_benchmark.py

import os
os.environ["OPENBLAS_NUM_THREADS"] = "32"
# import mkl
# mkl.set_num_threads(32)
import numpy as np
import time

from threadpoolctl import threadpool_info
from pprint import pp

pp(threadpool_info())
np.show_config()

N_LOOP = 5
calc_eigh_time_list = []
calc_inv_time_list = []
calc_dot_time_list = []
calc_norm_time_list = []

for size in [5000, 10000, 20000]:
    print(f"size : {size}")
    for i in range(3):
        np.random.seed(i)
        X = np.random.randn(size, size)
        t_start = time.time()
        np.linalg.eigh(X @ X.T)
        calc_eigh_time_list.append(time.time() - t_start)

        t_start = time.time()
        np.linalg.inv(X)
        calc_inv_time_list.append(time.time() - t_start)

        t_start = time.time()
        np.dot(X,X)
        calc_dot_time_list.append(time.time() - t_start)

        t_start = time.time()
        np.linalg.norm(X @ X)
        calc_norm_time_list.append(time.time() - t_start)

    calc_eigh_time_ndarr = np.array(calc_eigh_time_list)
    calc_inv_time_ndarr = np.array(calc_inv_time_list)
    calc_dot_time_ndarr = np.array(calc_dot_time_list)
    calc_norm_time_ndarr = np.array(calc_norm_time_list)

    print(f"np.linalg.eigh : {np.average(calc_eigh_time_ndarr):.4f} s")
    print(f"np.linalg.inv : {np.average(calc_inv_time_ndarr):.4f} s")
    print(f"np.dot : {np.average(calc_dot_time_ndarr):.4f} s")
    print(f"np.linalg.norm : {np.average(calc_norm_time_ndarr):.4f} s")
```

### Intel MKL の場合（スレッド数：32）

```bash
docker run --init --rm --shm-size 8g -v $PWD:/work -w /work  continuumio/anaconda3 python numpy_benchmark.py
```

```bash
[{'filepath': '/opt/conda/lib/libmkl_rt.so.1',
  'prefix': 'libmkl_rt',
  'user_api': 'blas',
  'internal_api': 'mkl',
  'version': '2021.4-Product',
  'num_threads': 32,
  'threading_layer': 'intel'},
 {'filepath': '/opt/conda/lib/libiomp5.so',
  'prefix': 'libiomp',
  'user_api': 'openmp',
  'internal_api': 'openmp',
  'version': None,
  'num_threads': 64}]

blas_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/opt/conda/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/opt/conda/include']
blas_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/opt/conda/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/opt/conda/include']
lapack_mkl_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/opt/conda/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/opt/conda/include']
lapack_opt_info:
    libraries = ['mkl_rt', 'pthread']
    library_dirs = ['/opt/conda/lib']
    define_macros = [('SCIPY_MKL_H', None), ('HAVE_CBLAS', None)]
    include_dirs = ['/opt/conda/include']

size : 5000
np.linalg.eigh : 4.2719 s
np.linalg.inv : 0.6087 s
np.dot : 0.4056 s
np.linalg.norm : 0.3880 s
size : 10000
np.linalg.eigh : 14.3513 s
np.linalg.inv : 2.1228 s
np.dot : 1.6021 s
np.linalg.norm : 1.5480 s
size : 20000
np.linalg.eigh : 61.9019 s
np.linalg.inv : 10.3558 s
np.dot : 7.9529 s
np.linalg.norm : 7.7727 s
```

### OpenBLAS の場合（スレッド数：32）

普段良く使うベースイメージを元にしたコンテナでテスト

```bash
docker run --init --rm --shm-size 8g -v $PWD:/work -w /work  nvcr.io/nvidia/pytorch:21.11-py3 python numpy_benchmark.py
```

```bash
[{'user_api': 'blas',
  'internal_api': 'openblas',
  'prefix': 'libopenblas',
  'filepath': '/opt/conda/lib/libopenblasp-r0.3.18.so',
  'version': '0.3.18',
  'threading_layer': 'pthreads',
  'architecture': 'Zen',
  'num_threads': 32}]

blas_info:
    libraries = ['cblas', 'blas', 'cblas', 'blas']
    library_dirs = ['/opt/conda/lib']
    include_dirs = ['/opt/conda/include']
    language = c
    define_macros = [('HAVE_CBLAS', None)]
blas_opt_info:
    define_macros = [('NO_ATLAS_INFO', 1), ('HAVE_CBLAS', None)]
    libraries = ['cblas', 'blas', 'cblas', 'blas']
    library_dirs = ['/opt/conda/lib']
    include_dirs = ['/opt/conda/include']
    language = c
lapack_info:
    libraries = ['lapack', 'blas', 'lapack', 'blas']
    library_dirs = ['/opt/conda/lib']
    language = f77
lapack_opt_info:
    libraries = ['lapack', 'blas', 'lapack', 'blas', 'cblas', 'blas', 'cblas', 'blas']
    library_dirs = ['/opt/conda/lib']
    language = c
    define_macros = [('NO_ATLAS_INFO', 1), ('HAVE_CBLAS', None)]
    include_dirs = ['/opt/conda/include']
Supported SIMD extensions in this NumPy install:
    baseline = SSE,SSE2,SSE3
    found = SSSE3,SSE41,POPCNT,SSE42,AVX,F16C,FMA3,AVX2
    not found = AVX512F,AVX512CD,AVX512_KNL,AVX512_KNM,AVX512_SKX,AVX512_CLX,AVX512_CNL,AVX512_ICL

size : 5000
np.linalg.eigh : 4.6165 s
np.linalg.inv : 0.8397 s
np.dot : 0.3431 s
np.linalg.norm : 0.3570 s
size : 10000
np.linalg.eigh : 26.7373 s
np.linalg.inv : 2.5276 s
np.dot : 1.1968 s
np.linalg.norm : 1.2321 s
size : 20000
np.linalg.eigh : 138.9376 s
np.linalg.inv : 10.5088 s
np.dot : 6.3217 s
np.linalg.norm : 6.0329 s
```

## cupy でベンチマーク

```python
import os
#os.environ["MKL_NUM_THREADS"] = 64
#os.environ["OPENBLAS_NUM_THREADS"] = "64"
# import mkl
# mkl.set_num_threads(32)
import numpy as np
import cupy as cp
import time

from threadpoolctl import threadpool_info
from pprint import pp

# pp(threadpool_info())
# np.show_config()

N_LOOP = 5
calc_eigh_time_list = []
calc_inv_time_list = []
calc_dot_time_list = []
calc_norm_time_list = []

for size in [5000, 10000, 20000]:
    print(f"size : {size}")
    for i in range(3):
        cp.random.seed(i)
        X = cp.random.randn(size, size)
        cp.cuda.Stream.null.synchronize()
        t_start = time.time()
        cp.linalg.eigh(X @ X.T)
        cp.cuda.Stream.null.synchronize()
        calc_eigh_time_list.append(time.time() - t_start)

        t_start = time.time()
        cp.linalg.inv(X)
        cp.cuda.Stream.null.synchronize()
        calc_inv_time_list.append(time.time() - t_start)

        t_start = time.time()
        cp.dot(X,X)
        cp.cuda.Stream.null.synchronize()
        calc_dot_time_list.append(time.time() - t_start)

        t_start = time.time()
        cp.linalg.norm(X @ X)
        cp.cuda.Stream.null.synchronize()
        calc_norm_time_list.append(time.time() - t_start)

    calc_eigh_time_ndarr = cp.array(calc_eigh_time_list)
    calc_inv_time_ndarr = cp.array(calc_inv_time_list)
    calc_dot_time_ndarr = cp.array(calc_dot_time_list)
    calc_norm_time_ndarr = cp.array(calc_norm_time_list)

    print(f"cp.linalg.eigh : {cp.average(calc_eigh_time_ndarr):.4f} s")
    print(f"cp.linalg.inv : {cp.average(calc_inv_time_ndarr):.4f} s")
    print(f"cp.dot : {cp.average(calc_dot_time_ndarr):.4f} s")
    print(f"cp.linalg.norm : {cp.average(calc_norm_time_ndarr):.4f} s")
```

```bash
docker run --init --rm --shm-size 8g --gpus all -v $PWD:/work -w /work  nvcr.io/nvidia/pytorch:21.11-py3 python cupy_benchmark.py
```

```bash
size : 5000
cp.linalg.eigh : 2.1541 s
cp.linalg.inv : 0.8055 s
cp.dot : 0.4646 s
cp.linalg.norm : 0.5734 s
size : 10000
cp.linalg.eigh : 7.4867 s
cp.linalg.inv : 2.9686 s
cp.dot : 2.0489 s
cp.linalg.norm : 2.1329 s
size : 20000
cp.linalg.eigh : 37.9862 s
cp.linalg.inv : 15.2210 s
cp.dot : 11.0195 s
cp.linalg.norm : 11.1704 s
```

## 結果（size = 20000 の場合）

|     TH      | numpy (Intel MKL) | numpy (OpenBLAS) |    cupy     |
| :---------: | :---------------: | :--------------: | :---------: |
|     dot     |    7.9529 sec     |    6.3217 sec    | 11.0195 sec |
| linalg.inv  |    10.3558 sec    |   10.5088 sec    | 15.2210 sec |
| linalg.norm |    7.7727 sec     |    6.0329 sec    | 11.1704 sec |
| linalg.eigh |    61.9019 sec    |   138.9376 sec   | 37.9862 sec |

この４つの評価項目だと linalig.eigh （固有値計算） 以外は numpy (OpenBLAS)で良くて、固有値 は cupy で計算すれば良さそう。行列のサイズがもっと大きくなれば結果が変わるかもしれない。<br>
（一概に CPU と GPU の比較といっても CPU 側ではスレッド数と BLAS でだいぶ結果が変わるので単純に比較はできなさそう。）

**雑な結論**：サイズが 20000 までの行列なら Ryzen Threadripper 3970X ＆ numpy でだいたい OK。<br>
（ま、とは言っても普段行列計算しないんですけどね。）
