import os
import time
import generate_input as inputs
import homework3 as runscript


OUTPUT_DIR_NAME = 'random_output'
CROSSFIRE = True
CROSSFILE_BUCKET = ['BFS', 'DFS', 'UCS', 'A*']


def run_file(input_file, output_file, des_algo=None):
    runscript.main_func(input_file, output_file, des_algo)


def gen_main():
    start_time = time.time()
    # gen input settings
    if CROSSFIRE:
        print('CROSSFIRE')
        inputs.ALGO_BUCKET = ['CROSSFIRE']
    # gen input files
    input_list, input_dir_name = inputs.gen_main()
    # do files
    if not os.path.exists(OUTPUT_DIR_NAME):
        os.makedirs(OUTPUT_DIR_NAME)
    if CROSSFIRE:
        runscript.CROSSFIRE = True
        for algo in CROSSFILE_BUCKET:
            for f in input_list:
                algoDirName = OUTPUT_DIR_NAME + '/' + algo
                algoDirName = algoDirName.replace('*', '_');
                if not os.path.exists(algoDirName):
                    os.makedirs(algoDirName)
                run_file(input_dir_name + '/' + f, algoDirName + '/' + f, algo)
        end_time = time.time()
        delta_time = (end_time - start_time) * 1000
        print('Generate ' + str(len(input_list) * len(CROSSFILE_BUCKET)) +
              ' Output Files Batch finished in ' + str(delta_time) + 'ms')
    else:
        for f in input_list:
            run_file(input_dir_name + '/' + f, OUTPUT_DIR_NAME + '/' + f)
        end_time = time.time()
        delta_time = (end_time - start_time) * 1000
        print('Generate ' + str(len(input_list)) + ' Output Files Batch finished in ' + str(delta_time) + 'ms')

if __name__ == '__main__':
    CROSSFIRE = True
    CROSSFILE_BUCKET = ['DFS', 'BFS', 'UCS', 'A*']
    inputs.GEN = False
    inputs.INPUT_SIZE = 100
    inputs.MAX_PATH_COST = 100
    inputs.MIN_PATH_COST = 10
    inputs.MAX_HELPER_COST = 1000
    inputs.MIN_HELPER_COST = 10
    gen_main()


