import openai 
import json 

openai.api_base = "https://yunfan.smoa.cc/v1/chatbotmodel/v1"
openai.api_key = 'sk-jzOqTSBsou/Sfaqaom6lU0D/BSSqjdJ2ACdvZj9UaSrA7Nqp6h+o75khMZImz3k9'

system_prompt = 'Reply only in json with the following format:\n\n{\n    \\"thoughts\\": {\n        \\"text\\":  \\"thoughts\\",\n        \\"reasoning\\": \\"reasoning behind thoughts\\",\n        \\"plan\\": \\"- short bulleted\\\\n- list that conveys\\\\n- long-term plan\\",\n        \\"criticism\\": \\"constructive self-criticism\\",\n        \\"speak\\": \\"thoughts summary to say to user\\",\n    },\n    \\"ability\\": {\n        \\"name\\": \\"ability name\\",\n        \\"args\\": {\n            \\"arg1\\": \\"value1", etc...\n        }\n    }\n}' 

user_prompt = 'Answer as an expert in Planner. \nYour task is:\n\n{question}\n\nAnswer in the provided format.\n\nYour decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and\npursue simple strategies with no legal complications.\n\n\n\n\n\n\n## Abilities\nYou have access to the following abilities you can call:\n\n- finish(reason: string) -> None. Usage: Use this to shut down once you have accomplished all of your goals, or when there are insurmountable problems that make it impossible for you to finish your task.,\n\n- web_search(query: string) -> list[str]. Usage: Searches the web,\n\n- read_webpage(url: string, question: string) -> string. Usage: Read a webpage, and extract specific information from it if a question is specified. If you are looking to extract specific information from the webpage, you should specify a question.,\n\n- list_files(path: string) -> list[str]. Usage: List files in a directory,\n\n- read_file(file_path: string) -> bytes. Usage: Read data from a file,\n\n- write_file(file_path: string, data: bytes) -> None. Usage: Write data to a file,\n\n\n\n\n\n\n'

def llm(question):
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt.format(question=question)}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=messages,
    )
    reply = json.loads(response['choices'][0]['message']['content'])
    return reply

question = 'what can you do?'
question = 'Search the arguments of the class Transformer.Trainer() from its official website'
reply = llm(question)["thoughts"]["speak"]
print('User:', question)
print('Answer:', reply)