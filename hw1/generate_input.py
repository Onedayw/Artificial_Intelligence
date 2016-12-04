# This is to generate random path map
import os
import random
import time


# Global level:
GEN = False
INPUT_DIR_NAME = 'random_inputs'


# batch level:
ALGO_BUCKET = ['DFS', 'BFS', 'UCS', 'A*']
INPUT_SIZE = 10

# file level
NUM_NODES = 500
AVG_DENSITY = 0.01
MANDATORY_PATH = True


MIN_STEPS_TO_GOAL = 100
MAX_STEPS_TO_GOAL = 200
MAX_PATH_COST = 50
MIN_PATH_COST = 25

MAX_HELPER_COST = 50
MIN_HELPER_COST = 25

GAUSS_SIGMA = 5

# use system time as seed
random.seed()


def gen_cost():
    return random.randint(MIN_PATH_COST, MAX_PATH_COST)


def gen_helper():
    return random.randint(MIN_HELPER_COST, MAX_HELPER_COST)


def gen_sample_content(algo='BFS'):

    # init with header algo
    content = algo

    # set up containers
    nodes = []  # nodes = [node, sunday_cost]
    paths = dict()  # paths = {node1: {node2: cost}}
    # generate all nodes
    steps_to_goal = min(random.randint(MIN_STEPS_TO_GOAL, MAX_STEPS_TO_GOAL), NUM_NODES)
    path_count = 0

    # generate the path from start to goal
    if MANDATORY_PATH:
        # adding start and goal
        start = 'start'
        goal = 'goal'
        nodes.append([start, gen_helper()])
        nodes.append([goal, 0])
        # adding the nodes on the path and the paths
        last_node = start
        for i in range(0, max(steps_to_goal - 2, 0)):
            node = 'P' + str(i+100)  # special P nodes on the path
            nodes.append([node, gen_helper()])
            paths[last_node] = {node: gen_cost()}
            path_count += 1
            last_node = node
        paths[last_node] = {goal: gen_cost()}
        path_count += 1

    # generate the rest nodes
    leftover_nodes = max(NUM_NODES - len(nodes), 0)
    for i in range(0, leftover_nodes):
        node = 'O' + str(i+100)  # ordinary nodes spread out there
        nodes.append([node, gen_helper()])

    # generate random paths
    for i in nodes:
        # figure out how many outgoing paths it needs
        node = i[0]
        num_path = min(max(int(random.gauss(AVG_DENSITY * NUM_NODES, GAUSS_SIGMA)), 0), NUM_NODES - 1)
        destinations = random.sample(nodes, num_path)
        for j in destinations:
            destination = j[0]
            # if path already exists or to itself
            if node in paths:
                if destination in paths[node] or destination == node:
                    continue
                paths[node][destination] = gen_cost()
            else:
                paths[node] = {destination: gen_cost()}
            path_count += 1

    # writing to content
    if MANDATORY_PATH:
        content += '\nstart\ngoal'
    else:
        [start, goal] = random.sample(nodes, 2)
        content += '\n' + start[0] + '\n' + goal[0]

    # paths
    content += '\n' + str(path_count)
    for k1 in paths:
        node1 = k1
        for k2 in paths[k1]:
            node2, cost = k2, paths[k1][k2]
            content += '\n' + node1 + ' ' + node2 + ' ' + str(cost)

    # nodes
    content += '\n' + str(len(nodes))
    for [node, cost] in nodes:
        content += '\n' + node + ' ' + str(cost)

    # done
    return content


def batch_inputs(num=INPUT_SIZE, flag=GEN):
    file_list = []
    for alg in ALGO_BUCKET:
        for i in range(0, num):
            content = gen_sample_content(alg)
            file_name = alg + str(i + 1000) + '.txt'
            file_name = file_name.replace("*", "_")
            if flag: 
                fin = open(INPUT_DIR_NAME + '/' + file_name, 'w')
                fin.write(content)  
            else:
                fin = open(INPUT_DIR_NAME + '/' + file_name, 'a')
            file_list.append(file_name)
            fin.close()
    return file_list, INPUT_DIR_NAME


def gen_main():
    # init random
    random.seed()
    # generate random input files in this dir
    start_time = time.time()
    if not os.path.exists(INPUT_DIR_NAME):
        os.makedirs(INPUT_DIR_NAME)
    batch_list, dir_name = batch_inputs(INPUT_SIZE)
    end_time = time.time()
    delta_time = (end_time - start_time) * 1000
    print(str(batch_list))
    print('Generate ' + str(len(batch_list)) + ' Input Files Batch finished in ' + str(delta_time) + 'ms')
    return batch_list, dir_name


if __name__ == '__main__':
    gen_main()






