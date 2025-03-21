import asyncio

from src.database.chroma import ChromaRepository
from src.graph.nodes.retrieve import RetrieveNode
from src.graph import graph, GraphState
from src.util import time

repository = ChromaRepository('./data/db', 'academia')

async def main():
    print('--Init--\n')
    state = GraphState()

    while True:
        question = input(f'[{time.now()}] HUMAN: ')
        state.question = question

        await graph.run(
            RetrieveNode(),
            state=state,
            deps=repository
        )

        print(f'\n[{time.now()}] IA: ', state.answer, '\n')

asyncio.run(main())