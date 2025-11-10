"""
OpenAI Structured Output Example 1: Using Strict JSON Mode
This example uses OpenAI's native structured output feature with JSON schema.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_structured_output_strict_json():
    """
    Use OpenAI's structured output with strict JSON schema.
    This ensures the model returns data in the exact format specified.
    """
    
    # Define a simple JSON schema for structured output
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "person_info",
            "strict": True,  # Enable strict mode for guaranteed schema adherence
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The person's full name"
                    },
                    "age": {
                        "type": "integer",
                        "description": "The person's age in years"
                    },
                    "occupation": {
                        "type": "string",
                        "description": "The person's job or profession"
                    }
                },
                "required": ["name", "age", "occupation"],
                "additionalProperties": False
            }
        }
    }
    
    # Make the API call with structured output
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",  # Note: structured outputs require specific models
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates fictional person profiles."
            },
            {
                "role": "user",
                "content": "Generate a profile for a software engineer named Alice."
            }
        ],
        response_format=response_format
    )
    
    # The response will be in the exact format specified in the schema
    result = completion.choices[0].message.content
    print("Structured Output (Strict JSON Mode):")
    print(result)
    print("\n" + "="*50 + "\n")
    
    return result

if __name__ == "__main__":
    print("OpenAI Structured Output - Strict JSON Mode Examples\n")
    print("="*50 + "\n")
    
    # Example 1: Generate person profile
    get_structured_output_strict_json()


