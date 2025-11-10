# OpenAI Structured Outputs Examples

This repository demonstrates two different approaches to getting structured outputs from OpenAI's API using Python.

## Overview

### Method 1: Strict JSON Mode (`1_openai_strict_json_mode.py`)

Uses OpenAI's native structured output feature with JSON schema and `strict: True` mode. This guarantees the model will return data in the exact format specified by your JSON schema.

**Advantages:**

- Native OpenAI feature
- Guaranteed schema adherence
- No additional validation libraries needed
- Direct JSON schema definition

### Method 2: Pydantic AI Validation (`2_pydantic_ai_validation.py`)

Uses Pydantic models for schema definition and validation. This provides type safety, custom validators, and robust data validation.

**Advantages:**

- Type safety with Python type hints
- Custom validation logic (e.g., field validators)
- Better IDE support and autocomplete
- Reusable models across your application
- Rich error messages for validation failures

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

1. **Install uv (if you haven't already):**

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. **Install dependencies:**

sync the entire environment:

```bash
uv sync
```

3. **Set up environment variables:**

Create a `.env` file in the project root:

```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

4. **Get an OpenAI API key:**

- Go to https://platform.openai.com/api-keys
- Create a new API key
- Add it to your `.env` file

## Usage

### Run Method 1 (Strict JSON Mode):

```bash
uv run python 1_openai_strict_json_mode.py
```

Or with standard Python:

```bash
python 1_openai_strict_json_mode.py
```

This script demonstrates:

- Generating a simple person profile with 3 fields
- Direct JSON schema definition with `strict: True`

### Run Method 2 (Pydantic AI):

```bash
uv run python 2_pydantic_ai_validation.py
```

Or with standard Python:

```bash
python 2_pydantic_ai_validation.py
```

This script demonstrates:

- Simple person profile with Pydantic validation
- Field-level validation (e.g., age range 0-150, name validation)
- Handling validation errors with clear error messages

## Key Differences

| Feature           | Strict JSON Mode      | Pydantic AI              |
| ----------------- | --------------------- | ------------------------ |
| Schema Definition | JSON Schema dict      | Python classes           |
| Type Safety       | Runtime only          | Compile-time + Runtime   |
| Custom Validation | Limited               | Full control             |
| IDE Support       | Basic                 | Excellent                |
| Error Messages    | Generic               | Detailed                 |
| Learning Curve    | Steeper (JSON Schema) | Gentler (Python classes) |

## Examples Included

Simple, easy-to-understand examples:

1. **Method 1** - Person profile generation with strict JSON schema
2. **Method 2** - Person profile with Pydantic validation and error handling

## Requirements

- Python 3.8+
- OpenAI API key
- Models that support structured outputs (e.g., `gpt-4o-2024-08-06` or later)

## Notes

- Structured outputs require specific OpenAI models (gpt-4o-2024-08-06 or later)
- The `strict: True` parameter ensures 100% schema adherence
- Pydantic provides additional runtime validation beyond schema compliance

## License

MIT License - Feel free to use these examples in your projects!
