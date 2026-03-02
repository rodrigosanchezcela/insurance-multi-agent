
import json

from langchain_openai import ChatOpenAI
from insurance_multi_agent.config import Config
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from insurance_multi_agent.agents.prompts import SUPERVISOR_PROMPT
import logging

cfg = Config()
logger = logging.getLogger(__name__)


class ReActSupervisor:  
    """
    ReAct supervisor agent implemented from scratch.
    Implements loop: think -> act -> observe.
    """

    def __init__(self, model: str, tools: list):
        self.tools = {tool.name : tool for tool in tools}
        self.llm = ChatOpenAI(api_key=cfg.openrouter_api_key,
                                base_url="https://openrouter.ai/api/v1",
                                model=model,
                                max_retries=cfg.max_retries
                                )
        self.llm_with_tools = self.llm.bind_tools(tools)

    
    def run(self, text: str, max_iterations: int = 10) -> str:
        """
        Run the ReAct loop until the model returns a final answer.

        Args:
            text (str): The cleaned insurance document text.
            max_iterations (int): Safety cap on the number of LLM calls.
        Returns:
            str: The final answer produced by the supervisor.
        """
        messages = [
            SystemMessage(content=SUPERVISOR_PROMPT),
            HumanMessage(content=text),
        ]
        history = {"steps": [], "final_answer": None}

        for i in range(max_iterations):
            response = self.llm_with_tools.invoke(messages)
            
            messages.append(response) 
            logger.info(f"[Iteration {i}] tool_calls: {[tc['name'] for tc in response.tool_calls]}")

            if not response.tool_calls:
                logger.info("[ReActSupervisor] Final answer reached.")
                history["final_answer"] = response.content
                return history

            for tool_call in response.tool_calls:
                tool = self.tools[tool_call["name"]]
                result = tool.invoke(tool_call["args"])

                history["steps"].append({
                    "iteration": i,
                    "tool_call": tool_call,
                    "tool_result": result
                })
                logger.info(f"[{tool_call['name']}] → {str(result)[:300]}")
                messages.append(
                    ToolMessage(
                        content=json.dumps(result, default=str),
                        tool_call_id=tool_call["id"],
                    )
                )

        logger.warning("[ReActSupervisor] Max iterations reached without a final answer.")
        return "Max iterations reached without a final answer."


        
        