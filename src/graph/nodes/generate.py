from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_graph import BaseNode, End, GraphRunContext

from src.database.chroma import ChromaRepository
from src.graph.state import GraphState
from src.util import directory as dir
from src.util import time

agent = Agent(
    model='openai:gpt-4o-mini',
    result_type=str,
    system_prompt=(
        "Responda a pergunta baseado no contexto."
        " Você precisa responder como se tivesse CERTEZA da resposta."
        " Use somente o contexto para responder a pergunta"
        " Se você não conseguir a resposta, diga que não sabe"
    )
)

@dataclass
class GenerateNode(BaseNode[GraphState]):
    question: str
    context: list[str]

    async def run(self, ctx: GraphRunContext[GraphState, ChromaRepository]) -> End[str]:
        print(f'-- [{time.now()}] Generate--')

        prompt = (
            f"Pergunta: {self.question}"
            f"\n\nContexto:{'\n'.join(self.context)}"
        )

        response = await agent.run(
            prompt
        )

        file = dir.File('prompt.txt', prompt)
        dir.create_file(file)

        ctx.state.answer = response.data

        return End(response)
        