import os
import json
import requests
import threading

import time
from openai import (
    OpenAI,
    RateLimitError,
    OpenAIError,
    AuthenticationError,
    APIConnectionError,
)
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class BaseLLM(ABC):
    @abstractmethod
    def chat(self, *args, **kwargs) -> str:
        """Chat through LLMs."""
        pass


class OpenAILLM(BaseLLM):
    def __init__(self):
        self._api_keys = self._load_api_keys()
        self._key_usage = {
            key: {"count": 0, "cooldown": None} for key in self._api_keys
        }
        self._lock = threading.Lock()

    def _load_api_keys(self):
        api_keys = []
        index = 1
        while key := os.getenv(f"OPENAI_API_KEY_{index}"):
            api_keys.append(key)
            index += 1

        if not api_keys:
            raise ValueError("No OPENAI_API_KEY environment variables set.")

        return api_keys

    @property
    def api_key(self):
        # Use the least used key
        with self._lock:
            sorted_keys = sorted(
                self._api_keys, key=lambda k: self._key_usage[k]["count"]
            )
            for key in sorted_keys:
                if (
                    self._key_usage[key]["cooldown"] is None
                    or datetime.now() > self._key_usage[key]["cooldown"]
                ):
                    self._key_usage[key]["count"] += 1
                    return key

    def _reset_key_usage(self, key):
        with self._lock:
            self._key_usage[key]["count"] = 0
            self._key_usage[key]["cooldown"] = datetime.now() + timedelta(minutes=1)

    def _get_key_index(self, key):
        for index, stored_key in enumerate(self._api_keys, 1):
            if stored_key == key:
                return index
        return None

    def chat(self, model, messages, **kwargs):
        max_response_tokens = kwargs.get("max_response_tokens", 3500)
        temperature = kwargs.get("temperature", 0.3)

        for _ in range(len(self._api_keys)):
            retry_count = 0  # Initialize retry count for each key
            timeout = int(os.getenv("OPENAI_REQUEST_TIMEOUT", default="60"))
            while retry_count < 3:
                try:
                    client = OpenAI(api_key=self.api_key)
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages,
                        max_tokens=max_response_tokens,
                        temperature=temperature,
                        timeout=timeout,
                    )
                    chat_message = response.choices[0].message.content
                    print(
                        f"Prompt Tokens: {response.usage.prompt_tokens}, Completion Tokens: {response.usage.completion_tokens}, Total Tokens: {response.usage.total_tokens}"
                    )
                    client.close()
                    return chat_message

                except RateLimitError as e:
                    print(f"Rate limit exhausted Key {self.api_key}")
                    self._reset_key_usage(self.api_key)
                    print(
                        f"An error occurred for {self.api_key}: {str(e)}. Retrying..."
                    )
                    retry_count += 1
                    if retry_count < 3:  # Apply delay only if there are more retries
                        time.sleep(3)  # Adding 3000ms  delay between retries
                    if retry_count == 3:  # If max retries reached for this key
                        print(
                            f"Max retries reached for key index: {self._get_key_index(self.api_key)}"
                        )
                    break  # Move on to the next key

                except OpenAIError as e:
                    if e.code == "insufficient_quota":
                        print(f"Insufficient Quota : {self.api_key}")
                        print(
                            "You exceeded your quota. Please check your plan and billing details."
                        )
                    else:
                        print(f"OpenAI API Error Key Name : {self.api_key}")
                        print(f"OpenAI API Error: {e}")
                    break

                except AuthenticationError as e:
                    print(f"Authentication failed: {self.api_key}")
                    break

                except APIConnectionError as e:
                    print(f"API connection error: {self.api_key}")
                    break

                except Exception as e:
                    print(
                        f"An error occurred for {self.api_key}: {str(e)}. Retrying..."
                    )
                    retry_count += 1
                    if retry_count < 3:  # Apply delay only if there are more retries
                        time.sleep(3)  # Adding 3000ms delay between retries
                    if retry_count == 3:  # If max retries reached for this key
                        print(
                            f"Max retries reached for key index: {self._get_key_index(self.api_key)}"
                        )
                        break  # Exit the retry loop and try with the next key

        raise Exception(
            "All API keys exhausted or maximum retries reached. Try again later."
        )


class LlamaLLM(BaseLLM):
    def __init__(self):
        self._api_key = None
        self._serverless_api_key = None

    @property
    def api_key(self):
        if self._api_key is None:
            self._api_key = os.getenv("RUNPOD_API_KEY")
            if self._api_key is None:
                raise ValueError("RUNPOD_API_KEY environment variable not set.")
        return self._api_key

    @property
    def serverless_api_key(self):
        if self._serverless_api_key is None:
            self._serverless_api_key = os.getenv("SERVERLESS_API_KEY")
            if self._serverless_api_key is None:
                raise ValueError("SERVERLESS_API_KEY environment variable not set.")
        return self._serverless_api_key

    def chat(self, prompt):
        """Chat using Llama LLM."""

        data = {
            "input": {
                "prompt": prompt,
                "max_new_tokens": 2000,
                "temperature": 0.9,
                "top_k": 50,
                "top_p": 0.7,
                "repetition_penalty": 1.2,
                "batch_size": 8,
                "stop": ["</s>"],
            }
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        response = requests.post(
            f"https://api.runpod.ai/v2/{self.serverless_api_key}/runsync",
            data=json.dumps(data),
            headers=headers,
        )
        response.raise_for_status()  # Check if request was successful

        result = response.json()["output"].strip()
        return result.split("[/INST]")[-1].strip()
