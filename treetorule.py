#!/usr/bin/python
# -*- coding:utf-8 -*-

"""

@author:zlh
@file: rulejk.py
@time: 2019/10/25 10:57
"""

from sklearn.tree import _tree

class treetorule:
    '''
        defname 生成的函数名
        defstr 记录函数
    '''
    defname='treerule'
    def __init__(self,tree_trained,feature_names):
        '''

        :param tree_trained: 训练好的规则树
        :param feature_names: 特征名list
        '''
        self.tree = tree_trained
        self.fes =feature_names
        self.defstr=[]

    def torule(self):
        '''

        :return: 递归出self.defstr
        '''
        tree_ = self.tree.tree_
        feature_name = [
            self.fes[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        self.defstr.append("def {}({}):".format(self.defname, 'x'))
        self.defstr.append('\n')
        def recurse(node, depth):
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                self.defstr.append("{}if x.{} <= {}:".format(indent, name, threshold))
                self.defstr.append('\n')
                recurse(tree_.children_left[node], depth + 1)
                self.defstr.append("{}else:  # if x.{} > {}".format(indent, name, threshold))
                self.defstr.append('\n')
                recurse(tree_.children_right[node], depth + 1)
            else:
                self.defstr.append("{}return {}".format(indent, tree_.value[node][0][0]))
                self.defstr.append('\n')

        recurse(0, 1)



if __name__=="__main__":
    cs = treetorule(5, 5)
    print(cs)