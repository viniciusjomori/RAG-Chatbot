from dataclasses import dataclass, field
from pydantic_ai.messages import ModelRequest, ModelResponse, UserPromptPart, TextPart
from src.util import time

@dataclass
class GraphState:
    _question: str = field(default_factory=str)
    _answer: str = field(default_factory=str)
    messages: list = field(default_factory=list)

    @property
    def question(self):
        return self._question
    
    @question.setter
    def question(self, question):
        self.add_request(question)
        self._question = question

    @property
    def answer(self):
        return self._answer
    
    @answer.setter
    def answer(self, answer):
        self.add_response(answer)
        self._answer = answer

    def add_request(self, message):
        request = ModelRequest(
            parts=[UserPromptPart(
                content=message,
                timestamp=time.now()
            )]
        )
        
        self.messages.append(request)

    def add_response(self, message):
        response = ModelResponse(
            parts=[TextPart(content=message)],
            timestamp=time.now()
        )
        
        self.messages.append(response)





