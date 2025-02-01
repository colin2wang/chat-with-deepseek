import logging
import requests


def create_chat_session(session, headers):
    """
    Create a chat session and retrieve the chat_session_id.

    :param session: The requests.Session object.
    :param headers: Headers for the request.
    :return: chat_session_id if successful, None otherwise.
    """
    url = "https://chat.deepseek.com/api/v0/chat_session/create"
    data = {"character_id": None}
    try:
        response = session.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        chat_session_id = result.get("data", {}).get("biz_data", {}).get("id")
        if chat_session_id:
            logging.info(f"Successfully obtained chat_session_id: {chat_session_id}")
            return chat_session_id
        else:
            logging.error("Failed to obtain chat_session_id from the response")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error occurred while creating chat session: {e}")
    return None


def get_request_data(chat_session_id, parent_message_id, prompt, thinking_enabled, search_enabled):
    """
    Generate the request data for the chat completion.

    :param chat_session_id: ID of the chat session.
    :param parent_message_id: ID of the parent message.
    :param prompt: The user's prompt.
    :param thinking_enabled: Whether thinking is enabled.
    :param search_enabled: Whether search is enabled.
    :return: Request data as a dictionary.
    """
    return {
        "chat_session_id": chat_session_id,
        "parent_message_id": parent_message_id,
        "prompt": prompt,
        "ref_file_ids": [],
        "thinking_enabled": thinking_enabled,
        "search_enabled": search_enabled
    }
