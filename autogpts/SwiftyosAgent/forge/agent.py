from forge.sdk import (
    Agent,
    AgentDB,
    ForgeLogger,
    Step,
    StepRequestBody,
    Task,
    TaskRequestBody,
    Workspace,    
    PromptEngine,	
    chat_completion_request,	
    ChromaMemStore	
)
import json	
import os 
import pprint
import pandas as pd
from tqdm import tqdm
LOG = ForgeLogger(__name__)

class ForgeAgent(Agent):
    def __init__(self, database: AgentDB, workspace: Workspace):
        super().__init__(database, workspace)
        self.leetcode_api_instance = self.get_leetcode_api_instance()

    def get_leetcode_api_instance(self):
        """
        Get the leetcode api instance
        """
        import leetcode
        import leetcode.auth
        configuration = leetcode.Configuration()

        # From Dev Tools/Application/Cookies/LEETCODE_SESSION
        with open('/home/jyli/Agent/AutoGPT/autogpts/SwiftyosAgent/forge/leetcode_session') as f:
            leetcode_session = f.read()
        csrf_token = leetcode.auth.get_csrf_cookie(leetcode_session)

        configuration.api_key["x-csrftoken"] = csrf_token
        configuration.api_key["csrftoken"] = csrf_token
        configuration.api_key["LEETCODE_SESSION"] = leetcode_session
        configuration.api_key["Referer"] = "https://leetcode.com"
        configuration.debug = False

        api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

        return api_instance

    async def create_task(self, task_request: TaskRequestBody) -> Task:
        task = await super().create_task(task_request)
        LOG.info(
            f"📦 Task created: {task.task_id} input: {task.input[:40]}{'...' if len(task.input) > 40 else ''}"
        )
        return task

    async def execute_step(self, task_id: str, step_request: StepRequestBody) -> Step:
        # Firstly we get the task this step is for so we can access the task input
        task = await self.db.get_task(task_id)

        # Create a new step in the database
        step = await self.db.create_step(
            task_id=task_id, input=step_request, is_last=True
        )

        LOG.info(f"\t✅ Final Step completed: {step.step_id} input: {step.input[:19]}")

        prompt_engine = PromptEngine("gpt-3.5-turbo")
        
        system_prompt = prompt_engine.load_prompt("system-format")

        LOG.info(f"User Input: {step.input}")
        if step.input.lower() in ['leetcode-hard-gym', 'leetcode', 'lc']:
            data_path = "/home/jyli/Agent/AutoGPT/autogpts/SwiftyosAgent/data/leetcode_hard_solutions.jsonl"
            
            dataset = pd.read_json(data_path, lines=True)[:1]
            for question_id, data in tqdm(dataset.iterrows()):
                input_kwargs = {
                    "website": data["url"], 
                }
                savepath = f"/home/jyli/Agent/AutoGPT/autogpts/SwiftyosAgent/solutions/{data['question_title'].lower().replace(' ', '-')}"
                input_prompt = prompt_engine.load_prompt("leetcode-hard-gym", **input_kwargs)

                LOG.info(f"User Input: {input_prompt}")
                task_kwargs = {
                    "task": input_prompt,
                    "abilities": self.abilities.list_abilities_for_prompt(),
                }
                task_prompt = prompt_engine.load_prompt("task-step", **task_kwargs)

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": task_prompt},
                ]

                step = await self.get_step_output(task_id, step, messages)

                with open(savepath, 'w') as f:
                    f.write(step.output)

            return step

        else:
            task_kwargs = {
                "task": step.input,
                "abilities": self.abilities.list_abilities_for_prompt(),
            }

            task_prompt = prompt_engine.load_prompt("task-step", **task_kwargs)

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_prompt},
            ]

            step = await self.get_step_output(task_id, step, messages)
            return step

    async def get_step_output(self, task_id, step, messages) -> Step:
        try:
            chat_completion_kwargs = {
                "messages": messages,
                "model": "gpt-3.5-turbo",
            }
            chat_response = await chat_completion_request(**chat_completion_kwargs)
            answer = json.loads(chat_response["choices"][0]["message"]["content"])
            LOG.info(pprint.pformat(answer))

        except json.JSONDecodeError as e:
            LOG.error(f"Unable to decode chat response: {chat_response}")

        except Exception as e:
            LOG.error(f"Unable to generate chat response: {e}")

        ability = answer["ability"]

        LOG.info(f"Function: {ability['name']}, Args: {ability['args']}")
        output = await self.abilities.run_ability(
            task_id, ability["name"], **ability["args"]
        )
        
        if "thoughts" in answer and "speak" in answer["thoughts"]:
            step.output = str(answer["thoughts"]["speak"]) + str(output)
        else:
            step.output = str(answer) + str(output)

        print(step.output)

        return step
