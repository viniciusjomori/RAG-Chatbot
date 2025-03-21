from pydantic_graph import Graph

from src.graph.nodes.generate import GenerateNode
from src.graph.nodes.retrieve import RetrieveNode

graph = Graph(
    nodes=[
        RetrieveNode,
        GenerateNode
    ],
)