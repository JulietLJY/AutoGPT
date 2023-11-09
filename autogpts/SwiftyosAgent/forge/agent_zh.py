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
import pprint

LOG = ForgeLogger(__name__)

class ForgeAgent(Agent):
    """
    Forge 的目标是处理样板代码，让您可以专注于代理设计。

    有一篇对代理风景进行了很好的调查论文：https://arxiv.org/abs/2308.11432
    我强烈建议阅读它，因为它将帮助您理解可能性。

    这是代理的关键组成部分的摘要：

    代理的构造：
         - 个人资料
         - 内存
         - 规划
         - 动作

    个人资料：

    代理通常通过扮演特定角色来执行任务。例如，教师、编码员、规划员等。在使用个人资料在 llm 提示中已经显示出它可以提高输出的质量。

    此外，根据所选择的个人资料，代理可以配置为使用不同的 llm。可能性无穷无尽，可以根据手头的任务动态选择个人资料。

    内存：

    内存对于代理积累经验、自我演化以及以更一致、合理和有效的方式行为至关重要。内存有许多方法。但是，有一些想法：长期和短期或工作记忆。您可能需要为每个采取不同的方法。还有关于内存反思的研究，即评估其记忆并重新评估其记忆的能力。例如，将短期记忆压缩成长期记忆。

    规划：

    当人类面临复杂任务时，他们首先将其分解为简单的子任务，然后逐个解决每个子任务。规划模块赋予基于 LLM 的代理思考和计划解决复杂任务的能力，从而使代理更全面、强大和可靠。需要考虑的两种关键方法是：带反馈的规划和不带反馈的规划。

    动作：

    动作将代理的决策转化为具体的结果。例如，如果代理决定写一个文件，动作就是写文件。您可以实施许多方法来执行动作。

    Forge 每个领域都有一个基本模块。但是，您可以自己实现。这只是一个起点。
    """

    def __init__(self, database: AgentDB, workspace: Workspace):
        """
        数据库用于存储任务、步骤和工件元数据。工作区用于存储工件。工作区是文件系统上的目录。

        请随时创建数据库和工作区的子类，以实现您自己的存储
        """
        super().__init__(database, workspace)

    async def create_task(self, task_request: TaskRequestBody) -> Task:
        """
        Forge 的核心是代理协议，它通过创建任务，然后为该任务执行步骤来工作。当代理被要求创建任务时，会调用此方法。

        我们正在通过此函数来添加自定义日志消息。尽管您可以在此处执行任何您想要的操作。
        """
        task = await super().create_task(task_request)
        LOG.info(
            f"📦 Task created: {task.task_id} input: {task.input[:40]}{'...' if len(task.input) > 40 else ''}"
        )
        return task
    
    async def execute_step(self, task_id: str, step_request: StepRequestBody) -> Step:
        """
        要了解如何添加自己的逻辑，请参阅官方教程系列：
        https://aiedge.medium.com/autogpt-forge-e3de53cc58ec

        Forge 的核心是代理协议，它通过创建任务，然后为该任务执行步骤来工作。当代理被要求执行步骤时，将调用此方法。

        创建的任务包含一个输入字符串，对于基准测试，这是代理被要求解决的任务，还包含附加输入，它是一个字典，可以包含任何内容。

        如果您想获取任务，请使用：

        ```
        task = await self.db.get_task(task_id)
        ```

        步骤请求正文基本上与任务请求相同，包含一个输入字符串，对于基准测试，这是代理被要求解决的任务，还包含附加输入，它是一个字典，可以包含任何内容。

        您需要实现一个逻辑，将接受此步骤输入并输出已完成的步骤作为步骤对象。您可以在一个步骤中执行所有操作，也可以将其分解为多个步骤。通过在步骤输出中返回继续请求，用户可以决定是否希望代理继续执行或停止。
        """
        # 下面是一个示例

        step = await self.db.create_step(
            task_id=task_id, input=step_request, is_last=True
        )

        self.workspace.write(task_id=task_id, path="output.txt", data=b"Washington D.C")

        await self.db.create_artifact(
            task_id=task_id,
            step_id=step.step_id,
            file_name="output.txt",
            relative_path="",
            agent_created=True,
        )

        step.output = "Washington D.C"

        LOG.info(f"\t✅ Final Step completed: {step.step_id}. \n" +
                 f"Output should be placeholder text Washington D.C. You'll need to \n" +
                 f"modify execute_step to include LLM behavior. Follow the tutorial " +
                 f"if confused. ")

        return step
