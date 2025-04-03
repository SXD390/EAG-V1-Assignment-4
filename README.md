# LLM-MCP-Powered ASCII calculator | Indian Flag Drawing and Email System
Note: This project is a simple demonstration of MCP which combines primitive math, MSPaint and Gmail functions. None of these functions are meant to be used together for production systems, they are used together as this is just a demo.
This project demonstrates an intelligent system that combines mathematical calculations, artistic drawing capabilities, and email communication using AI. The system uses Google's Gemini AI model to orchestrate a sequence of operations that include calculating ASCII values, drawing the Indian flag, and sending the result via email.

## Features

- **Mathematical Calculations**: Performs complex mathematical operations using a dedicated MCP server
- **Flag Drawing**: Automatically draws the Indian flag using Microsoft Paint
- **Email Integration**: Sends the drawn flag via Gmail with custom messages
- **AI Orchestration**: Uses Google's Gemini AI to intelligently sequence and execute operations
- **Modular Design**: Separate MCP servers for different functionalities (Calculator, Gmail)

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with Gmail API enabled
- Microsoft Paint installed
- Google Gemini API key

## Project Structure

```
ROOT/
├── MCP_Server.py      # Calculator and Paint operations server
├── Gmail_MCP_Server.py # Gmail operations server
├── MCP_Client.py      # Main client orchestrating all operations
├── credentials.json       # Gmail API credentials(need to fetch via GCP)
├── token.json            # Gmail API token (generated on first run)
└── README.md            # This file
```

## Usage

1. Start the MCP servers: (If you are testing individual servers)
```bash
# Terminal 1 - Calculator and Paint server
python MCP_Server.py

# Terminal 2 - Gmail server
python Gmail_MCP_Server.py --creds-file-path credentials.json --token-path token.json
```

2. Run the main client:
```bash
python Assignment/MCP_Client.py
```

The system will:
1. Calculate ASCII values of characters in "INDIA"
2. Compute the sum of exponentials of those values
3. Draw the Indian flag using Paint
4. Save the flag image
5. Send the result via email

## How It Works

1. **AI Orchestration**: The Gemini AI model receives a query and breaks it down into steps
2. **Tool Execution**: Each step is executed using appropriate MCP servers
3. **Result Processing**: Results are fed back to the AI for next steps
4. **Final Output**: The system produces both visual (flag) and numerical (calculations) outputs

## Technical Details

- Uses FastMCP for server implementation
- Implements async/await patterns for efficient operation
- Handles Gmail OAuth2 authentication
- Provides detailed logging for debugging
- Supports both mathematical and artistic operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for intelligent orchestration
- Google Gmail API for email functionality
- Microsoft Paint for drawing capabilities
- FastMCP for server implementation
