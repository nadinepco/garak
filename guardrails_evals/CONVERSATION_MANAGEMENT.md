# Conversation Management Implementation

## Overview
Added automatic conversation lifecycle management to RestGenerator. The generator now creates a new conversation for each probe, sends the message, and automatically deletes the conversation afterward.

## Changes Made

### 1. New Configuration Parameters

Added to `DEFAULT_PARAMS` in `garak/generators/rest.py`:

- **`conversation_base_uri`** (str, default: None)
  - Base API URL (e.g., `http://localhost:8000`)

- **`conversation_create_endpoint`** (str, default: None)
  - Endpoint to create conversations (e.g., `/conversations`)

- **`conversation_delete_endpoint`** (str, default: None)
  - Endpoint to delete conversations (e.g., `/conversations/{conversation_id}`)

- **`conversation_message_endpoint`** (str, default: None)
  - Endpoint template for sending messages (e.g., `/conversations/{conversation_id}/messages/v2`)

### 2. Automatic Mode Detection

Conversation management is **automatically enabled** when all four conversation parameters are set:
- If all four are present → Conversation management mode
- If any are missing → Traditional static URI mode (backward compatible)

### 3. New Methods

#### `_create_conversation()`
- Creates a new conversation via POST request
- Returns the conversation_id
- Raises ConnectionError on failure

#### `_delete_conversation(conversation_id)`
- Deletes a conversation via DELETE request
- Returns True/False based on success
- Logs warnings on failure (non-blocking)

### 4. Modified `_call_model()` Flow

**With conversation management:**
1. Create new conversation → get `conversation_id`
2. Build dynamic URI: `{base_uri}{message_endpoint.replace('{conversation_id}', id)}`
3. Send message and process streaming response
4. Delete conversation (cleanup)

**Cleanup occurs:**
- After successful response
- On errors (4xx, 5xx)
- On skip codes
- On rate limits

**Without conversation management:**
- Uses static `uri` from config (original behavior)

### 5. Added `$UUID` Placeholder Support

The `_populate_template()` method now supports:
- `$KEY` - API key from environment variable
- `$INPUT` - The prompt text
- `$UUID` - Auto-generated UUID (new UUID per call)

## Configuration Examples

### With Conversation Management (New)

```json
{
    "rest": {
        "RestGenerator": {
            "name": "Pharia Chat API",
            "method": "post",
            "key_env_var": "PHARIA_TOKEN",
            "headers": {
                "Content-Type": "application/json",
                "X-PHARIA-USER": "$KEY"
            },
            "req_template_json_object": {
                "content": "$INPUT",
                "collections": [],
                "server_ids": [],
                "think": true,
                "message_id": "$UUID"
            },
            "send_raw_json": true,
            "response_streaming": true,
            "stream_event_filter": "message_inserted",
            "stream_role_filter": "assistant",
            "stream_content_field": "content",
            "accumulate_stream": false,
            "request_timeout": 60,
            "conversation_base_uri": "http://localhost:8000",
            "conversation_create_endpoint": "/conversations",
            "conversation_delete_endpoint": "/conversations/{conversation_id}",
            "conversation_message_endpoint": "/conversations/{conversation_id}/messages/v2"
        }
    }
}
```

### Without Conversation Management (Legacy)

```json
{
    "rest": {
        "RestGenerator": {
            "name": "Example API",
            "uri": "http://localhost:8000/conversations/STATIC_ID/messages/v2",
            "method": "post",
            "headers": {
                "Content-Type": "application/json"
            },
            "req_template_json_object": {
                "content": "$INPUT"
            },
            "send_raw_json": true,
            "response_streaming": true,
            "stream_event_filter": "message_inserted",
            "stream_role_filter": "assistant",
            "stream_content_field": "content"
        }
    }
}
```

## Benefits

1. **Isolation**: Each probe runs in a fresh conversation
2. **No History Pollution**: Previous messages don't affect new tests
3. **Automatic Cleanup**: Conversations are deleted after each test
4. **Backward Compatible**: Existing configs without conversation params still work
5. **Flexible**: Works with any REST API that follows create/message/delete pattern

## Usage

```bash
# Make sure PHARIA_TOKEN is set
export PHARIA_TOKEN="your-token"

# Run garak with conversation management
uv run python -m garak \
  --target_type rest \
  -G tools/rest/streaming_config.json \
  --probes probes.test.Blank
```

## How It Works

1. **Probe starts** → garak calls `generator._call_model(prompt)`
2. **Create** → POST `/conversations` → returns `conversation_id`
3. **Build URI** → `http://localhost:8000/conversations/{conversation_id}/messages/v2`
4. **Send message** → POST with streaming, extract assistant response
5. **Cleanup** → DELETE `/conversations/{conversation_id}`
6. **Repeat** for each probe

## Files Modified

1. `garak/generators/rest.py`
   - Added conversation management parameters
   - Added `_create_conversation()` and `_delete_conversation()` methods
   - Modified `__init__()` to detect conversation management mode
   - Modified `_call_model()` to handle dynamic URIs and cleanup
   - Added `$UUID` placeholder support

2. `tools/rest/streaming_config.json`
   - Updated with conversation management parameters
   - Removed static `uri` field
   - Added conversation endpoints

## Testing

The implementation has been tested with:
- Conversation creation/deletion
- Dynamic URI building
- UUID generation per request
- Cleanup on success and failure paths
- Backward compatibility with static URIs
