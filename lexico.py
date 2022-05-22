token_unario = {
    ',': 'VIRGULA',
    ';': 'PONTO_VIRGULA',
    '=': 'ATRIBUICAO',
    '+': 'SOMA',
    '-': 'DIFERENCA',
    '/': 'DIVISAO',
    '*': 'MULTIPLICACAO',
    '<': 'MENOR_QUE',
    '>': 'MAIOR_QUE',
    '(': 'ABRE_PARENTESE',
    ')': 'FECHA_PARENTESE',
    '[': 'ABRE_COLCHETE',
    ']': 'FECHA_CHOLCHETE',
    '{': 'ABRE_CHAVE',
    '}': 'FECHA_CHAVE'
}

token_binario = {
    '==': 'IGUAL',
    '!=': 'DIFERENTE',
    '>=': 'MAIOR_IGUAL',
    '<=': 'MENOR_IGUAL'
}

token_palavra = {
    'if': 'COMANDO_IF',
    'else': 'COMANDO_ELSE',
    'while': 'COMANDO_WHILE',
    'printf': 'COMANDO_PRINTF',
    'scanf': 'COMANDO_SCANF',
    'return': 'COMANDO_RETURN',
    'int': 'TIPO_INT',
    'float': 'TIPO_FLOAT',
    'double': 'TIPO_DOUBLE',
    'struct': 'TIPO_STRUCT',
    'typedef': 'DEF_TIPO',
    'string': 'STRING',
    'function': 'FUNCAO',
    'var': 'VARIAVEL'
}

char = " "
linha = 1
arquivo = None


def erro(fLinha, msg):
    print(fLinha, msg)
    exit(1)


def proximo_char():
    global char, linha

    char = arquivo.read(1)
    if char == '\n':
        linha += 1

    return char


def divisao_ou_comentario(fLinha):
    aux = proximo_char()

    if aux != '*' and aux != '/':  # Se for divisao
        return token_unario['/'], fLinha
    elif aux == '/':
        while char != '\n':  # elimina comentario linear
            proximo_char()
        return pega_token()

    # comentario multilinear
    proximo_char()
    while True:
        if char == '*':
            if proximo_char() == '/':
                proximo_char()
                return pega_token()
        elif len(char) == 0:
            erro(fLinha, "F I M  D O  A R Q U I V O")
        else:
            proximo_char()


def trata_string(fLinha):
    texto = ""

    while proximo_char() != '"':
        if len(char) == 0:
            erro(fLinha, "F I M  D O  A R Q U I V O")
        elif char == '\n':
            erro(fLinha, "F I M  D A  L I N H A")
        else:
            texto += char  # acumulador

    proximo_char()
    return token_palavra['string'], fLinha, texto


def trata_identificador(fLinha):  # identificador, numero ou palavra reservada
    texto = ""

    if char.isalpha():  # verifica se o char e uma letra

        while char.isalnum() or char == '.':
            # acumulador enquanto for alfanumerico
            texto += char
            proximo_char()
        if char == '[':
            while char != ']':  # acumulador enquanto for alfanumerico
                texto += char
                proximo_char()
            if char == ']':
                texto += char
                proximo_char()
        if texto in token_palavra:  # se for alguma palavra reservada
            return token_palavra[texto], fLinha, texto

        else:  # se nao e um identificador
            return "IDENTIFICADOR", fLinha, texto

    elif char.isdigit():  # se comecar por numero, ja sabemod que e numero

        while char.isdigit():  # acumulador enquanto for numero
            texto += char
            proximo_char()

        if char == ".":  # pega o primeiro ponto do decimal
            texto += "."
            proximo_char()

            while char.isdigit():
                texto += char
                proximo_char()
            return "NUMERO_FLOAT", fLinha, texto

        return "NUMERO", fLinha, texto

    else:
        texto = char
        proximo_char()
        return "TOKEN_ALIENIGENA", fLinha, texto


def pega_tk_binario(complemento, sim, fLinha):
    aux = char
    proximo = proximo_char()
    if proximo == complemento:  # complemento e o que se espera depois do char atual
        proximo_char()
        return sim, fLinha

    else:
        return token_unario[aux], fLinha


def pega_token():
    while char.isspace():  # elimina os espacos
        proximo_char()

    fLinha = linha

    if len(char) == 0:
        return "EOF", fLinha

    elif char == '/':
        return divisao_ou_comentario(fLinha)
    elif char == '<':
        return pega_tk_binario('=', token_binario['<='], fLinha)
    elif char == '>':
        return pega_tk_binario('=', token_binario['>='], fLinha)
    elif char == '=':
        return pega_tk_binario('=', token_binario['=='], fLinha)
    elif char == '!':
        if proximo_char() == '=':
            return token_binario['!=']
        else:
            return "TOKEN_ALIENIGENA", fLinha, char
    elif char == '"':
        return trata_string(fLinha)
    elif char in token_unario:
        aux = char
        proximo_char()
        return token_unario[aux], fLinha
    else:
        return trata_identificador(fLinha)

    # ________________________ M A I N ________________________


arquivo = open("test.c", 'r')
saida = open('lex.txt', 'w')
while True:
    dados = pega_token()
    token = dados[0]
    fLinha = dados[1]

    if token == "NUMERO" or token == "NUMERO_FLOAT":
        print("%d  %s  %s" % (fLinha, token, dados[2]))
        saida.write("%d  %s  %s\n" % (fLinha, token, dados[2]))
    elif token == "IDENTIFICADOR":
        print("%d  %s  %s" % (fLinha, token, dados[2]))
        saida.write("%d  %s  %s\n" % (fLinha, token, dados[2]))
    elif token == "STRING":
        print("%d  %s  %s" % (fLinha, token, dados[2]))
        saida.write("%d  %s  %s\n" % (fLinha, token, dados[2]))
    elif token == "TOKEN_ALIENIGENA":
        print("%d  %s  %s" % (fLinha, token, dados[2]))
        saida.write("%d  %s  %s\n" % (fLinha, token, dados[2]))
    else:
        print('%d  %s' % (fLinha, token,))
        saida.write('%d  %s\n' % (fLinha, token,))
    if token == "EOF":
        saida.close()
        break
