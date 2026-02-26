from fastapi import FastAPI, Query,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import json

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def add_ngrok_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response


class FunctionCallResponse(BaseModel):
    name: str
    arguments: str


def parse_query(query: str) -> dict:
    """Parse the query and map it to the appropriate function with arguments"""
    
    query_lower = query.lower()
    
    # Pattern 1: Ticket Status
    # "What is the status of ticket 83742?" or "ticket 83742"
    ticket_match = re.search(r'ticket\s+(\d+)', query_lower)
    if ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": ticket_id})
        }
    
    # Pattern 2: Schedule Meeting
    # "Schedule a meeting on 2025-02-15 at 14:00 in Room A." or "meeting 2025-02-15 14:00 Room A"
    meeting_match = re.search(r'meeting.*?(\d{4}-\d{2}-\d{2}).*?(\d{2}:\d{2}).*?(room\s+\w+)', query_lower)
    if meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        meeting_room = meeting_match.group(3).strip()
        # Capitalize room name properly
        meeting_room = ' '.join(word.capitalize() for word in meeting_room.split())
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({"date": date, "time": time, "meeting_room": meeting_room})
        }
    
    # Pattern 3: Expense Balance
    # "Show my expense balance for employee 10056." or "expense emp 10056"
    expense_match = re.search(r'expense.*?(?:employee|emp)\s+(\d+)', query_lower)
    if expense_match:
        employee_id = int(expense_match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": employee_id})
        }
    
    # Pattern 4: Performance Bonus (multiple formats)
    # "Calculate performance bonus for employee 10056 for 2025." or "What bonus for emp 72211 in 2025?"
    bonus_match = re.search(r'bonus.*?(?:employee|emp)\s+(\d+).*?(?:for|in)\s+(\d{4})', query_lower)
    if bonus_match:
        employee_id = int(bonus_match.group(1))
        current_year = int(bonus_match.group(2))
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({"employee_id": employee_id, "current_year": current_year})
        }
    
    # Pattern 5: Report Office Issue
    # "Report office issue 45321 for the Facilities department." or "issue 45321 Facilities"
    issue_match = re.search(r'(?:office\s+)?issue\s+(\d+).*?(?:for.*?)?(\w+)(?:\s+department)?', query_lower)
    if issue_match:
        issue_code = int(issue_match.group(1))
        department = issue_match.group(2).capitalize()
        # Skip common words that aren't departments
        if department.lower() not in ['for', 'the', 'in', 'at', 'to']:
            return {
                "name": "report_office_issue",
                "arguments": json.dumps({"issue_code": issue_code, "department": department})
            }
    
    # Default response if no pattern matches
    return {
        "name": "unknown",
        "arguments": json.dumps({})
    }


@app.get("/execute", response_model=FunctionCallResponse)
async def execute_query(q: str = Query(..., description="Query string to parse")):
    """
    Parse a query and return the function name and arguments.
    
    Example: /execute?q=What is the status of ticket 83742?
    Returns: {"name": "get_ticket_status", "arguments": "{\"ticket_id\": 83742}"}
    """
    result = parse_query(q)
    return FunctionCallResponse(
        name=result["name"],
        arguments=result["arguments"]
    )


@app.get("/")
async def root():
    return {"status": "Function Calling API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
