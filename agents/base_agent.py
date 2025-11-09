"""
Base Agent class for all agents in the system
"""
from openai import OpenAI
from typing import Dict, Any, Optional
import config


class BaseAgent:
    """Base class for all agents in the multi-agent system"""
    
    def __init__(self, name: str, role: str, instructions: str):
        """
        Initialize the base agent
        
        Args:
            name: Name of the agent
            role: Role/specialty of the agent
            instructions: System instructions for the agent
        """
        self.name = name
        self.role = role
        self.instructions = instructions
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.OPENAI_MODEL
        
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Execute a task using the agent with timeout protection
        
        Args:
            task: The task description
            context: Additional context for the task
            
        Returns:
            The agent's response
        """
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": task}
        ]
        
        if context:
            context_str = "\n\nContext:\n" + "\n".join([f"{k}: {v}" for k, v in context.items()])
            messages[1]["content"] += context_str
        
        try:
            # Add timeout to API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                timeout=config.API_CALL_TIMEOUT_SECONDS
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                return f"Error: API call timed out after {config.API_CALL_TIMEOUT_SECONDS} seconds"
            return f"Error executing task: {error_msg}"
    
    def __str__(self):
        return f"{self.name} ({self.role})"

