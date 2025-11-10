"""
OpenAI Structured Output Example 2: Using Pydantic AI
This example uses Pydantic models for schema validation with OpenAI.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Define Pydantic models for schema validation
class PersonProfile(BaseModel):
    """Simple person profile with Pydantic validation"""
    name: str = Field(description="The person's full name")
    age: int = Field(ge=0, le=150, description="Age must be between 0 and 150")
    occupation: str = Field(description="The person's job or profession")
    
    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Ensure name is not empty or just whitespace"""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


def get_structured_output_with_pydantic(model_class: type[BaseModel], prompt: str, system_message: str):
    """
    Generic function to get structured output using Pydantic models.
    
    Args:
        model_class: Pydantic model class defining the schema
        prompt: User prompt
        system_message: System message for the AI
    
    Returns:
        Validated Pydantic model instance
    """
    # Convert Pydantic model to JSON schema
    schema = model_class.model_json_schema()
    
    # Add additionalProperties: false for strict mode
    schema["additionalProperties"] = False
    
    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": model_class.__name__,
            "strict": True,
            "schema": schema
        }
    }
    
    # Make API call
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        response_format=response_format
    )
    
    # Parse and validate the response using Pydantic
    json_response = json.loads(completion.choices[0].message.content)
    validated_result = model_class.model_validate(json_response)
    
    return validated_result


def example_person_profile():
    """Example 1: Generate and validate a person profile"""
    print("Example 1: Person Profile with Pydantic Validation")
    print("="*50)
    
    result = get_structured_output_with_pydantic(
        model_class=PersonProfile,
        prompt="Generate a profile for a software engineer named Bob.",
        system_message="You are a helpful assistant that generates fictional person profiles."
    )
    
    # Access validated fields
    print(f"\nName: {result.name}")
    print(f"Age: {result.age}")
    print(f"Occupation: {result.occupation}")
    
    # Export as JSON
    print("\nFull JSON output:")
    print(result.model_dump_json(indent=2))
    print("\n" + "="*50 + "\n")


def example_with_validation_error():
    """Example 3: Demonstrate Pydantic validation catching errors"""
    print("Example 3: Validation Error Handling")
    print("="*50)
    
    try:
        # Manually create an invalid instance to show validation
        invalid_data = {
            "name": "   ",  # Empty name (should fail validation)
            "age": 200,     # Age too high (should fail validation)
            "occupation": "Developer"
        }
        
        # This will raise validation errors
        PersonProfile.model_validate(invalid_data)
        
    except Exception as e:
        print("\nValidation errors caught by Pydantic:")
        print(f"Error: {e}")
        print("\nPydantic ensures data integrity before processing!")
    
    print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    print("OpenAI Structured Output - Pydantic AI Validation Examples\n")
    print("="*50 + "\n")
    
    # Example 1: Person profile
    example_person_profile()
    
    # Example 2: Show validation capabilities
    example_with_validation_error()

