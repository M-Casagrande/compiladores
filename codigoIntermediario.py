operadores = {
    '+': 'ADD',
    '-': 'SUB',
    '/': 'DIV',
    '*': 'MLT',
    '=': 'ATRIBUICAO'
}
op_logico = {
    '==': 'IGUAL',
    '!=': 'DIFERENTE',
    '<': 'MENOR_QUE',
    '>': 'MAIOR_QUE'
}

comandos = ('if', 'else', 'while', 'return')
sinc = ('(', ')', ';')


class pilha_comando:
    'Classe para uma pilha'

    def __init__(self):
        self.pilha = []
        self.instr = []
        self.funcao = {}

    def empilha(self, comando):
        return self.pilha.append(comando)

    def desempilha(self, id):
        atual = self.pilha.pop()
        fila = []  # fila de comandos
        temp = ""  # variavel ou numero imediatamente anterior
        operador = ""  # armazena o operador a ser tratado
        opLog = ""  # armazena o operador lógico a ser tratado
        acmldr = [None, None, None]  # acumula variavel na 0 e 1 e na 2 um operador
        temporarios = []  # cria registradores temporarios
        while (len(self.pilha) != 0):
            if atual == '}':
                fila.insert(0, ['}', None, None, None])
                acmldr = zera(acmldr)
            elif atual == '=':
                if operador != "":
                    atual = self.pilha.pop()
                    fila.insert(0,
                                [operadores[operador], atual,
                                 temp, acmldr[0]])
                    acmldr = zera(acmldr)
                    temp = ""
                    operador = ""
                elif acmldr[2] is not None:
                    atual = self.pilha.pop()
                    fila.insert(0,
                                [operadores[acmldr[2]], atual,
                                 temp, acmldr[1]])
                    acmldr = zera(acmldr)
                    temp = ""
                    operador = ""
                elif temp in self.funcao:
                    atual = self.pilha.pop()
                    fila.insert(0,
                                ['MOV', atual, 'JMP', self.funcao[temp]])
                    acmldr = zera(acmldr)
                    temp = ""
                else:
                    atual = self.pilha.pop()
                    fila.insert(0,
                                ['MOV', atual, temp, None])
                    acmldr = zera(acmldr)
                    temp = ""
            elif atual == ')' and temp and operador != "":
                acmldr[1] = temp
                acmldr[2] = operador
                operador = ""
                temp = ""
            elif atual in operadores:
                acmldr[0] = temp
                operador = atual
            elif atual in op_logico:
                acmldr[1] = temp
                opLog = atual
            elif atual == '(':
                i = len(temporarios)
                temporarios.append('t'+str(i+1))
                fila.insert(0,
                            [operadores[operador], temporarios[i-1],
                             temp, acmldr[0]])
                acmldr = zera(acmldr)
                temp = temporarios[i-1]
                operador = ""
            elif atual == 'return':
                fila.insert(0,
                            ['RTN', temp, None, None])
            elif atual == 'else':
                fila.insert(0, ['else', None, None, None])
            elif atual == 'if':
                if opLog == '<':
                    fila.insert(0, ['JGT', temp, acmldr[1], 'PULAR'])
                elif opLog == '>':
                    fila.insert(0, ['JGT', acmldr[1], temp, 'PULAR'])
                elif opLog == '==':
                    fila.insert(0, ['JDT', temp, acmldr[1], 'PULAR'])
                elif opLog == '!=':
                    fila.insert(0, ['JET', temp, acmldr[1], 'PULAR'])
            elif atual == 'while':
                if opLog == '<':
                    fila.insert(0, ['JGT', temp, acmldr[1], 'WPULAR'])
                elif opLog == '>':
                    fila.insert(0, ['JGT', acmldr[1], temp, 'WPULAR'])
                elif opLog == '==':
                    fila.insert(0, ['JDT', temp, acmldr[1], 'WPULAR'])
                elif opLog == '!=':
                    fila.insert(0, ['JET', temp, acmldr[1], 'WPULAR'])
            else:
                temp = atual
            if len(self.pilha) > 0:
                atual = self.pilha.pop()
        i = 0
        j = 0
        fila.pop(-1)
        for iten in fila:
            if fila[i][0] == '}':
                j = i
                while i >= 0:
                    i -= 1
                    if fila[i][0] is 'else':
                        fila.insert(i, ['JMP', j, None, None])
                        fila.pop(j)
                        break
                    elif fila[i][3] == 'PULAR':
                        fila[i][3] = j+1
                        fila.pop(j)
                        break
                    elif fila[i][3] == 'WPULAR':
                        fila[i][3] = j+2
                        fila[j] = ['JNP', i+1, None, None]
                        break
                i = j
            i += 1
        self.funcao[id] = len(self.instr)
        self.pilha.clear()
        return self.instr.append(fila)

    def imprime_instrucoes(self):
        i = 0
        print(self.funcao)
        for item in self.instr:
            print(i)
            print(self.instr[i])
            i += 1


def zera(vetor):
    vetor[0] = None
    vetor[1] = None
    vetor[2] = None
    return vetor
# varrer a FILA atras dos } pa poder colcoar os GOTO e substituir os PULAR

# transformar isso no gerador de codigo intermediaro
# a medida que for desempilhando as instruções,
# que acontece sempre ao fim do BLOCO
# acrescentar a instrução completa numa FILA
# depois imprimir essa filha
# pq na pilha nos vamos desempilha do final para o começo
# pela gramatica obrigatoriamente tem um else depois do if
# porem eu nao tratei disso no sintatico, [ja tratei]
# aqui eu preciso esperar um else apos desempilhar os comandos do if
# para ser a instruçao do GOTO
# o GOTO vai ser para o final da fila de instruções
# que vai ser onde o inicio do outro comando vai ser anexado
# fazer uma fila por bloco
# ao fim do bloco desempilhar e colocar numa fila temporaria
# pegar a len()+1+filareal.len() dessa fila
# e sinalizar ao GOTO onde deve ser o pulo
# anexar a fila temporaria a fila real
# filareal é a fila do programa como um todo
# marcar o inicio do bloco de cada funcao
