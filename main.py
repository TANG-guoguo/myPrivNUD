import numpy as np
import math
from treelib import Tree, Node
from numpy import random
from freqoracle import optRR
import NUDTOOL
import re




class Nodex(object):
    def __init__(self, AvailableUser_list, Interval, UserForItself_list=np.array([]), granularity=0, Frequency=0, isleaf=0):
        self.AvailableUser_list = AvailableUser_list
        self.AvailableUser_num = len(AvailableUser_list)
        self.Interval = Interval
        self.Interval_len = Interval[1]-Interval[0]+1
        self.UserForItself_list = UserForItself_list
        self.UserForItself_num = len(UserForItself_list)
        self.granularity = granularity
        self.Frequency = Frequency
        self.isleaf = isleaf



def TreeConstruction(domainsize, User_list, epsilon):
    #Construct root node
    NUD_Tree = Tree()
    NUD_Tree.create_node('Root','Root',data=Nodex(User_list, np.array([0, domainsize-1]), np.array([]), 2, 1, 0))

    unvisited_list = []
    unvisited_list.append(NUD_Tree['Root'])
    while(len(unvisited_list) != 0):   #若有未访问非叶结点
        current_node = unvisited_list.pop(0)
        if current_node.tag == 'Root':    #根节点二分
            tmpdomain = current_node.data.Interval
            g = current_node.data.granularity
            cutlist = NUDTOOL.domain_cut(g, tmpdomain)  #返回按g划分当前节点的子节点的域列表#完成
            for i in range(0, g):   #构建并初始化子节点
                tmptag = 'L-1'+'N-'+str(i+1)
                NUD_Tree.create_node(tmptag, tmptag, parent='Root', data=Nodex(User_list, cutlist[i]))
                unvisited_list.append(NUD_Tree[tmptag])

        else:    #访问非根节点
            tmpdomain = current_node.data.Interval
            g = NUDTOOL.best_granularity_calculation(NUD_Tree, current_node, domainsize, epsilon)  #返回最优g#完成
            current_node.data.granularity = g
            au_num = current_node.data.AvailableUser_num
            domain_len = current_node.data.Interval_len
            UserForItself_num = au_num//(math.log(domain_len, g)+1)
            UserForItself_list, AvailableUser_list_update = NUDTOOL.random_sample(UserForItself_num)  #随机抽取UserForItself_num个用户用于本结点估计，返回[抽取的用户数据,剔除后的AUlist]##########################未完成
            current_node.data.UserForItself_list = UserForItself_list
            current_node.data.UserForItself_num = UserForItself_num
            # derive the estimated frequency
            f = NUDTOOL.freqestimate()  #返回频率估计结果#############################################################未完成
            current_node.data.Frequency = f
            if NUDTOOL.isdecomposable()==1: #判断是否可以分解，可以返回1，不可分解返回0###################################未完成
                cutlist = NUDTOOL.domain_cut(g, tmpdomain)  # 返回按g划分当前节点的子节点的域列表##############################未完成
                for i in range(0,g):    #构建并初始化子节点
                    level = int(re.search(r"\d+",current_node.tag).group())+1
                    tmptag = 'L-'+str(level)+ 'N-' + str(i + 1)
                    NUD_Tree.create_node(tmptag, tmptag, parent=current_node.tag, data=Nodex(AvailableUser_list_update, cutlist[i]))
                    unvisited_list.append(NUD_Tree[tmptag])
            else:  #不可分解
                current_node.data.isleaf=1  #设置当前节点为叶结点
                f_update = NUDTOOL.freqestimate()  # 返回频率估计结果#############################################################未完成
                current_node.data.Frequency = f_update*k + f*(1-k)








if __name__ == '__main__':
    pass


























