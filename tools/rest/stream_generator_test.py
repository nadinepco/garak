#!/usr/bin/env python3
"""
Script to create a new conversation and conduct a multi-turn chat with the agent.

Usage:
    python manual_test_multi_turn_chat.py [--keep-conversation] [--api-url URL] [--user-id ID] [--message "Your message"]

Options:
    --keep-conversation    Don't delete the conversation after the test (for debugging)
    --api-url URL          API base URL (default: from env or http://localhost:8000)
    --user-id ID           User ID to use (default: from env or "system")
    --message "Message"    Add a custom message to the conversation (can be used multiple times)
"""

from typing import Any
import uuid
import requests
import json
import os
import time
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Test multi-turn conversation with the agent"
)
parser.add_argument(
    "--keep-conversation",
    action="store_true",
    default=os.getenv("PHARIA_CHAT_KEEP_CONVERSATION", "true"),
    help="Don't delete the conversation after the test (for debugging)",
)
parser.add_argument(
    "--api-url",
    default=os.getenv("API_BASE_URL", "http://localhost:8000"),
    help="API base URL (default: from env or http://localhost:8000)",
)
parser.add_argument(
    "--user-id",
    default=os.getenv("TEST_USER_ID", "system"),
    help="User ID to use (default: from env or 'system')",
)
parser.add_argument(
    "--message",
    action="append",
    help="Add a custom message to the conversation (can be used multiple times)",
)

args = parser.parse_args()

# Configuration
API_BASE_URL = args.api_url
USER_ID = args.user_id

# Headers
headers = {"Content-Type": "application/json", "X-PHARIA-USER": USER_ID}

# Messages for the multi-turn conversation
default_messages = [
    "What is the weather today in Berlin Germany? 1111",
    "Can you calculate 345 * 678 for me?",
    "Translate 'Hello, how are you?' to German.",
    "What's the weather in Paris?",
    "Summarize your last output",
]

# Use custom messages if provided, otherwise use defaults
messages = args.message if args.message else default_messages


def create_conversation() -> Any:
    """Create a new conversation and return its ID."""
    url = f"{API_BASE_URL}/conversations"
    params: dict[str, Any] = {}  # Removed the name parameter to let the backend use None as default

    try:
        response = requests.post(url, params=params, headers=headers)
        response.raise_for_status()
        conversation_id = response.json()
        print(f"Created new conversation with ID: {conversation_id}")
        return conversation_id
    except requests.exceptions.RequestException as e:
        print(f"Error creating conversation: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        exit(1)


def get_conversation_details(conversation_id: str) -> Any | None:
    """Fetch conversation details including its current name."""
    url = f"{API_BASE_URL}/conversations/{conversation_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        conversation_details = response.json()
        return conversation_details
    except requests.exceptions.RequestException as e:
        print(f"Error fetching conversation details: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None


def send_message(conversation_id: str, message_content: str, parent_message_id: str|None = None) -> str|None:
    """Send a message to the conversation and return the agent's response message ID."""
    url = f"{API_BASE_URL}/conversations/{conversation_id}/messages/v2"

    message_data = {"content": message_content, "message_id": str(uuid.uuid4())}
    if parent_message_id:
        message_data["parent_message_id"] = parent_message_id

    message_data["think"] = False

    agent_message_id = None
    user_message_id = None

    try:
        print(f"\n--- SENDING MESSAGE: {message_content} ---")
        if parent_message_id:
            print(f"Parent message ID: {parent_message_id}")

        with requests.post(
            url, json=message_data, headers=headers, stream=True
        ) as response:
            response.raise_for_status()

            print("\nReceiving streaming response:")
            # Process the SSE streaming response line by line
            current_event = None
            for line in response.iter_lines():
                if not line:
                    continue

                try:
                    decoded_line = line.decode("utf-8")

                    # Skip empty lines and comments
                    if not decoded_line.strip() or decoded_line.startswith(":"):
                        continue

                    # Parse SSE format: "event: type" or "data: json"
                    if decoded_line.startswith("event: "):
                        current_event = decoded_line[7:]
                    elif decoded_line.startswith("data: "):
                        try:
                            json_str = decoded_line[6:]
                            json_obj = json.loads(json_str)

                            if current_event == "tool":
                                if json_obj.get("content"):
                                    print("Tool call:", json_obj.get("content"))

                            if current_event == "message_inserted":
                                if json_obj.get("role") == "user":
                                    user_message_id = json_obj.get("insertion_id")
                                    print(f"User message ID: {user_message_id}")
                                elif json_obj.get("role") == "assistant":
                                    agent_message_id = json_obj.get("insertion_id")
                                    print("=" * 10)
                                    print("Assistant message:", json_obj.get("content"))
                                    print(f"Agent message ID: {agent_message_id}")

                            # # Pretty print the JSON to stdout
                            # print(json.dumps(json_obj, indent=2))
                        except json.JSONDecodeError:
                            print(f"Could not parse JSON data: {json_str}")

                except Exception as e:
                    print(f"Error processing stream line: {line}: {e}")

            print("\nMessage exchange completed.")

        return agent_message_id or user_message_id

    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return None


def delete_conversation(conversation_id: str) -> bool:
    """Delete a conversation."""
    url = f"{API_BASE_URL}/conversations/{conversation_id}"

    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        print(f"Deleted conversation with ID: {conversation_id}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error deleting conversation: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return False


def main() -> None:
    # Create a new conversation
    conversation_id = create_conversation()

    # Store initial conversation details
    initial_details = get_conversation_details(conversation_id)
    initial_name = (
        initial_details.get("name", "Unknown") if initial_details else "Unknown"
    )
    print(f"Initial conversation name: '{initial_name}'")

    # Initialize parent_message_id as None for the first message
    parent_message_id = None

    try:
        # Conduct a multi-turn conversation
        for i, message in enumerate(messages):
            print(f"\n=== TURN {i + 1} OF {len(messages)} ===")

            # Send message and get the response message ID
            response_message_id = send_message(
                conversation_id, message, parent_message_id
            )

            if not response_message_id:
                print(f"Failed to get response for message: {message}")
                break

            # Use the current response as the parent for the next message
            parent_message_id = response_message_id

            # Add a small delay between turns to avoid rate limiting
            if i < len(messages) - 1:
                time.sleep(0.1)

        # Get the current conversation details after all turns
        conversation_details = get_conversation_details(conversation_id)
        if conversation_details and "name" in conversation_details:
            conversation_name = (
                conversation_details["name"] or "None"
            )  # Handle None value
            print("\nMulti-turn conversation completed successfully!")
            print(f"Final conversation name: '{conversation_name}'")

            # Check if name changed
            if conversation_name != initial_name:
                print(
                    f"Conversation name was updated by summarizer (from '{initial_name or 'None'}' to '{conversation_name}')"
                )
            else:
                print("Conversation name was NOT updated by summarizer")
        else:
            print("\nMulti-turn conversation completed successfully!")
            print("Unable to retrieve current conversation name")

    finally:
        # Clean up by deleting the conversation unless --keep-conversation was specified
        if not args.keep_conversation:
            print("\nCleaning up...")
            delete_conversation(conversation_id)
        else:
            # Get the current conversation details if we haven't already
            if not conversation_details:
                conversation_details = get_conversation_details(conversation_id)

            conversation_name = (
                conversation_details.get("name", "Unknown")
                if conversation_details
                else "Unknown"
            )
            conversation_name = conversation_name or "None"  # Handle None value
            print(
                f"\nKeeping conversation '{conversation_name}' (ID: {conversation_id}) for debugging (--keep-conversation flag was used)"
            )


if __name__ == "__main__":
    main()
