# RAG-Driven Generative AI

A Python application that implements Retrieval-Augmented Generation (RAG) pipelines for space exploration content. The system fetches Wikipedia articles about space exploration, processes them, and prepares them for use with OpenAI's API.

## Features

- **Web Scraping**: Automatically fetches content from Wikipedia articles about space exploration
- **Content Cleaning**: Removes references, bibliographies, and other non-essential content
- **AWS Integration**: Securely retrieves OpenAI API keys from AWS Secrets Manager
- **Text Processing**: Cleans and formats text for optimal use with language models

## Prerequisites

- Python 3.8 or higher
- AWS CLI configured with appropriate credentials
- OpenAI API key stored in AWS Secrets Manager

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-driven-gen-ai
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install boto3 urllib3 openai requests beautifulsoup4
   ```

## Configuration

### AWS Setup

1. **Configure AWS credentials**
   ```bash
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, default region, and output format.

2. **Store OpenAI API key in AWS Secrets Manager**
   ```bash
   aws secretsmanager create-secret \
     --name "openai/apiKey" \
     --description "OpenAI API Key for RAG application" \
     --secret-string "your-openai-api-key-here"
   ```

### Environment Variables

The application automatically retrieves the OpenAI API key from AWS Secrets Manager, so no additional environment variables are needed.

## Usage

### Running the Application

1. **Activate your virtual environment** (if not already active)
   ```bash
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

2. **Run the main script**
   ```bash
   python src/main.py
   ```

### What the Application Does

1. **Fetches Space Exploration Content**: Downloads content from 30+ Wikipedia articles about space exploration, including:
   - Space exploration missions (Apollo, Voyager, etc.)
   - Space agencies (NASA, ESA)
   - Spacecraft and telescopes (Hubble, James Webb, etc.)
   - Mars rovers and planetary missions

2. **Processes Content**: 
   - Removes reference numbers `[1]`, `[2]`, etc.
   - Eliminates bibliography and reference sections
   - Cleans up formatting and extracts clean text

3. **Outputs Processed Data**: Saves all cleaned content to `llm.txt` for use with language models

### Output

The application creates a file called `llm.txt` containing all the cleaned Wikipedia content, ready for use in RAG applications or other AI pipelines.

## Project Structure

```
rag-driven-gen-ai/
├── src/
│   └── main.py              # Main application script
├── tests/                   # Test files
├── pyproject.toml          # Python project configuration
├── pdm.lock               # Dependency lock file
├── Makefile               # Build automation
├── run.sh                 # Execution script
└── README.md              # This file
```

## Troubleshooting

### SSL Certificate Errors

If you encounter SSL certificate errors when running the application locally, the code includes SSL verification bypass for development purposes. This is handled automatically in the current implementation.

### AWS Credentials Issues

- Ensure your AWS credentials are properly configured
- Verify you have permissions to access AWS Secrets Manager
- Check that the secret `openai/apiKey` exists in your AWS account

### Missing Dependencies

If you get import errors, install missing packages:
```bash
pip install <package-name>
```

## Development

### Adding New Wikipedia Articles

To add new articles to the scraping list, edit the `urls` list in `src/main.py`:

```python
urls = [
    "https://en.wikipedia.org/wiki/Your_New_Article",
    # ... existing URLs
]
```

### Customizing Content Processing

Modify the `clean_text()` and `fetch_and_clean()` functions in `src/main.py` to customize how content is processed and cleaned.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues and questions, please open an issue in the repository or contact the development team.
