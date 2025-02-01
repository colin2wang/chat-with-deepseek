import json
import time
import logging  # 添加 logging 导入语句
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def send_request(session, url, headers, data):
    """
    Send a POST request to the specified URL and handle the response.

    :param session: The requests.Session object.
    :param url: The URL to send the request to.
    :param headers: Headers for the request.
    :param data: Data to be sent in the request body.
    :return: Full text content and new message ID.
    """
    logging.info(f"Sending POST request to {url}, prompt: {data['prompt']}...")
    start_time = time.time()
    response = session.post(url, headers=headers, json=data, stream=True, timeout=30)
    response.raise_for_status()
    full_text_content = ""
    thinking_content = ""
    new_message_id = None
    for line in response.iter_lines():
        if line:
            try:
                line = line.decode('utf-8').replace('data: ', '')
                logging.debug(f"Data: {line}")
                data = json.loads(line)
                choices = data.get('choices', [])
                if choices:
                    delta = choices[0].get('delta', {})
                    content = delta.get('content', "")
                    content_type = delta.get('type', "")
                    if content_type == 'text':
                        full_text_content += content
                        logging.debug(f"Text: {content}")
                    elif content_type == 'thinking':
                        thinking_content += content
                        logging.debug(f"Thinking content: {content}")
                new_message_id = data.get('message_id')
            except json.JSONDecodeError:
                logging.debug(f"Failed to decode line: {line}")
    end_time = time.time()
    response_time = end_time - start_time
    logging.info(f"Request completed in {response_time:.2f} seconds.")
    logging.info(f"Full text content: {full_text_content}")
    logging.info(f"Thinking content: {thinking_content}")
    return full_text_content, new_message_id