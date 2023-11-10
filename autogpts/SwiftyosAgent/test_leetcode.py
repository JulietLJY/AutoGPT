from leetcode_env.environment import LeetCodeEnv
from leetcode_env.types import LeetCodeSubmission, ProgrammingLanguage
import re 
from tqdm import tqdm 
import os 

solution_dir = '/home/jyli/Agent/AutoGPT/autogpts/SwiftyosAgent/solutions/'
accuracy = 0
num = 0
for name in os.listdir(solution_dir):
    with open(os.path.join(solution_dir, name)):
        text = f.read()
    code = re.find_all(r'```python\s*([\s\S]+?)\s*```', text)[0]

    sub = LeetCodeSubmission(code=code,
                            lang=ProgrammingLanguage.PYTHON3,
                            question_slug='two-sum')

    env = LeetCodeEnv()
    status, reward, done, submission_result = env.step(sub)
    print(status)
    if status == 'Accepted':
        accuracy = 1
    num += 1
accuracy /= num
print(accuracy)
