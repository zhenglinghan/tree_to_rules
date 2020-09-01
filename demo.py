#!/usr/bin/env python 
# encoding: utf-8 

"""
@version: v1.0
@author: zhenglinghan
@contact: 422807471@qq.com
@software: PyCharm
@file: demo.py
@time: 2020/9/1 22:30
"""

import pandas as pd
import warnings

warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('precision', 5)
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('max_colwidth', 200)
pd.set_option('display.width', 5000)

from sklearn import datasets
from sklearn import tree
import treetorule


if __name__ == "__main__":
    # sim data
    data, target = datasets.make_classification(n_samples=1000, n_features=5, n_classes=2,
                                                n_informative=2, n_redundant=0, n_repeated=0)
    dataSim = pd.DataFrame(data)
    dataSim.columns = [f'f_{i}' for i in range(5)]
    dataSim['label'] = target

    # train the model
    dtree = tree.DecisionTreeRegressor(max_depth=3, min_samples_leaf=40, min_samples_split=60, random_state=2020)
    dtree = dtree.fit(dataSim.iloc[:, :-1], dataSim['label'])

    # tree model to rule
    cs = treetorule.treetorule(dtree, list(dataSim.columns)[:-1])
    cs.torule()
    defstr = ''.join(cs.defstr)
    exec(defstr)
    print(defstr)
    # checkrule
    dataSim['mz'] = dataSim.apply(lambda x: treerule(x), axis=1)
    print(dataSim['mz'].value_counts())

    # check rule max lift
    badRateBase = dataSim['label'].mean()
    maxLift = dataSim['mz'].max() / badRateBase
    print(f'maxLift: {maxLift}')
