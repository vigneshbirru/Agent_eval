from langchain.tools import tool
from data import users_data
from dotenv import load_dotenv
import logging
from objects import PurchaseItem
from datetime import date, datetime

load_dotenv()

@tool
def get_user_purchase_history(user:str) -> dict:
    """this tool takes the user username and return a dict of the purchase history if 
    the user exists"""
    logging.info(f"using get_user_pruchase_history tool on user: {user}")
    if users_data.get(user):
        return users_data[user]
    return  {"status": "there was no  username found"}



@tool
def calculate_right_refund(user: str,items: list[PurchaseItem],) -> str:
    """Calculate the refund for eligible purchased items."""

    history = users_data.get(user)

    if not history:
        return "No username found."

    today = date.today()
    total_refund = 0

    for item in items:
        purchase = history.get(item.name)

        if not purchase:
            continue

        purchase_date = datetime.strptime(
            purchase["date"], "%Y-%m-%d"
        ).date()

        if purchase_date > today:
            continue

        if (today - purchase_date).days > 30:
            continue

        total_refund += purchase["price"]

    return f"The eligible refund amount is: {total_refund}"

@tool
def issue_refund_ticket(user:str, refund_amount: int )-> str:
    """this tool will send to the right team to return the refund"""
    
    logging.info(f"using issue_refund_ticket for user: {user}")
    return f"a refund ticket has been issued successfully with the amount of {refund_amount}"

@tool
def get_today_date(user:str)-> str:
    "this tool will return today's date"
    logging.info(f"using the date_today_date tool")
    return date.today().isoformat()

# print(get_user_purchase_history.invoke("user123"))
# book = PurchaseItem(name="book")
# pen = PurchaseItem(name="pen")
# print(calculate_right_refund.invoke({"user":"user123",
#                                     "items":[book,pen]}))
print(issue_refund_ticket.invoke({
    "user": "user123",
    "refund_amount": 30
}))

print(get_today_date.invoke("user123"))