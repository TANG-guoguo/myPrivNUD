import math


def domain_cut(g,domain):
    '''将domain[a,f]均分为g个子域，返回子域[[a,b],[c,d],[e,f]]列表cutlist'''
    domainsize = domain[1]-domain[0]+1
    subdomainsize = domainsize/g
    assert subdomainsize % 1 == 0    #子域长为整数
    cutlist = []
    for i in range(0, g):
        cut = [domain[0] + i*int(subdomainsize), domain[0] + (i+1)*int(subdomainsize) - 1]
        cutlist.append(cut)
    print(cutlist)
    return cutlist


def calculate_glist(D):
    '''返回D的所有因子的有序列表glist'''
    assert D>=0
    if D==1:
        return [1]
    glist=[]
    for factor in range(1,int(math.sqrt(D))+1):
        if D % factor ==0:
            glist.append(factor)
            if factor != int(D/factor):
                glist.append(int(D/factor))
    glist.sort()
    glist.remove(1)
    return glist


def fun_omega(o, D, p_o):
    '''返回子域o对应的omega的值'''
    pass

def best_granularity_calculation(NUD_Tree, current_node, domainsize, epsilon):
    '''根据v的结点和v的父结点挑选v的最优划分粒度g'''
    v_domainsize = current_node.data.Interval_len
    v_domain = current_node.data.Interval
    p_v_domain = NUD_Tree.parent(current_node.tag).data.Interval   #注：parent返回结点对象

    #得出所有可能的g
    glist = calculate_glist(v_domainsize)
    errorlist=[]
    for g in glist:
        N_g = domain_cut(g, v_domain)   #N_g为按照粒度g分解后的子域构成的集合
        #N_g.append(v_domain)
        sum=0
        for o in N_g:
            p_o = v_domain
            sum += fun_omega(o, domainsize, p_o) * fun_E(o,g,epsilon)
        o = v_domain    #v自身的域
        p_o = p_v_domain    #v父结点的域
        sum += fun_omega(o, domainsize, p_o) * fun_E(o,g,epsilon)




    pass



if __name__ == '__main__':
    pass