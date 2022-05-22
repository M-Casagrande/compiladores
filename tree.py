from anytree import NodeMixin, RenderTree


class arvore():
    'Classe para uma arvore sintatica'
    linha = 0
    token = " "

    def __init__(self, linha, token):
        self.linha = linha
        self.token = token


class arv_sint(arvore, NodeMixin):
    def __init__(self, linha, token, parent=None, children=None):
        super(arv_sint, self).__init__(linha, token)
        self.parent = parent
        if children:
            self.children = children


def imprime(arvore):
    for pre, _, node in RenderTree(arvore):
        treesr = "%s%s" % (pre, node.token)
        print(treesr.ljust(8))
