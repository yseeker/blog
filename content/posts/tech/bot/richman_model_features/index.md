---
#author: "Hugo Authors"
title: "richmanbtcさんのチュートリアルで特徴量を解析してみる"
date: "2022-02-01"
#description: "Sample article showcasing basic Markdown syntax and formatting for HTML elements."
tags: ["特徴量", "richmanbtc"]
categories: ["仮想通貨ボット"]
ShowToc: true
TocOpen: true
draft: true
---

richmanbtcさんの機械学習ボットのチュートリアルが面白そうだったので少し特徴量を解析してみました。ただ、機械学習で重要なのはrichmanbtcさん自身が[FAQ](https://note.com/btcml/n/ne5f730bb7c64)で「執行の改善と特徴量の改善、どちらが寄与が大きい？」という問いに対して「執行の改善」と答えていたり、界隈で有名な方が
[「予測より執行」について](https://bittokoinn.tokyo/posts/prediction_and_execution/)
[予測力と執行戦略について](https://note.com/hht/n/nb7fcfe538c59)
という記事を出している通り、特徴量エンジニアリングするより強い執行を導入する方が重要なのかなと思ってます。（何が強い執行かは戦略とか時間足によって変わると思う。）

とはいってもやはり特徴量がボットの改善にほんの少しは影響すると思うので、最近読んだ「機械学習を解釈する技術」で出てきた手法を使って、チュートリアルのデフォルトの設定で特徴量を解析してみます。

```python
# richmanbtcさんのコードから抜粋

# あとで各foldごとのモデルからfeature importanceなどを求めるためにmodel_buy_listとmodel_sell_listを定義

    model_buy_list = []
    model_sell_list = []

    def my_cross_val_predict(estimator, estimator_list, X, y=None, cv=None):
        y_pred = y.copy()
        y_pred[:] = np.nan
        for train_idx, val_idx in cv:
            estimator.fit(X[train_idx], y[train_idx])
            y_pred[val_idx] = estimator.predict(X[val_idx])
            estimator_list.append(copy.copy(estimator))
        return y_pred

    df["y_pred_buy"] = my_cross_val_predict(
        model_buy,
        model_buy_list,
        df[features].values,
        df["y_buy"].values,
        cv=cv_indicies,
    )
    df["y_pred_sell"] = my_cross_val_predict(
        model_sell,
        model_sell_list,
        df[features].values,
        df["y_sell"].values,
        cv=cv_indicies,
    )
```

## Feature Imporance

- split
- gain

```python
def visualize_importance(models, features):
    feature_importance_df = pd.DataFrame()
    for i, model in enumerate(models):
        _df = pd.DataFrame()
        _df["feature importance"] = model.feature_importances_
        _df["features"] = features
        _df["fold"] = i + 1
        feature_importance_df = pd.concat(
            [feature_importance_df, _df], axis=0, ignore_index=True
        )

    order = (
        feature_importance_df.groupby("features")
        .sum()[["feature importance"]]
        .sort_values("feature importance", ascending=False)
        .index[:50]
    )

    fig, ax = plt.subplots(figsize=(8, max(6, len(order) * 0.4)))
    plt.rcParams["font.size"] = 14
    sns.boxplot(
        data=feature_importance_df,
        y="features",
        x="feature importance",
        order=order,
        ax=ax,
        palette="viridis_r",
    )
    ax.tick_params(axis="x", rotation=90)
    fig.tight_layout()
    return fig, ax
```
<p>
<img src="images/feature_importance_buy.png" width=49% >
<img src="images/feature_importance_sell.png" width=49% >
</p>

## Permutation Feature Importance
```python
def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


def get_permutation_importance(df, model, features, target):
    mse_scorer = make_scorer(rmse)
    result = permutation_importance(
        model,
        df[features].values,
        df[target].values,
        scoring=mse_scorer,
        n_repeats=5,
        n_jobs=-1,
        random_state=71,
    )
    return result["importances_mean"]
```
<p>
<img src="images/permutation_feature_importance_buy.png" width=49% >
<img src="images/permutation_feature_importance_sell.png" width=49% >
</p>

## Partial Dependence

## Independent なんとか

## Shapley value (shap 値)
```python

```
![](images/2022-02-01-21-45-08.png#center)
