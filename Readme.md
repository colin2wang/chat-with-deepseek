# DeepSeek Chat Application

## Overview
This Python application is designed to interact with the DeepSeek Chat API, offering users a graphical user interface (GUI) to send prompts and receive responses. It incorporates various features such as cookie management, session handling, and a retry mechanism for robust communication with the API.

## Features
1. **Cookies Management**:
    - The application can load previously saved cookies from a `cookies.json` file to maintain session continuity.
    - If no saved cookies are found, it guides the user through a login process to obtain new cookies and then saves them for future use.
2. **Request Headers**:
    - It loads the necessary request headers from a `deepseek_headers.yml` file. These headers are crucial for making valid requests to the DeepSeek Chat API.
3. **Chat Session Management**:
    - The application creates new chat sessions with unique `chat_session_id`. This allows for organized and independent conversations.
    - It keeps track of the `parent_message_id` to maintain the context of the conversation.
4. **Retry Mechanism**:
    - When sending requests to the API, the application uses the `tenacity` library to retry failed requests up to three times with a two - second interval between each attempt.
5. **Graphical User Interface (GUI)**:
    - The GUI is built using the `tkinter` library, providing an intuitive and user - friendly interface.
    - Users can enter prompts, send them, and view responses in a formatted way.
    - There are also options to start a new conversation, enable deep thinking, and enable web search.

## Prerequisites
- **Python Version**: Python 3.x is required to run this application.
- **Required Python Packages**:
    - `requests`: Used for making HTTP requests to the DeepSeek Chat API.
    - `tkinter`: The standard GUI library for Python, used to create the user interface.
    - `tkhtmlview`: Enables the display of HTML - formatted text in the GUI.
    - `markdown2`: Converts Markdown text to HTML for better formatting of responses.
    - `colorlog`: Adds colored output to the logging system for better readability.
    - `selenium`: Used for the login process to interact with the browser and obtain cookies.
    - `tenacity`: Implements the retry mechanism for failed requests.
    - `PyYAML`: Parses the YAML file containing the request headers.

## Installation
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required Python packages using the following command:
```bash
pip install -r requirements.txt
```

## Usage
1. **Set Up EdgeDriver**:
    - Download the appropriate EdgeDriver version from the official website and set its path in the code. The default path in the code is `D:\Software\Frameworks\edgedriver_win64\msedgedriver.exe`, which you need to adjust according to your actual situation.
2. **Prepare Configuration Files**:
    - Create a `cookies.json` file (initially empty if no cookies are saved).
    - Create a `deepseek_headers.yml` file with the necessary request headers.
3. **Run the Application**:
    - Execute the `main.py` file using the following command:
```bash
python main.py
```
4. **Interact with the Application**:
    - If no saved cookies are found, you will be prompted to complete the login process in the browser. After logging in, press Enter to continue.
    - Enter your prompt in the input box and click the "Send" button to receive a response from the DeepSeek Chat API.
    - Use the "New Conversation" button to start a new chat session.
    - Check the "Deep Thinking" and "Web Search" checkboxes to enable corresponding features.

## Logging
The application uses a colored logging system to provide detailed information about its operations. Log messages include information about cookie loading and saving, request sending, response handling, and any errors that occur.

## Notes
- Make sure the EdgeDriver version matches your Edge browser version to avoid compatibility issues.
- Keep the `cookies.json` and `deepseek_headers.yml` files in the correct directory and ensure their content is valid.