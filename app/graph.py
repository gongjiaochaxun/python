from app.models import *

class Graph_Matrix:
    """
    Adjacency Matrix
    """
    def __init__(self, vertices=[], matrix=[]):
        """

        :param vertices:a dict with vertex id and index of matrix , such as {vertex:index}
        :param matrix: a matrix
        """
        self.matrix = matrix
        self.edges_dict = {}  # {(tail, head):weight}
        self.edges_array = []  # (tail, head, weight)
        self.vertices = vertices
        self.num_edges = 0

        # if provide adjacency matrix then create the edges list
        if len(matrix) > 0:
            if len(vertices) != len(matrix):
                raise IndexError
            self.edges = self.getAllEdges()
            self.num_edges = len(self.edges)

        # if do not provide a adjacency matrix, but provide the vertices list, build a matrix with 0
        elif len(vertices) > 0:
            self.matrix = [[0 for col in range(len(vertices))] for row in range(len(vertices))]

        self.num_vertices = len(self.matrix)

    def getAllEdges(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if 0 < self.matrix[i][j] < float('inf'):
                    self.edges_dict[self.vertices[i], self.vertices[j]] = self.matrix[i][j]
                    self.edges_array.append([self.vertices[i], self.vertices[j], self.matrix[i][j]])
                   # print(self.edges_array)
        return self.edges_array
def create_undirected_matrix(my_graph,list):
    M = 1E100
    set1=set()
    node1=set()
    for i in range(len(list)):
        set1=set(list[i])
        node1=node1.union(set1)
    node = [i for i in node1]
    l = len(node)
    d = {}
    for i in range(l):
        d.update({node[i]: i})
    matrix = [([M]) * l for i in range(l)]
    for i in range(l):
        matrix[i][i]=0
    for i in range(len(list)):
        for j in range(len(list[i])-1):
            i1=d[list[i][j]]
            i2=d[list[i][j+1]]
            if i1!=i2:
                matrix[i1][i2] = matrix[i2][i1]=1
    my_graph = Graph_Matrix(node, matrix)
    #getPath(my_graph,0)
    return matrix,d

def dijkstra(matrix, map, source):
    source=map[source]
    M = 1E100
    n = len(matrix)
    m = len(matrix[0])
    if source >= n or n != m:
        print('Error!')
        return
    found = [source]        # 已找到最短路径的节点
    cost = [M] * n          # source到已找到最短路径的节点的最短距离
    cost[source] = 0
    path = [[]] * n          # source到其他节点的最短路径
    path[source] = [source]
    while len(found) < n:   # 当已找到最短路径的节点小于n时
        min_value = M+1
        col = -1
        row = -1
        for f in found:     # 以已找到最短路径的节点所在行为搜索对象
            for i in [x for x in range(n) if x not in found]:   # 只搜索没找出最短路径的列
                if matrix[f][i] + cost[f] < min_value:  # 找出最小值
                    min_value = matrix[f][i] + cost[f]  # 在某行找到最小值要加上source到该行的最短路径
                    row = f         # 记录所在行列
                    col = i
        if col == -1 or row == -1:  # 若没找出最小值且节点还未找完，说明图中存在不连通的节点
            break
        found.append(col)           # 在found中添加已找到的节点
        cost[col] = min_value       # source到该节点的最短距离即为min_value
        path[col] = path[row][:]    # 复制source到已找到节点的上一节点的路径
        path[col].append(col)       # 再其后添加已找到节点即为sorcer到该节点的最短路径



    return found, cost, path

def Change(map,path):
    new_d = {v: k for k,v in map.items()}

    for p in range(len(path)):
        for i in range(len(path[p])):
            path[p][i] = new_d[path[p][i]]
    return path
def Sort(path):
    for i in range(len(path)-1):
        for j in range(len(path)-i-1):
            j1=j
            j2=j+1
            if len(path[j1]) > len(path[j2]):
                tem=path[j1]
                path[j1]=path[j2]
                path[j2]=tem
    return path

def Search(s,t):
    my_graph=Graph_Matrix()
    lists = [[_.placename for _ in r.places] for r in Route.objects()]
    create_graph,map=create_undirected_matrix(my_graph,lists)
    found,cost,path = dijkstra(create_graph,map,s)
    del my_graph
    del found
    del cost
    path=Change(map,Sort(path))
    tl = [_[len(_)-1] for _ in path if len(_)>1]
    if t in tl:
        for _ in path:
            if _[len(_)-1]==t:
                pl = [Place.objects(placename=x).first() for x in _]
                ret = []
                tmpret = pl[0]
                tem = set(pl[0].routes)
                for i in range(0,len(pl)-1):
                    ttem = tem&set(pl[i+1].routes)
                    if len(ttem)==0:
                        ret.append({"s":tmpret.placename,"t":pl[i].placename,"r":[xx.routename for xx in tem]})
                        tmpret = pl[i]
                        ttem = set(pl[i].routes) & set(pl[i+1].routes)
                    tem = ttem
                ret.append({"s": tmpret.placename, "t": pl[len(pl)-1].placename, "r": [xx.routename for xx in tem]})
                return ret
    else:
        return None




if  __name__=='__main__':
    my_graph=Graph_Matrix()
    list1 = ["地点1","地点2","地点3","地点5","地点7"]
    list2 = ["地点3","地点4","地点6","地点8"]
    list3 = ["地点2","地点5","地点7","地点9"]
    list4 = ["地点3","地点6","地点8","地点9"]
    list=[list1,list2,list3,list4]
    create_graph,map=create_undirected_matrix(my_graph,list)
    found,cost,path = dijkstra(create_graph,map,"地点2")
    print('found:')
    print(found)
    print('cost:')
    print(cost)
    print('path:')
    print(path)

    path=Sort(path)
    print(Change(map,path))











