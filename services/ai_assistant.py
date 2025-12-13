"""
AIAssistant service class for the Multi-Domain Intelligence Platform.
Wraps AI/chat functionality using Google's Generative AI (Gemini).
"""

import google.generativeai as genai
from typing import List, Dict, Optional


class AIAssistant:
    """Manages AI chat interactions using Google's Gemini model.

    This service provides a clean interface for AI-powered chat functionality,
    including conversation history management and domain-specific prompts.
    """

    def __init__(self, api_key: str, model_name: str = "models/gemini-2.5-flash",
                 system_prompt: str = "You are a helpful assistant."):
        """Initialize the AI Assistant.

        Args:
            api_key: Google Generative AI API key
            model_name: Name of the Gemini model to use
            system_prompt: Initial system prompt for the assistant
        """
        self._api_key = api_key
        self._model_name = model_name
        self._system_prompt = system_prompt
        self._history: List[Dict[str, str]] = []
        self._model = None

        # Configure the API
        self._configure_api()

    def _configure_api(self) -> None:
        """Configure the Google Generative AI API with the provided key."""
        try:
            genai.configure(api_key=self._api_key)
            self._model = genai.GenerativeModel(self._model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to configure AI API: {str(e)}")

    def set_system_prompt(self, prompt: str) -> None:
        """Update the system prompt for the assistant.

        Args:
            prompt: New system prompt text
        """
        self._system_prompt = prompt

    def get_system_prompt(self) -> str:
        """Get the current system prompt.

        Returns:
            str: Current system prompt
        """
        return self._system_prompt

    def send_message(self, user_message: str) -> str:
        """Send a message to the AI and get a response.

        Args:
            user_message: User's message text

        Returns:
            str: AI assistant's response

        Raises:
            RuntimeError: If the API call fails
        """
        if self._model is None:
            raise RuntimeError("AI model not initialized. Check API configuration.")

        # Add user message to history
        self._history.append({"role": "user", "content": user_message})

        try:
            # Create chat and send message with system prompt
            chat = self._model.start_chat()
            full_prompt = f"{self._system_prompt}\nUser: {user_message}"
            response = chat.send_message(full_prompt)

            # Extract response text
            reply = response.text

            # Add assistant response to history
            self._history.append({"role": "assistant", "content": reply})

            return reply

        except Exception as e:
            error_msg = f"AI Error: {str(e)}"
            self._history.append({"role": "assistant", "content": error_msg})
            raise RuntimeError(error_msg)

    def get_history(self) -> List[Dict[str, str]]:
        """Get the conversation history.

        Returns:
            List[Dict[str, str]]: List of message dictionaries
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self._history.clear()

    def get_domain_prompt(self, domain: str) -> str:
        """Get a pre-defined system prompt for a specific domain.

        Args:
            domain: Domain name (e.g., "Cybersecurity", "Data Science")

        Returns:
            str: Domain-specific system prompt
        """
        domain_prompts = {
            "cybersecurity": "You are a cybersecurity expert. Provide clear, actionable advice on security incidents, threats, and best practices. Explain technical concepts in simple terms.",
            "data science": "You are a data analyst expert. Help users understand datasets, provide insights on data analysis, and explain data science concepts clearly.",
            "it operations": "You are an IT operations specialist. Provide practical guidance on IT tickets, troubleshooting, and system administration. Keep explanations simple and actionable.",
            "general": "You are a helpful assistant for a multi-domain intelligence platform. Provide clear, concise answers and practical advice."
        }

        return domain_prompts.get(domain.lower(), domain_prompts["general"])

    def set_domain(self, domain: str) -> None:
        """Set the assistant's domain and update the system prompt accordingly.

        Args:
            domain: Domain name to set
        """
        prompt = self.get_domain_prompt(domain)
        self.set_system_prompt(prompt)

    def __str__(self) -> str:
        """Return a string representation of the assistant."""
        return f"AIAssistant(model='{self._model_name}', messages={len(self._history)})"