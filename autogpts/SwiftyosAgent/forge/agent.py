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

        # Log the message
        LOG.info(f"\t✅ Final Step completed: {step.step_id} input: {step.input[:19]}")

        # Initialize the PromptEngine with the "gpt-3.5-turbo" model
        prompt_engine = PromptEngine("gpt-3.5-turbo")

        # Load the system and task prompts
        system_prompt = prompt_engine.load_prompt("system-format")

        # Initialize the messages list with the system prompt
        messages = [
            {"role": "system", "content": system_prompt},
        ]

        # Define the task parameters
        LOG.info(f"User Input: {step.input}")
        task_kwargs = {
            "task": step.input,
            "abilities": self.abilities.list_abilities_for_prompt(),
        }

        # Load the task prompt with the defined task parameters
        task_prompt = prompt_engine.load_prompt("task-step", **task_kwargs)

        # Append the task prompt to the messages list
        messages.append({"role": "user", "content": task_prompt})

        try:
            # Define the parameters for the chat completion request
            chat_completion_kwargs = {
                "messages": messages,
                "model": "gpt-3.5-turbo",
            }

            # Make the chat completion request and parse the response
            chat_response = await chat_completion_request(**chat_completion_kwargs)

            answer = json.loads(chat_response["choices"][0]["message"]["content"])

            # Log the answer for debugging purposes
            LOG.info(pprint.pformat(answer))

        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            LOG.error(f"Unable to decode chat response: {chat_response}")
        except Exception as e:
            # Handle other exceptions
            LOG.error(f"Unable to generate chat response: {e}")

        # Extract the ability from the answer
        ability = answer["ability"]

        # Run the ability and get the output
        # We don't actually use the output in this example

        LOG.info(f"Function: {ability['name']}, Args: {ability['args']}")
        output = await self.abilities.run_ability(
            task_id, ability["name"], **ability["args"]
        )

        print(output)
        
        # Set the step output to the "speak" part of the answer
        if "thoughts" in answer:
            step.output = str(answer["thoughts"]["speak"]) + str(output)
        else:
            print(answer)
            step.output = str(answer) + str(output)

        # Return the completed step
        return step
