import tkinter as tk
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel
import markdown2
from config import load_cookies, load_headers, logger
import requests
import logging  # 导入 logging 模块

class ChatApp:
    def __init__(self, root):
        """
        Initialize the ChatApp with the given root Tkinter window.

        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title("DeepSeek Chat")
        self.url = "https://chat.deepseek.com/api/v0/chat/completion"
        self.headers = load_headers()
        if not self.headers:
            raise SystemExit("Failed to load headers, exiting program.")

        self.cookies = load_cookies()
        self.session = requests.Session()

        if self.cookies:
            logging.info("Applying loaded cookies to the session...")
            for cookie in self.cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
            logging.info("Successfully applied cookies to the session.")
        else:
            logging.info("No saved cookies found, starting login process...")
            # 这里需要实现登录获取cookies的逻辑，原代码中通过Selenium实现，此处暂未完整实现
            self.cookies = None
            if self.cookies:
                logging.info("Applying newly obtained cookies to the session...")
                for cookie in self.cookies:
                    self.session.cookies.set(cookie['name'], cookie['value'])
                logging.info("Successfully applied newly obtained cookies to the session.")

        self.generate_new_chat_session()

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)

        self.input_label = tk.Label(root, text="Enter question:")
        self.input_label.grid(row=0, column=0, pady=10, sticky="e")

        self.input_text = scrolledtext.ScrolledText(root, width=50, height=5)
        self.input_text.grid(row=0, column=1, pady=5, sticky="ew")
        self.input_text.columnconfigure(0, weight=1)

        self.send_button = tk.Button(root, text="Send", command=self.send_prompt)
        self.send_button.grid(row=0, column=2, pady=10, sticky="w")

        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)

        self.new_conversation_button = tk.Button(self.button_frame, text="New Conversation", command=self.new_conversation)
        self.new_conversation_button.grid(row=0, column=0, padx=5)

        self.thinking_enabled_var = tk.BooleanVar()
        self.thinking_enabled_checkbox = tk.Checkbutton(self.button_frame, text="Deep Thinking", variable=self.thinking_enabled_var)
        self.thinking_enabled_checkbox.grid(row=0, column=1, padx=5)

        self.search_enabled_var = tk.BooleanVar()
        self.search_enabled_checkbox = tk.Checkbutton(self.button_frame, text="Web Search", variable=self.search_enabled_var)
        self.search_enabled_checkbox.grid(row=0, column=2, padx=5)

        self.output_frame = tk.Frame(root)
        self.output_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")
        self.output_frame.columnconfigure(0, weight=1)
        self.output_frame.rowconfigure(0, weight=1)

        self.output_scrollbar = tk.Scrollbar(self.output_frame)
        self.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_label = HTMLLabel(self.output_frame, width=60, height=20)
        self.output_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.output_label.config(bg='white')
        self.output_label.config(yscrollcommand=self.output_scrollbar.set)
        self.output_scrollbar.config(command=self.output_label.yview)

    def generate_new_chat_session(self):
        """
        Generate a new chat session and set the chat_session_id and parent_message_id.
        """
        from session_management import create_chat_session
        self.chat_session_id = create_chat_session(self.session, self.headers)
        if self.chat_session_id:
            self.parent_message_id = None
            logging.info(f"New chat session ID: {self.chat_session_id}")
        else:
            logging.error("Failed to create a new chat session")

    def send_prompt(self):
        """
        Send the user's prompt, handle the response, and display it in the GUI.
        """
        prompt = self.input_text.get(1.0, tk.END).strip()
        if not prompt:
            return

        thinking_enabled = self.thinking_enabled_var.get()
        search_enabled = self.search_enabled_var.get()

        from session_management import get_request_data
        data = get_request_data(self.chat_session_id, self.parent_message_id, prompt, thinking_enabled, search_enabled)
        logging.info(f"Data to be sent: {data}")
        try:
            from request_handler import send_request
            full_text_content, new_message_id = send_request(self.session, self.url, self.headers, data)
            if new_message_id:
                self.parent_message_id = new_message_id

            question_md = f"**You**: {prompt}\n\n"
            answer_md = f"**Answer**: {full_text_content}\n\n"
            combined_md = question_md + answer_md
            html = markdown2.markdown(combined_md)
            self.output_label.set_html(html)

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            html_error = f"<p>HTTP error occurred: {http_err}</p>"
            self.output_label.set_html(html_error)
        except requests.exceptions.Timeout:
            logging.error("Request timed out.")
            html_timeout = "<p>Request timed out.</p>"
            self.output_label.set_html(html_timeout)
        except Exception as err:
            logging.error(f"Other error occurred: {err}")
            html_other = f"<p>Other error occurred: {err}</p>"
            self.output_label.set_html(html_other)

    def new_conversation(self):
        """
        Start a new conversation by generating a new chat session and clearing the input and output.
        """
        self.generate_new_chat_session()
        html_new_conversation = "<p>Starting a new conversation</p>"
        self.output_label.set_html(html_new_conversation)
        self.input_text.delete(1.0, tk.END)