import pandas as pd
data_path = "/home/jyli/Agent/AutoGPT/autogpts/SwiftyosAgent/data/leetcode_hard_solutions.jsonl"
dataset = pd.read_json(data_path, lines=True)
for data in dataset.index:
import pdb;pdb.set_trace()