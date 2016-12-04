import os
import generate_input as inputs
import generate_output as outputs
import shutil

if os.path.exists(inputs.INPUT_DIR_NAME):
    # os.removedirs(inputs.INPUT_DIR_NAME)
    shutil.rmtree(inputs.INPUT_DIR_NAME)

if os.path.exists(outputs.OUTPUT_DIR_NAME):
    # os.removedirs(outputs.OUTPUT_DIR_NAME)
    shutil.rmtree(outputs.OUTPUT_DIR_NAME)
