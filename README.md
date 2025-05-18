# Giphy Adapter

A Python adapter for interacting with the Giphy API. This project provides functionality to search for GIFs and retrieve GIFs by their ID using the Giphy API.

## Features

- Search for GIFs based on a query.
- Retrieve GIF details by their unique ID.
- Uses Pydantic models for data validation and serialization.

## Requirements

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/giphy-adapter.git
   cd giphy-adapter
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Giphy API key as an environment variable:

   ```bash
   export GIPHY_API_KEY=your_api_key_here
   ```

## Usage

### Example: Search for a GIF

```python
from adapter import GiphyAdapter

adapter = GiphyAdapter()
gif = adapter.search_gif("sad")
if gif:
    print(f"Found GIF: {gif.title}")
    print(f"URL: {gif.content_url}")
```

### Example: Get a GIF by ID

```python
from adapter import GiphyAdapter

adapter = GiphyAdapter()
gif = adapter.get_gif_by_id("xT9IgDEI1iZyb2wqo8")
if gif:
    print(f"Found GIF: {gif.title}")
    print(f"URL: {gif.content_url}")
```
