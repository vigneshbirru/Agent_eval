from uuid import uuid4
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage

from models import model
from tools import (
    calculate_right_refund,
    get_today_date,
    issue_refund_ticket,
    get_user_purchase_history,
)
from prompts import agent_system_prompt

load_dotenv()



agent = create_agent(
    model=model,
    system_prompt=agent_system_prompt,
    tools=[
        calculate_right_refund,
        get_user_purchase_history,
        get_today_date,
        issue_refund_ticket,
    ],
    checkpointer=InMemorySaver(),
)

def run_conversation():
    config = {
        "configurable": {
            "thread_id": str(uuid4())
        }
    }

    question = HumanMessage(
        content="I would like to request a refund"
    )

    while True:
        response = agent.invoke(
            {"messages": [question]},
            config=config,
        )

        answer = response["messages"][-1].content
        print(answer)

        user_input = input("Reply (or type 'exit'): ").strip()

        if user_input.lower() == "exit":
            break

        question = HumanMessage(content=user_input)

    print("This job is done!")
    
# if __name__ == "__main__":
#     run_conversation()