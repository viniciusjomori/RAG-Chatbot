from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_graph import BaseNode, GraphRunContext

from src.graph.nodes.generate import GenerateNode
from src.database.chroma import ChromaRepository
from src.graph.state import GraphState
from src.util import time

class Prepare(BaseModel):
    query: str = Field(description="Duvida resumoda", max_length=50)

prepare_agent = Agent(
    'openai:gpt-3.5-turbo',
    system_prompt=(
        "Baseado nas mensagens anteriores e na pergunta feita,"
        " elabore uma pergunta simples que resuma a duvida"
        " baseado no contexto"
    ),
    result_type=Prepare
)

@dataclass
class RetrieveNode(BaseNode[GraphState]):

    async def run(self, ctx: GraphRunContext[GraphState, ChromaRepository]) -> GenerateNode:
        print(f'-- [{time.now()}] Retrieve--')
        
        question = ctx.state.question
        messages = ctx.state.messages

        result = await prepare_agent.run(f'Pergunta: {question}', message_history=messages)
        query = result.data.query
        print(f"-- [{time.now()}] query for chroma: ", query, "--")

        context = ctx.deps.retrieve(query, 10)

        return GenerateNode(query, context)