## Command
./run arena enter SwiftyosAgent
./run agent start SwiftyosAgent

## TODO
### TaskList
1. **Search websites for provided information**

Search the website of solution code of the two sum problem solution.

Search the website of arguments of transformers.Trainer().

2. **Read websites and answer questions**

Read the website https://huggingface.co/docs/transformers/main_classes/trainer. 
Question: "What're the arguments of transformers.Trainer()?"

Read the website https://huggingface.co/codellama. 
Question: "Extract links of the codellama pretrained models."

Read the website https://github.com/azl397985856/leetcode/blob/master/problems/1.two-sum.en.md
Question: "Extract the solution codes of the two sum problem solution."

3. **Search websites, Read websites and Answer questions**

Search the arguments of transformers.Trainer().

Search the download links of the codellama pretrained models.

Search the solution code of the two sum problem solution.

## Idea
**What is a USEFUL coding Agent?**

### 目前的Code Agent的思路
使用coding环境的反馈来改进代码
1. 写出来需求，LLM生成代码
2. 利用LLM的代码输入到环境中进行测试，并根据反馈设计prompt给GPT来生成新的代码/手动修复代码以符合需求，可能会重复几轮

### 可以改进的地方（自己使用GPT写code的时候遇到的问题）
**思路一**：使用GPT写code可能产生的问题：由于库函数（例如transformers）的版本更新，导致GPT输出的结果不适用
GPT是否可以实时联网从github或者huggingface上搜索最新的代码？

**思路二**：当我使用GPT产生的代码有问题的时候，另一个做法：在网上搜索解题策略
那么LLM能否联网搜索解题策略？
例如数据集Leetcode-Hard上面，目前所有的LLM都只有个位数的解题策略
但LeetCode网站上具有所有题目的解题策略和解答，如果GPT可以学习这个查询过程，就可以达到100%的准确率

就像人类通过使用工具来达成目的一样，LLM as Agent相比于LLM最大的进步在于在一个开放世界，可以使用各式各样的工具获得知识并利用它们来解决问题
并不止于编码环境，而是可以调用浏览器等更多工具，例如AutoGPT可以从google搜索网页并浏览相关网页

**思路三**：GPT通常会产生一个示例程序，例如
```python
def add(x, y):
    return x + y

# test
add(1, 1) # output: 2
```
但是输出的结果只是LLM预测的结果，而不一定是程序运行可以产生的真实结果，我们还需要自己将code复制粘贴到程序中运行才能获取真实结果
那么LLM能否自动运行程序并且展示真实输出结果？
目前的Coding LLM Agent只是按照规定的格式，例如Humaneval的function，或者leetcode的solution，输入人为设定的测试框架
但是我们想要的是LLM自动根据需求设计test程序并且调用，程序的格式不受限制，且由LLM自己设计测试框架，而不是人为设计


