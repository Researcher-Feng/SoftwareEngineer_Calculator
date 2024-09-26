from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput


graphviz = GraphvizOutput()
graphviz.output_file = 'basic.png'

with PyCallGraph(output=graphviz):
    import main
