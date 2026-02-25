# Trendlearn-AI

Trendlearn-AI is an automated course generator that picks up top trending tech topics in Brazil (using Google Trends) and generates a mini-course website using OpenAI's GPT-4o-mini.

## Setup

1. Clone the repository.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up your `.env` file with your `OPENAI_API_KEY`:

```bash
OPENAI_API_KEY="your-api-key-here"
```

## Running

Execute the main script:

```bash
python main.py
```

This will fetch the latest trend, ask OpenAI to generate a syllabus, and output a beautiful, modern `index.html`. 

## GitHub Actions

This project includes a daily cron job (GitHub Actions) to automatically update the course each day. Ensure you set the `OPENAI_API_KEY` repository secret on GitHub for the action to run!
