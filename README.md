# Function Calling API

FastAPI endpoint that maps natural language queries to predefined functions with extracted parameters.

## Features

- ✅ Parses natural language queries
- ✅ Maps to 5 predefined functions
- ✅ Extracts parameters automatically
- ✅ Returns function name and JSON arguments
- ✅ CORS enabled for cross-origin requests

## Supported Functions

1. **get_ticket_status(ticket_id: int)**
   - Query: "What is the status of ticket 83742?"
   - Response: `{"name": "get_ticket_status", "arguments": "{\"ticket_id\": 83742}"}`

2. **schedule_meeting(date: str, time: str, meeting_room: str)**
   - Query: "Schedule a meeting on 2025-02-15 at 14:00 in Room A."
   - Response: `{"name": "schedule_meeting", "arguments": "{\"date\": \"2025-02-15\", \"time\": \"14:00\", \"meeting_room\": \"Room A\"}"}`

3. **get_expense_balance(employee_id: int)**
   - Query: "Show my expense balance for employee 10056."
   - Response: `{"name": "get_expense_balance", "arguments": "{\"employee_id\": 10056}"}`

4. **calculate_performance_bonus(employee_id: int, current_year: int)**
   - Query: "Calculate performance bonus for employee 10056 for 2025."
   - Response: `{"name": "calculate_performance_bonus", "arguments": "{\"employee_id\": 10056, \"current_year\": 2025}"}`

5. **report_office_issue(issue_code: int, department: str)**
   - Query: "Report office issue 45321 for the Facilities department."
   - Response: `{"name": "report_office_issue", "arguments": "{\"issue_code\": 45321, \"department\": \"Facilities\"}"}`

## Setup

```bash
# Navigate to project directory
cd path/to/function-calling

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```bash
# Windows
venv\Scripts\python.exe main.py

# Mac/Linux
venv/bin/python main.py
```

Server runs on `http://localhost:8000`

## API Endpoint

### GET /execute

Parse a query and return the function name and arguments.

**Parameters:**
- `q` (required): Query string to parse

**Example Request:**
```bash
curl "http://localhost:8000/execute?q=What%20is%20the%20status%20of%20ticket%2083742?"
```

**Example Response:**
```json
{
  "name": "get_ticket_status",
  "arguments": "{\"ticket_id\": 83742}"
}
```

## Testing

```bash
# Test ticket status
curl "http://localhost:8000/execute?q=What%20is%20the%20status%20of%20ticket%2083742?"

# Test meeting scheduling
curl "http://localhost:8000/execute?q=Schedule%20a%20meeting%20on%202025-02-15%20at%2014:00%20in%20Room%20A."

# Test expense balance
curl "http://localhost:8000/execute?q=Show%20my%20expense%20balance%20for%20employee%2010056."

# Test performance bonus
curl "http://localhost:8000/execute?q=Calculate%20performance%20bonus%20for%20employee%2010056%20for%202025."

# Test office issue
curl "http://localhost:8000/execute?q=Report%20office%20issue%2045321%20for%20the%20Facilities%20department."
```

## Deployment

Use ngrok to expose the API publicly:

```bash
# Windows
.\ngrok.exe http 8000

# Mac/Linux
./ngrok http 8000
```

Copy the HTTPS URL and use it as your API endpoint.

## How It Works

1. **Query Parsing**: Uses regex patterns to identify query type
2. **Parameter Extraction**: Extracts relevant parameters from the query text
3. **Function Mapping**: Maps to the appropriate predefined function
4. **JSON Response**: Returns function name and JSON-encoded arguments

## Project Structure

```
function-calling/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```
