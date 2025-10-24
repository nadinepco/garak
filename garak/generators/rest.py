# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""REST API generator interface

Generic Module for REST API connections
"""

import json
import logging
import uuid
from typing import List, Union
import requests

import backoff
import jsonpath_ng
from jsonpath_ng.exceptions import JsonPathParserError

from garak import _config
from garak.attempt import Message, Conversation
from garak.exception import (
    APIKeyMissingError,
    BadGeneratorException,
    RateLimitHit,
    GarakBackoffTrigger,
)
from garak.generators.base import Generator


class RestGenerator(Generator):
    """Generic API interface for REST models

    See reference docs for details (https://reference.garak.ai/en/latest/garak.generators.rest.html)
    """

    DEFAULT_PARAMS = Generator.DEFAULT_PARAMS | {
        "headers": {},
        "method": "post",
        "ratelimit_codes": [429],
        "skip_codes": [],
        "response_json": False,
        "response_json_field": None,
        "req_template": "$INPUT",
        "request_timeout": 20,
        "proxies": None,
        "verify_ssl": True,
        "response_streaming": False,
        "stream_event_filter": None,
        "stream_role_filter": None,
        "stream_content_field": "content",
        "accumulate_stream": False,
        "send_raw_json": False,
        "conversation_create_endpoint": None,
        "conversation_delete_endpoint": None,
        "conversation_base_uri": None,
        "conversation_message_endpoint": None,
    }

    ENV_VAR = "REST_API_KEY"
    generator_family_name = "REST"

    _supported_params = (
        "api_key",
        "name",
        "uri",
        "key_env_var",
        "req_template",
        "req_template_json",
        "context_len",
        "max_tokens",
        "method",
        "headers",
        "response_json",
        "response_json_field",
        "req_template_json_object",
        "request_timeout",
        "ratelimit_codes",
        "skip_codes",
        "skip_seq_start",
        "skip_seq_end",
        "temperature",
        "top_k",
        "proxies",
        "verify_ssl",
        "response_streaming",
        "stream_event_filter",
        "stream_role_filter",
        "stream_content_field",
        "accumulate_stream",
        "send_raw_json",
        "conversation_create_endpoint",
        "conversation_delete_endpoint",
        "conversation_base_uri",
        "conversation_message_endpoint",
    )

    def __init__(self, uri=None, config_root=_config):
        self.uri = uri
        self.name = uri
        self.supports_multiple_generations = False  # not implemented yet
        self.escape_function = self._json_escape
        self.retry_5xx = True
        self.key_env_var = self.ENV_VAR if hasattr(self, "ENV_VAR") else None

        # load configuration since super.__init__ has not been called
        self._load_config(config_root)

        if (
            hasattr(self, "req_template_json_object")
            and self.req_template_json_object is not None
        ):
            self.req_template = json.dumps(self.req_template_json_object)

        if self.response_json:
            if self.response_json_field is None:
                raise ValueError(
                    "RestGenerator response_json is True but response_json_field isn't set"
                )
            if not isinstance(self.response_json_field, str):
                raise ValueError("response_json_field must be a string")
            if self.response_json_field == "":
                raise ValueError(
                    "RestGenerator response_json is True but response_json_field is an empty string. If the root object is the target object, use a JSONPath."
                )

        # Check if conversation management is enabled
        self.conversation_management_enabled = (
            self.conversation_create_endpoint is not None
            and self.conversation_delete_endpoint is not None
            and self.conversation_base_uri is not None
            and self.conversation_message_endpoint is not None
        )

        if self.conversation_management_enabled:
            logging.info("Conversation management enabled - will create/delete conversations automatically")
            self.conversation_id = None  # Will be set per request
            # Use conversation_base_uri as the name if uri is not set
            if self.name is None:
                self.name = self.conversation_base_uri
        else:
            # Traditional mode - static URI
            if self.name is None:
                self.name = self.uri

            if self.uri is None:
                raise ValueError(
                    "No REST endpoint URI definition found in either constructor param, JSON, or --target_name. Please specify one."
                )

        self.fullname = f"{self.generator_family_name} {self.name}"

        self.method = self.method.lower()
        if self.method not in (
            "get",
            "post",
            "put",
            "patch",
            "options",
            "delete",
            "head",
        ):
            logging.info(
                "RestGenerator HTTP method %s not supported, defaulting to 'post'",
                self.method,
            )
            self.method = "post"
        self.http_function = getattr(requests, self.method)

        # validate proxies formatting
        # sanity check only leave actual parsing of values to the `requests` library on call.
        if hasattr(self, "proxies") and self.proxies is not None:
            if not isinstance(self.proxies, dict):
                raise BadGeneratorException(
                    "`proxies` value provided is not in the required format. See documentation from the `requests` package for details on expected format. https://requests.readthedocs.io/en/latest/user/advanced/#proxies"
                )

        # suppress warnings about intentional SSL validation suppression
        if isinstance(self.verify_ssl, bool) and not self.verify_ssl:
            requests.packages.urllib3.disable_warnings()

        # validate jsonpath
        if self.response_json and self.response_json_field:
            try:
                self.json_expr = jsonpath_ng.parse(self.response_json_field)
            except JsonPathParserError as e:
                logging.critical(
                    "Couldn't parse response_json_field %s", self.response_json_field
                )
                raise e

        super().__init__(self.name, config_root=config_root)

    def _validate_env_var(self):
        key_match = "$KEY"
        header_requires_key = False
        for _k, v in self.headers.items():
            if key_match in v:
                header_requires_key = True
        if "$KEY" in self.req_template or header_requires_key:
            return super()._validate_env_var()

    def _json_escape(self, text: str) -> str:
        """JSON escape a string"""
        # trim first & last "
        return json.dumps(text)[1:-1]

    def _populate_template(
        self, template: str, text: str, json_escape_key: bool = False
    ) -> str:
        """Replace template placeholders with values

        Interesting values are:
        * $KEY - the API key set as an object variable
        * $INPUT - the prompt text
        * $UUID - a randomly generated UUID (new UUID for each call)

        $KEY is only set if the relevant environment variable is set; the
        default variable name is REST_API_KEY but this can be overridden.
        """
        output = template
        if "$KEY" in template:
            if self.api_key is None:
                raise APIKeyMissingError(
                    f"Template requires an API key but {self.key_env_var} env var isn't set"
                )
            if json_escape_key:
                output = output.replace("$KEY", self.escape_function(self.api_key))
            else:
                output = output.replace("$KEY", self.api_key)

        # Replace $UUID with a new UUID
        if "$UUID" in output:
            output = output.replace("$UUID", str(uuid.uuid4()))

        return output.replace("$INPUT", self.escape_function(text))

    def _handle_streaming_response(
        self, resp: requests.Response
    ) -> List[Union[Message, None]]:
        """Handle Server-Sent Events (SSE) streaming responses

        Processes streaming responses line by line, parsing SSE format with
        'event: <type>' and 'data: <json>' lines. Filters by event type and
        role (if configured), extracts content, and returns the result.

        :param resp: The streaming response object from requests
        :return: List containing a single Message with the accumulated content, or [None] if no content found
        """
        accumulated_content = [] if self.accumulate_stream else None
        current_event = None
        last_content = None

        try:
            for line in resp.iter_lines():
                if not line:
                    continue

                try:
                    decoded_line = line.decode("utf-8")

                    # Skip empty lines and comments
                    if not decoded_line.strip() or decoded_line.startswith(":"):
                        continue

                    # Parse SSE format: "event: type" or "data: json"
                    if decoded_line.startswith("event: "):
                        current_event = decoded_line[7:].strip()
                    elif decoded_line.startswith("data: "):
                        json_str = decoded_line[6:]

                        # Check for stream termination signal
                        if json_str.strip() == "[DONE]":
                            break

                        try:
                            json_obj = json.loads(json_str)

                            # Apply event type filter if configured
                            if self.stream_event_filter and current_event != self.stream_event_filter:
                                continue

                            # Apply role filter if configured
                            if self.stream_role_filter:
                                role = json_obj.get("role")
                                if role != self.stream_role_filter:
                                    continue

                            # Extract content from the configured field
                            content = json_obj.get(self.stream_content_field)
                            if content:
                                if self.accumulate_stream:
                                    accumulated_content.append(content)
                                else:
                                    last_content = content

                        except json.JSONDecodeError as jde:
                            logging.warning(
                                "Could not parse JSON in streaming data: %s",
                                json_str,
                                exc_info=jde,
                            )
                            continue

                except UnicodeDecodeError as ude:
                    logging.warning(
                        "Could not decode streaming line: %s", line, exc_info=ude
                    )
                    continue

        except Exception as e:
            logging.error(
                "Error processing streaming response from %s", self.uri, exc_info=e
            )
            return [None]

        # Return accumulated or last content
        if self.accumulate_stream:
            if accumulated_content:
                return [Message(text="".join(accumulated_content))]
        else:
            if last_content is not None:
                return [Message(text=str(last_content))]

        # No content found
        logging.warning("No content extracted from streaming response from %s", self.uri)
        return [None]

    def _get_populated_headers(self) -> dict:
        """Get headers with $KEY placeholder replaced by actual API key.

        :return: Dictionary of headers with placeholders populated
        :raises: APIKeyMissingError if $KEY is in headers but api_key is not set
        """
        request_headers = dict(self.headers)
        for k, v in self.headers.items():
            if "$KEY" in v:
                if self.api_key is None:
                    raise APIKeyMissingError(
                        f"Header requires an API key but {self.key_env_var} env var isn't set"
                    )
                request_headers[k] = v.replace("$KEY", self.api_key)
        return request_headers

    def _create_conversation(self) -> str:
        """Create a new conversation and return its ID.

        :return: The conversation ID as a string
        :raises: ConnectionError if conversation creation fails
        """
        url = f"{self.conversation_base_uri}{self.conversation_create_endpoint}"
        request_headers = self._get_populated_headers()

        try:
            logging.debug(f"Creating conversation at {url}")
            logging.debug(f"Headers: {request_headers}")
            resp = requests.post(
                url,
                headers=request_headers,
                timeout=self.request_timeout,
                proxies=self.proxies,
                verify=self.verify_ssl,
            )
            resp.raise_for_status()

            # Response should be a conversation ID (string)
            conversation_id = resp.json()
            logging.info(f"Created conversation with ID: {conversation_id}")
            return conversation_id

        except Exception as e:
            logging.error(f"Failed to create conversation: {e}")
            raise ConnectionError(f"Failed to create conversation at {url}: {e}") from e

    def _delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation by ID.

        :param conversation_id: The conversation ID to delete
        :return: True if successful, False otherwise
        """
        if not conversation_id:
            return False

        # Replace {conversation_id} placeholder in endpoint
        endpoint = self.conversation_delete_endpoint.replace("{conversation_id}", conversation_id)
        url = f"{self.conversation_base_uri}{endpoint}"

        try:
            request_headers = self._get_populated_headers()
        except APIKeyMissingError:
            logging.warning("Cannot delete conversation - API key not set")
            return False

        try:
            logging.debug(f"Deleting conversation {conversation_id} at {url}")
            resp = requests.delete(
                url,
                headers=request_headers,
                timeout=self.request_timeout,
                proxies=self.proxies,
                verify=self.verify_ssl,
            )
            resp.raise_for_status()
            logging.info(f"Deleted conversation {conversation_id}")
            return True

        except Exception as e:
            logging.warning(f"Failed to delete conversation {conversation_id}: {e}")
            return False

    @backoff.on_exception(
        backoff.fibo, (RateLimitHit, GarakBackoffTrigger), max_value=70
    )
    def _call_model(
        self, prompt: Conversation, generations_this_call: int = 1
    ) -> List[Union[Message, None]]:
        """Individual call to get a rest from the REST API

        :param prompt: the input to be placed into the request template and sent to the endpoint
        :type prompt: str
        """

        # Handle conversation management if enabled
        if self.conversation_management_enabled:
            # Create a new conversation for this request
            self.conversation_id = self._create_conversation()

            # Build the URI dynamically with the conversation_id
            endpoint = self.conversation_message_endpoint.replace("{conversation_id}", self.conversation_id)
            request_uri = f"{self.conversation_base_uri}{endpoint}"
        else:
            # Use the static URI
            request_uri = self.uri

        # should this support a serialized Conversation?
        request_data = self._populate_template(
            self.req_template, prompt.last_message().text
        )

        request_headers = dict(self.headers)
        for k, v in self.headers.items():
            # why does this provide the prompt to fill out headers?
            request_headers[k] = self._populate_template(v, prompt.last_message().text)

        # the prompt should not be sent via data when using a GET request. Prompt should be
        # serialized as parameters, in general a method could be created to add
        # the prompt data to a request via params or data based on the action verb
        if self.send_raw_json:
            # Send as parsed JSON object (json= parameter in requests)
            data_kw = "params" if self.http_function == requests.get else "json"
            request_data = json.loads(request_data) if isinstance(request_data, str) else request_data
        else:
            # Send as string data (data= parameter in requests)
            data_kw = "params" if self.http_function == requests.get else "data"

        req_kArgs = {
            data_kw: request_data,
            "headers": request_headers,
            "timeout": self.request_timeout,
            "proxies": self.proxies,
            "verify": self.verify_ssl,
            "stream": self.response_streaming,
        }

        # Debug logging
        logging.info("REST Generator Request Details:")
        logging.info(f"  URI: {request_uri}")
        logging.info(f"  Method: {self.method}")
        logging.info(f"  Data keyword: {data_kw}")
        logging.info(f"  Request data: {request_data}")
        logging.info(f"  Headers: {request_headers}")

        try:
            resp = self.http_function(request_uri, **req_kArgs)
        except UnicodeEncodeError as uee:
            # only RFC2616 (latin-1) is guaranteed
            # don't print a repr, this might leak api keys
            logging.error(
                "Only latin-1 encoding supported by HTTP RFC 2616, check headers and values for unusual chars",
                exc_info=uee,
            )
            raise BadGeneratorException from uee

        if resp.status_code in self.skip_codes:
            logging.debug(
                "REST skip prompt: %s - %s, uri: %s",
                resp.status_code,
                resp.reason,
                request_uri,
            )
            # Clean up conversation if enabled
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            return [None]

        if resp.status_code in self.ratelimit_codes:
            # Clean up conversation if enabled
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            raise RateLimitHit(
                f"Rate limited: {resp.status_code} - {resp.reason}, uri: {request_uri}"
            )

        if str(resp.status_code)[0] == "3":
            # Clean up conversation if enabled
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            raise NotImplementedError(
                f"REST URI redirection: {resp.status_code} - {resp.reason}, uri: {request_uri}"
            )

        if str(resp.status_code)[0] == "4":
            # Clean up conversation if enabled
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            raise ConnectionError(
                f"REST URI client error: {resp.status_code} - {resp.reason}, uri: {request_uri}"
            )

        if str(resp.status_code)[0] == "5":
            error_msg = f"REST URI server error: {resp.status_code} - {resp.reason}, uri: {request_uri}"
            # Clean up conversation if enabled
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            if self.retry_5xx:
                raise GarakBackoffTrigger(error_msg)
            raise ConnectionError(error_msg)

        # Handle SSE streaming responses
        if self.response_streaming:
            result = self._handle_streaming_response(resp)
            # Clean up conversation after successful response
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            return result

        if not self.response_json:
            result = [Message(text=str(resp.text))]
            # Clean up conversation after successful response
            if self.conversation_management_enabled and self.conversation_id:
                self._delete_conversation(self.conversation_id)
            return result

        response_object = json.loads(resp.content)

        response = [None]

        # if response_json_field starts with a $, treat is as a JSONPath
        assert (
            self.response_json
        ), "response_json must be True at this point; if False, we should have returned already"
        assert isinstance(
            self.response_json_field, str
        ), "response_json_field must be a string"
        assert (
            len(self.response_json_field) > 0
        ), "response_json_field needs to be complete if response_json is true; ValueError should have been raised in constructor"
        if self.response_json_field[0] != "$":
            if isinstance(response_object, list):
                response = [item[self.response_json_field] for item in response_object]
            else:
                response = [response_object[self.response_json_field]]
        else:
            field_path_expr = jsonpath_ng.parse(self.response_json_field)
            responses = field_path_expr.find(response_object)
            if len(responses) == 1:
                response_value = responses[0].value
                if isinstance(response_value, str):
                    response = [response_value]
                elif isinstance(response_value, list):
                    response = response_value
            elif len(responses) > 1:
                response = [r.value for r in responses]
            else:
                logging.error(
                    "RestGenerator JSONPath in response_json_field yielded nothing. Response content: %s"
                    % repr(resp.content)
                )
                # Clean up conversation if enabled
                if self.conversation_management_enabled and self.conversation_id:
                    self._delete_conversation(self.conversation_id)
                return [None]

        # Clean up conversation after successful response
        if self.conversation_management_enabled and self.conversation_id:
            self._delete_conversation(self.conversation_id)

        # Ensure Message objects are created with string text values
        messages = []
        for r in response:
            if r is None:
                messages.append(None)
            elif isinstance(r, str):
                messages.append(Message(text=r))
            else:
                # Convert non-string values to JSON string
                messages.append(Message(text=json.dumps(r)))
        return messages


DEFAULT_CLASS = "RestGenerator"
