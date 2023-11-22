from rdflib import Graph

def split_blocks(txt):
    rdf_blocks = ['']
    for line in txt.splitlines():
        if len(line) == 0:
            rdf_blocks.append('')
        else:
            rdf_blocks[-1] += ('\n' if len(rdf_blocks[-1]) > 0 else '') + line
    return rdf_blocks

class ParseErrorOnBlock:
    block_txt: str
    error_obj: SyntaxError
    def __init__(self, block_txt: str, error_obj: SyntaxError):
        self.block_txt = block_txt
        self.error_obj = error_obj

class ParseResult:
    graph: Graph
    block_errors: [ParseErrorOnBlock]
    def __init__(self, graph: Graph, block_errors: [ParseErrorOnBlock]):
        self.graph = graph
        self.block_errors = block_errors

def parse(rdf_txt, graph=None, format='text/turtle'):
    block_errors = []
    if graph is None:
        graph = Graph()
    try:
        graph.parse(data=rdf_txt, format=format)
    except SyntaxError:
        txt_blocks = split_blocks(rdf_txt)
        preamble = txt_blocks[0]
        content_blocks = txt_blocks[1:]
        for content_block in content_blocks:
            block = preamble + '\n' + content_block
            try:
                graph.parse(data=block, format=format)
            except SyntaxError as error:
                block_errors.append(ParseErrorOnBlock(block,error))
    return ParseResult(graph, block_errors)