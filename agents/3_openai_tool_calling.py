"""
OpenAI Tool Calling Example
This example demonstrates how to use OpenAI's function calling feature
with multiple tools and show how the LLM routes requests to appropriate tools.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def get_weather(location: str, unit: str = "celsius") -> dict:
    """
    Get the current weather for a location.
    In a real application, this would call a weather API.
    """
    # Simulated weather data
    weather_data = {
        "london": {"temp": 15, "condition": "Cloudy", "humidity": 65},
        "new york": {"temp": 22, "condition": "Sunny", "humidity": 45},
        "tokyo": {"temp": 18, "condition": "Rainy", "humidity": 80},
        "paris": {"temp": 17, "condition": "Partly Cloudy", "humidity": 55},
        "sydney": {"temp": 25, "condition": "Sunny", "humidity": 50},
    }
    
    location_lower = location.lower()
    data = weather_data.get(location_lower, {"temp": 20, "condition": "Unknown", "humidity": 50})
    
    return {
        "location": location,
        "temperature": data["temp"],
        "unit": unit,
        "condition": data["condition"],
        "humidity": data["humidity"]
    }


def calculate(expression: str) -> dict:
    """
    Perform a mathematical calculation.
    Safely evaluates simple mathematical expressions.
    """
    try:
        # Only allow safe mathematical operations
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        
        result = eval(expression)
        return {
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}


def get_stock_price(symbol: str) -> dict:
    """
    Get the current stock price for a symbol.
    In a real application, this would call a financial API.
    """
    # Simulated stock data
    stock_data = {
        "AAPL": {"price": 178.50, "change": +2.30, "change_percent": 1.31},
        "GOOGL": {"price": 142.80, "change": -1.20, "change_percent": -0.83},
        "MSFT": {"price": 415.30, "change": +5.40, "change_percent": 1.32},
        "TSLA": {"price": 242.80, "change": +8.60, "change_percent": 3.67},
        "AMZN": {"price": 178.25, "change": -0.50, "change_percent": -0.28},
    }
    
    symbol_upper = symbol.upper()
    data = stock_data.get(symbol_upper, {"price": 0, "change": 0, "change_percent": 0})
    
    return {
        "symbol": symbol_upper,
        "price": data["price"],
        "change": data["change"],
        "change_percent": data["change_percent"]
    }


def send_email(to: str, subject: str, body: str) -> dict:
    """
    Send an email (simulated).
    In a real application, this would use an email service.
    """
    return {
        "status": "success",
        "message": f"Email sent to {to}",
        "to": to,
        "subject": subject,
        "body_preview": body[:50] + "..." if len(body) > 50 else body
    }


def search_database(query: str, table: str = "users") -> dict:
    """
    Search a database (simulated).
    In a real application, this would query a real database.
    """
    # Simulated database results
    results = {
        "users": [
            {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
            {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com"},
        ],
        "products": [
            {"id": 101, "name": "Laptop", "price": 999},
            {"id": 102, "name": "Mouse", "price": 29},
            {"id": 103, "name": "Keyboard", "price": 79},
        ],
        "orders": [
            {"id": 501, "customer": "Alice", "total": 1107},
            {"id": 502, "customer": "Bob", "total": 79},
        ]
    }
    
    table_data = results.get(table, [])
    
    return {
        "table": table,
        "query": query,
        "results": table_data,
        "count": len(table_data)
    }


# ============================================================================
# TOOL DEFINITIONS FOR OPENAI
# ============================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g., London, New York"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate, e.g., '2 + 2' or '10 * 5'"
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current stock price for a company symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock ticker symbol, e.g., AAPL, GOOGL, MSFT"
                    }
                },
                "required": ["symbol"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {
                        "type": "string",
                        "description": "The recipient's email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "The email subject line"
                    },
                    "body": {
                        "type": "string",
                        "description": "The email body content"
                    }
                },
                "required": ["to", "subject", "body"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search a database table for records",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "table": {
                        "type": "string",
                        "enum": ["users", "products", "orders"],
                        "description": "The database table to search"
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]


# Map function names to actual functions
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_stock_price": get_stock_price,
    "send_email": send_email,
    "search_database": search_database,
}


# ============================================================================
# MAIN CONVERSATION HANDLER
# ============================================================================

def run_conversation(user_query: str, verbose: bool = True):
    """
    Run a conversation with tool calling.
    Shows how the LLM routes requests to appropriate tools.
    """
    if verbose:
        print(f"\n{'='*70}")
        print(f"USER QUERY: {user_query}")
        print(f"{'='*70}\n")
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to various tools. Use them to answer user queries accurately."},
        {"role": "user", "content": user_query}
    ]
    
    # First API call - LLM decides which tool(s) to use
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # Let the model decide when to use tools
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # If the model wants to call tools
    if tool_calls:
        if verbose:
            print(f"🤖 LLM wants to call {len(tool_calls)} tool(s):\n")
        
        # Add the assistant's response to messages
        messages.append(response_message)
        
        # Execute each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            if verbose:
                print(f"   → Calling: {function_name}")
                print(f"     Arguments: {json.dumps(function_args, indent=6)}")
            
            # Call the actual function
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)
            
            if verbose:
                print(f"     Result: {json.dumps(function_response, indent=6)}\n")
            
            # Add the function response to messages
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response),
            })
        
        # Second API call - get the final response from the model
        if verbose:
            print("🤖 Getting final response from LLM...\n")
        
        second_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        
        final_answer = second_response.choices[0].message.content
    else:
        # No tool calls needed
        final_answer = response_message.content
        if verbose:
            print("🤖 No tools needed for this query.\n")
    
    if verbose:
        print(f"{'='*70}")
        print(f"FINAL ANSWER:")
        print(f"{'='*70}")
        print(final_answer)
        print(f"{'='*70}\n")
    
    return final_answer


# ============================================================================
# EXAMPLE QUERIES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("OpenAI Tool Calling Examples - 5 Different Tools")
    print("="*70)
    
    # Example 1: Weather query (routes to get_weather)
    run_conversation("What's the weather like in Tokyo?")
    
    # Example 2: Math calculation (routes to calculate)
    run_conversation("What is 157 multiplied by 23?")
    
    # Example 3: Stock price query (routes to get_stock_price)
    run_conversation("What's the current stock price of Apple?")
    
    # Example 4: Database search (routes to search_database)
    run_conversation("Show me all users in the database")
    
    # Example 5: Email sending (routes to send_email)
    run_conversation("Send an email to john@example.com with subject 'Meeting Tomorrow' and tell him the meeting is at 2 PM")
    
    # Example 6: Multiple tools in one query (routes to multiple tools)
    print("\n" + "="*70)
    print("BONUS: Query requiring MULTIPLE tools")
    print("="*70)
    run_conversation("What's the weather in Paris and what's the stock price of Microsoft?")
    
    # Example 7: Complex query with calculation
    run_conversation("Calculate 15% of 250 and tell me the weather in London")

