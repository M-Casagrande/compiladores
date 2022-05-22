# [nome] [class] [escopo] [tipo] [num_param] [ordem_param]
#   0       1       2       3       4           5


class tabela_sim:
    'Classe para uma tabela de símbolos'

    def __init__(self):
        self.lista = []

    def entra_sym(self, nome, classif, escopo, tipo, num_param, ordem_param):
        return self.lista.append([nome, classif, escopo,
                                  tipo, num_param, ordem_param])

    def pertence_escopo(self, nome, escopo):
        i = 0
        for list in self.lista:
            if self.lista[i][0] == nome and self.lista[i][2] == escopo:
                return True  # achou a var com o mesmo nome no escopo
            i += 1
        return False

    def efuncao(self, nome):
        i = 0
        for list in self.lista:
            if self.lista[i][0] == nome and self.lista[i][2] == 'global':
                if self.lista[i][1] == 'funcao':
                    return True
            i += 1
        return False

    def verifica_tipo(self, nome, escopo):
        i = 0
        for list in self.lista:
            if self.lista[i][0] == nome and self.lista[i][2] == escopo:
                return self.lista[i][3]  # retorna o tipo
            i += 1
        return 0

    def verifica_qtd_param(self, nome, escopo, qtd_param):
        i = 0
        for list in self.lista:
            if self.lista[i][0] == nome and self.lista[i][2] == escopo:
                if qtd_param == self.lista[i][4]:
                    return True
                else:
                    return False  # se o numero de parametros for diferente
            i += 1
        return -1

    def atualiza_qtd_param(self, nome, escopo, qtd):
        i = 0
        for list in self.lista:
            if self.lista[i][0] == nome and self.lista[i][2] == escopo:
                self.lista[i][4] = qtd
                return 1
            i += 1
        return 0

    def eglobal(self, nome):
        i = 0
        for list in self.lista:
            if self.lista[i][0] == nome and self.lista[i][2] == 'global':
                return True
            i += 1
        return False

    def imprime(self):
        print("[nome]   [class]   [escopo]   ",
              "[tipo]   [num_param]   [ordem_param]")
        i = 0
        for list in self.lista:
            print(self.lista[i])
            i += 1
