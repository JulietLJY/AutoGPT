import os

import uvicorn
from dotenv import load_dotenv

import forge.sdk.forge_log

LOG = forge.sdk.forge_log.ForgeLogger(__name__)


logo = """\n\n
       d8888          888             .d8888b.  8888888b. 88888888888 
      d88888          888            d88P  Y88b 888   Y88b    888     
     d88P888          888            888    888 888    888    888     
    d88P 888 888  888 888888 .d88b.  888        888   d88P    888     
   d88P  888 888  888 888   d88""88b 888  88888 8888888P"     888     
  d88P   888 888  888 888   888  888 888    888 888           888     
 d8888888888 Y88b 888 Y88b. Y88..88P Y88b  d88P 888           888     
d88P     888  "Y88888  "Y888 "Y88P"   "Y8888P88 888           888     
                                                                      
                                                                      
                                                                      
                8888888888                                            
                888                                                   
                888                                                   
                8888888  .d88b.  888d888 .d88b.   .d88b.              
                888     d88""88b 888P"  d88P"88b d8P  Y8b             
                888     888  888 888    888  888 88888888             
                888     Y88..88P 888    Y88b 888 Y8b.                 
                888      "Y88P"  888     "Y88888  "Y8888              
                                             888                      
                                        Y8b d88P                      
                                         "Y88P"                v0.1.0
\n"""

if __name__ == "__main__":
    ######################## create localhost ########################
    print(logo)
    port = os.getenv("PORT", 8000)
    LOG.info(f"Agent server starting on http://localhost:{port}")
    load_dotenv()
    forge.sdk.forge_log.setup_logger()

    uvicorn.run(
        "forge.app:app", host="localhost", port=port, log_level="error", reload=True
    )

    ######################## debug ########################
    # import os
    # from forge.agent import ForgeAgent
    # from forge.sdk import LocalWorkspace, StepRequestBody, Step, StepOutput, Status
    # from .db import ForgeDatabase
    
    # database_name = os.getenv("DATABASE_STRING")
    # workspace = LocalWorkspace(os.getenv("AGENT_WORKSPACE"))
    # database = ForgeDatabase(database_name, debug_enabled=False)
    # agent = ForgeAgent(database=database, workspace=workspace)

    # from datetime import datetime

    # step_request = Step(
    #     created_at=datetime.now(),
    #     modified_at=datetime.now(),
    #     task_id="50da533e-3904-4401-8a07-c49adf88b5eb",
    #     step_id="6bb1801a-fd80-45e8-899a-4dd723cc602e",
    #     name="Write to file",
    #     status=Status.created,
    #     output="I am going to use the write_to_file command and write Washington to a file called output.txt",
    #     additional_output=StepOutput(),
    #     artifacts=[],
    #     is_last=True
    # )
    # output = agent.execute_step(task_id='debug', step_request=step_request).output
    # LOG.info(f'Agent Output: {output}')
    # import pdb;pdb.set_trace()

