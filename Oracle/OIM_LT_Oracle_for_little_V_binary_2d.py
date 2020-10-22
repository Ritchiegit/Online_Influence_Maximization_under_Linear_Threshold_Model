import numpy as np
import copy

# tangency_point。
def calculate_tangency_point(V, c, x0, y0, type="-1"):
    # V is the parameter of ellipse，c = \rho^2
    # x0 y0 is the center of ellipse
    v1 = V[0][0]
    v2 = V[0][1]
    v3 = V[1][0]
    v4 = V[1][1]
    if type == "inf":
        # m maximium
        pass
        n_divide_m = -(v2+v3)/(2*v4)
        m = np.sqrt(c/(v1 + (v2 + v3) * n_divide_m + v4 * n_divide_m* n_divide_m))
        n = n_divide_m * m
        if m < 0:
            m = -m
            n = -n
    elif type =="-1":
        m_divide_n = -(v2 + v3 - 2 * v4) / (2 * v1 - (v2 + v3) )
        n = np.sqrt(c / (v1 * m_divide_n * m_divide_n + (v2 + v3) * m_divide_n + v4))
        m = m_divide_n * n
        if m + n < 0:
            m = -m
            n = -n
    elif type == "0":
        # n maximium
        m_divide_n = -(v2+v3)/(2*v1)
        n = np.sqrt(c/ (v1*m_divide_n*m_divide_n + (v2+v3)*m_divide_n + v4))
        m = m_divide_n * n
        if n < 0:
            m = -m
            n = -n
    else:
        m = 0
        n = 0
    x = m + x0
    y = n + y0
    return x, y

# intersection_point_with x+y = 1
def calculate_intersection_point_with_x_plus_y_equal_1(V, c, x0, y0):
    v1 = V[0][0]
    v2 = V[0][1]
    v3 = V[1][0]
    v4 = V[1][1]

    Yu = 1 - x0 - y0
    m_left = -(v2+v3-2*v4) * Yu / (2*(v1-v2-v3+v4)) - np.sqrt(((v2+v3-2*v4)*Yu)**2 - 4*(v1-v2-v3+v4)*(v4*Yu**2 - c))/(2*(v1-v2-v3+v4))
    n_left = Yu-m_left

    m_right = -(v2+v3-2*v4) * Yu / (2*(v1-v2-v3+v4)) + np.sqrt(((v2+v3-2*v4)*Yu)**2 - 4*(v1-v2-v3+v4)*(v4*Yu**2 - c))/(2*(v1-v2-v3+v4))
    n_right = Yu-m_right

    x_left = x0 + m_left
    y_left = y0 + n_left
    x_right = x0 + m_right
    y_right = y0 + n_right
    return x_left, y_left, x_right, y_right

# intersection_point_with x axis
def calculate_intersection_point_with_X_axis(V, c, x0, y0):
    v1 = V[0][0]
    v2 = V[0][1]
    v3 = V[1][0]
    v4 = V[1][1]
    y = 0
    x = x0 + y0*(v2 + v3)/(2*v1) + np.sqrt(((v2+v3)*y0)**2 - 4 * v1 * (v4*y0**2 - c))/(2*v1)
    return x, y

# intersection_point_with y axis
def calculate_intersection_point_with_Y_axis(V, c, x0, y0):
    v1 = V[0][0]
    v2 = V[0][1]
    v3 = V[1][0]
    v4 = V[1][1]
    x = 0
    y = y0 + x0*(v2 + v3)/(2*v4) + np.sqrt( (x0*(v2+v3))**2 - 4* v4 * (-c + x0**2*v1))/(2*v4)
    return x, y

def calculate_spread_of_binary(G, VDir, cDir, S, average_weight_Dir, edge2IndexDir):
    spread = len(S)
    estimated_weight = copy.deepcopy(average_weight_Dir)
    for seed in S:
        assert seed in G.nodes(), 'seed is not in the graph'
    for node in G.nodes():
        if node in S:
            # If the node is seed node, there is no need to calculate the probability
            continue
        # edge of inedge of "node"
        edge_activated_of_this_inNode = []
        list_of_inedges = {}
        for edge in G.in_edges(node):
            list_of_inedges[edge2IndexDir[node][edge]] = edge
            if edge[0] in S:
                edge_activated_of_this_inNode.append(edge)  # corresponding to V
        # m average_weight_Dir[x] V[0] is x
        # n average_weight_Dir[y] V[1] is y

        if len(edge_activated_of_this_inNode) == 2:
            #  x+y = c
            x0 = average_weight_Dir[list_of_inedges[0]]
            y0 = average_weight_Dir[list_of_inedges[1]]
            x_tangency, y_tangency = calculate_tangency_point(VDir[node], cDir[node], x0, y0, type="-1")
            if x_tangency < 0 or y_tangency < 0:
                print("two activated in node, intersection_point does not appeared in first quartile")
            newx = x_tangency
            newy = y_tangency

            spread_add = newx + newy
            spread += spread_add
            estimated_weight[list_of_inedges[0]] = newx
            estimated_weight[list_of_inedges[1]] = newy

        elif len(edge_activated_of_this_inNode) == 1:
            edge_to_calculate = edge_activated_of_this_inNode[0]
            if G.in_degree(node) == 2:
                index_of_activated_edge = edge2IndexDir[node][edge_to_calculate]
                # x is maxmium dy/dx = inf
                if index_of_activated_edge == 0:
                    x0 = average_weight_Dir[list_of_inedges[0]]
                    y0 = average_weight_Dir[list_of_inedges[1]]
                    x_tangency, y_tangency = calculate_tangency_point(VDir[node], cDir[node], x0, y0, type="inf")
                    newx = x_tangency
                    newy = y_tangency
                    if y_tangency < 0:
                        x_intersection, y_intersection = calculate_intersection_point_with_X_axis(VDir[node], cDir[node], x0, y0)
                        newx = x_intersection
                        newy = y_intersection
                    spread_add = newx
                    spread += spread_add
                    estimated_weight[list_of_inedges[0]] = newx
                    estimated_weight[list_of_inedges[1]] = newy
                else:
                    # y is maxmium dy/dx = 0
                    x0 = average_weight_Dir[list_of_inedges[0]]
                    y0 = average_weight_Dir[list_of_inedges[1]]
                    x_tangency, y_tangency = calculate_tangency_point(VDir[node], cDir[node], x0, y0, type="0")
                    newx = x_tangency
                    newy = y_tangency
                    if x_tangency < 0:
                        x_intersection, y_intersection = calculate_intersection_point_with_Y_axis(VDir[node], cDir[node], x0, y0)
                        newx = x_intersection
                        newy = y_intersection
                    spread_add = newy
                    spread += spread_add
                    estimated_weight[list_of_inedges[0]] = newx
                    estimated_weight[list_of_inedges[1]] = newy
            else:
                # in degree is 2
                mOrn = np.sqrt(cDir[node] / VDir[node][0][0])
                if average_weight_Dir[edge_to_calculate] + mOrn > 1:
                    mOrn = 1 - average_weight_Dir[edge_to_calculate]
                estimated_weight[edge_to_calculate] = average_weight_Dir[edge_to_calculate] + mOrn
                spread_add = average_weight_Dir[edge_to_calculate] + mOrn
                spread += spread_add
        else:
            # activated in node is 0
            pass
    return spread, estimated_weight


def IMLinUCB_Oracle(VDir, bDir, cDir, K, G, edge2IndexDir):
    invVDir = {}
    invVbDir = {}
    average_weight_Dir = {}
    for v in G.nodes():
        invVDir[v] = np.linalg.inv(VDir[v])
        invVbDir[v] = invVDir[v].dot(bDir[v])
        for edge in G.in_edges(v):
            indexEdge = edge2IndexDir[v][edge]
            average_weight_Dir[(edge[0], edge[1])] = invVbDir[v][indexEdge][0]

    S = []
    best_spread = 0
    best_estimated_weight = []
    for No_of_seed in range(K):
        # S + x
        best_x = -2
        best_spread = 0
        # Add a seed which bring the biggest extension of spread
        for x in G.nodes():  #
            # view all node which is not seed
            if x not in S:
                S.append(x)
                # extension of spread
                spread_tmp, estimated_weight_tmp = calculate_spread_of_binary(G, VDir, cDir, S, average_weight_Dir, edge2IndexDir)
                if spread_tmp > best_spread:
                    best_x = x
                    best_estimated_weight = estimated_weight_tmp
                    best_spread = spread_tmp
                S.pop()
        S.append(best_x)

    best_estimated_weight_divide_Gweight = {}
    for edge in G.in_edges():
        best_estimated_weight_divide_Gweight[edge] = best_estimated_weight[edge]/G[edge[0]][edge[1]]['weight']

    return S, best_estimated_weight_divide_Gweight, best_spread
