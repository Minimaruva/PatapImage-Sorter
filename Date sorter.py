import os


SUCCESS_PATH = os.path.join(os.path.dirname(__file__), 'Sorted')
FAILURE_PATH = os.path.join(os.path.dirname(__file__), 'Failed')

# Setup folder sturcture
if not os.path.exists(SUCCESS_PATH):
    os.makedirs(SUCCESS_PATH)
if not os.path.exists(FAILURE_PATH):
    os.makedirs(FAILURE_PATH)

