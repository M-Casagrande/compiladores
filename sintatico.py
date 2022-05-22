import symTable as symTable
import tree as tree
import pdb as pdb
import codigoIntermediario as intermediario
# variavel texto vai sempre ter o final daquele token especifico
# pai é quem chama
op_logico = {
    'IGUAL': '==',
    'DIFERENTE': '!=',
    'MAIOR_IGUAL': '>=',
    'MENOR_IGUAL': '<=',
    'MENOR_QUE': '<',
    'MAIOR_QUE': '>'
}

tipos = {
    'TIPO_INT': 'int',
    'TIPO_FLOAT': 'float',
    'TIPO_DOUBLE': 'double',
    'TIPO_STRUCT': 'struct',
    'STRING': 'string'
}

operadors = {
    'SOMA': '+',
    'DIFERENCA': '-',
    'DIVISAO': '/',
    'MULTIPLICACAO': '*'
}

structs = {}

arquivo = None
token = " "
linha = 1
texto = " "
acum_else = 0  # contador de ifs para elses
raiz = tree.arv_sint(0, "programa")
escopo = " "
tb_sim = symTable.tabela_sim()
npar = 0
comandos = intermediario.pilha_comando()


def erro(flinha, msg):
    print(flinha, msg)
    exit(1)


def warning(linha, msg):
    print(linha, msg)


def prox_token():
    global token, linha, texto
    line = ['', '', '']
    conteudo = arquivo.readline()
    line = conteudo.split("  ")
    linha = line[0]
    aux = line[1].split("\n")
    token = aux[0]
    if token in ('IDENTIFICADOR', 'NUMERO', 'STRING', 'TOKEN_ALIENIGENA'):
        aux = line[2].split("\n")
        texto = aux[0]
    else:
        texto = None
    return token


def trata_if(pai, escopo):
    global acum_else
    tree.arv_sint(linha, 'if', pai)
    comandos.empilha('if')
    acum_else += 1
    trata_exp_log(pai, escopo)
    tkbloco = tree.arv_sint(linha, 'BLOCO', pai)
    return trata_bloco(tkbloco, escopo)


def trata_else(pai, escopo):
    global acum_else
    tree.arv_sint(linha, 'else', pai)
    comandos.empilha('else')
    if acum_else > 0:
        acum_else -= 1
        tkbloco = tree.arv_sint(linha, 'BLOCO', pai)
        prox_token()
        return trata_bloco(tkbloco, escopo)

    else:
        erro(linha, "Else sem if!")


def trata_while(pai, escopo):
    tree.arv_sint(linha, 'while', pai)
    comandos.empilha('while')
    trata_exp_log(pai, escopo)
    tkbloco = tree.arv_sint(linha, 'BLOCO', pai)
    return trata_bloco(tkbloco, escopo)


def trata_scanf(pai, escopo):
    tree.arv_sint(linha, 'scanf', pai)
    if prox_token() == 'ABRE_PARENTESE':
        tree.arv_sint(linha, '(', pai)
        prox_token()
        trata_nome(pai, escopo)
        if prox_token() == 'FECHA_PARENTESE':
            tree.arv_sint(linha, ')', pai)
            if prox_token() == 'PONTO_VIRGULA':
                tree.arv_sint(linha, ';', pai)
                return pai

            else:
                erro(linha,
                     "Falta ';' para encerrar a linha")
        else:
            erro(linha,
                 "Falta ')' para encerrar o scanf")
    else:
        erro(linha,
             "Falta '(' para iniciar o nome do scanf")


def trata_printf(pai, escopo):
    tree.arv_sint(linha, 'printf', pai)
    if prox_token() == 'ABRE_PARENTESE':
        tree.arv_sint(linha, '(', pai)
        prox_token()
        trata_nome_numero(pai, escopo)
        if prox_token() == 'FECHA_PARENTESE':
            tree.arv_sint(linha, ')', pai)
            if prox_token() == 'PONTO_VIRGULA':
                tree.arv_sint(linha, ';', pai)
                return pai

            else:
                erro(linha,
                     "Falta ';' para encerrar a linha")
        else:
            erro(linha,
                 "Falta ')' para encerrar o printf")
    else:
        erro(linha,
             "Falta '(' para iniciar o nome do printf")


def trata_return(pai, escopo):
    ret = tree.arv_sint(linha, 'return', pai)
    comandos.empilha('return')
    return trata_valor(ret, escopo)


def trata_nome_numero(pai, escopo):
    if texto.isdigit():
        numero = tree.arv_sint(linha, "NUMERO", pai)
        return trata_numero(numero)
    else:
        return trata_nome(pai, escopo)


def trata_bloco(pai, escopo):
    if token == 'ABRE_CHAVE':
        tree.arv_sint(linha, '{', pai)
        prox_token()
        while True:
            if token == 'IDENTIFICADOR':
                if tb_sim.verifica_tipo(texto, escopo) == 'string':
                    trata_nome(pai, escopo)
                    prox_token()
                    if token == 'ATRIBUICAO':
                        tree.arv_sint(linha, '=', pai)
                        trata_valor(pai, escopo)
                    else:
                        erro(linha, "esperva uma atribuição")
                else:
                    exp = tree.arv_sint(linha, 'EXP', pai)
                    trata_exp_mat(exp, 0, escopo, False, 0)
            elif token == 'COMANDO_IF':
                trata_if(pai, escopo)
            elif token == 'COMANDO_ELSE':
                trata_else(pai, escopo)
            elif token == 'COMANDO_WHILE':
                trata_while(pai, escopo)
            elif token == 'COMANDO_PRINTF':
                trata_printf(pai, escopo)
            elif token == 'COMANDO_SCANF':
                trata_scanf(pai, escopo)
            elif token == 'COMANDO_RETURN':
                trata_return(pai, escopo)
            elif token == 'VARIAVEL':
                declaracao_var(pai, escopo, 0, False)
            elif token == 'DEF_TIPO':
                trata_typedef(pai, escopo)
            elif token == 'EOF':
                erro(linha, "Fim do Arquivo")
            elif token == 'FECHA_CHAVE':
                comandos.empilha('}')
                tree.arv_sint(linha, '}', pai)
                return pai
            else:
                erro(linha, "Bloco nao inicia por comando ou declaração")
            prox_token()
    else:
        erro(linha, "Falta '{' para iniciar o bloco")


def trata_numero(pai):
    num = tree.arv_sint(linha, token, pai)
    tree.arv_sint(linha, texto, num)
    return num


def trata_chama_struct(pai, escopo):
    global texto
    nome, var_interna = texto.split('.', 1)
    tipo = tb_sim.verifica_tipo(nome, escopo)
    st_arv = tree.arv_sint(linha, 'STRUCT', pai)
    if tipo in structs:
        scp = structs[tipo]
        texto = nome
        trata_nome(st_arv, escopo)
        tree.arv_sint(linha, '.', st_arv)
        texto = var_interna
        trata_nome(st_arv, scp)
        return pai


def trata_nome(pai, escopo):  # verificar se e variavel ou funcao na tabela
    global texto
    if '.' in texto:
        return trata_chama_struct(pai, escopo)

    nome = tree.arv_sint(linha, "NOME", pai)
    if '[' in texto and ']' in texto:
        vetor = texto.partition('[')
        if tb_sim.pertence_escopo(vetor[0], escopo) or tb_sim.eglobal(vetor[0]):
            tree.arv_sint(linha, vetor[0], nome)
            tree.arv_sint(linha, vetor[1], nome)
            tam = vetor[2].split(']')
            tree.arv_sint(linha, tam[0], nome)
            tree.arv_sint(linha, ']', nome)
    elif tb_sim.pertence_escopo(texto, escopo) or tb_sim.eglobal(texto):
        tree.arv_sint(linha, texto, nome)
        return nome
    else:
        tb_sim.imprime()
        erro(linha,
             "A variavel %s nao pertence ao escopo %s" % (texto, escopo))


def trata_exp_mat(pai, tipoEsq, escopo, operador, contador):
    if token == 'PONTO_VIRGULA':
        tree.arv_sint(linha, ';', pai)
        return pai
    elif token in op_logico or token == 'ABRE_CHAVE':
        if comandos.pilha[-1] == ')':
            comandos.pilha.pop(-1)
        return pai
    elif token == 'ATRIBUICAO':
        comandos.empilha('=')
        tree.arv_sint(linha, '=', pai)
        prox_token()
        return trata_exp_mat(pai, tipoEsq, escopo, False, contador)
    elif not operador:
        # a chamada veio apos um operador
        if token == 'IDENTIFICADOR':
            if tb_sim.efuncao(texto):
                comandos.empilha(texto)
                trata_chama_funcao(pai, escopo)
                prox_token()
                return trata_exp_mat(pai, tipoEsq, escopo, True, contador)
            tipoVar = tb_sim.verifica_tipo(texto, escopo)
            if tipoEsq == 'INT':
                if tipoVar != 'STRUCT':
                    if tipoVar != 'INT':
                        warning(linha,
                                "int recebendo um outro tipo")
                    comandos.empilha(texto)
                    trata_nome(pai, texto, escopo)
                    prox_token()
                    return trata_exp_mat(pai, tipoEsq, escopo, True, contador)
                else:
                    erro(linha,
                         "atribuição de struct")
            elif tipoEsq == 'FLOAT' or 'DOUBLE' or tipoVar == 'DOUBLE':
                if tipoVar != 'STRUCT':
                    comandos.empilha(texto)
                    trata_nome(pai, escopo)
                    prox_token()
                    return trata_exp_mat(pai, tipoEsq, escopo, True, contador)
                else:
                    erro(linha,
                         "atribuição de struct")
            elif tipoEsq == 0:
                comandos.empilha(texto)
                trata_nome(pai, escopo)
                prox_token()
                return trata_exp_mat(pai, tb_sim.verifica_tipo(token, escopo),
                                     escopo, True, contador)
        elif token == 'NUMERO':
            comandos.empilha(texto)
            trata_numero(pai)
            prox_token()
            return trata_exp_mat(pai, tipoEsq, escopo, True, contador)
        elif token == 'NUMERO_FLOAT':
            if tipoEsq == 'INT':
                warning(linha,
                        "Float sendo atribuido a um int")
            comandos.empilha(texto)
            trata_numero(pai)
            prox_token()
            return trata_exp_mat(pai, tipoEsq, escopo, True, contador)
        elif token == '(':
            comandos.empilha('(')
            contador += 1
            tree.arv_sint(linha, token, pai)
            prox_token()
            return trata_exp_mat(pai, tipoEsq, escopo, True, contador)
    elif operador:
        if token == 'FECHA_PARENTESE':
            comandos.empilha(')')
            contador -= 1
            if contador < 0:
                return (linha, "erro no numero de parenteses na expressao")
            tree.arv_sint(linha, ')', pai)
            prox_token()
            return trata_exp_mat(pai, tipoEsq, escopo, False, contador)
        elif token == 'DIVISAO' and tipoEsq == 'INT':
            warning(linha,
                    "Inteiro recebendo resultado de divisao")
        comandos.empilha(operadors[token])
        trata_operador(pai)
        prox_token()
        return trata_exp_mat(pai, tipoEsq, escopo, False, contador)
    else:
        return erro(linha, "token inesperado")


def trata_operador(pai):
    return tree.arv_sint(linha, operadors[token], pai)


def trata_valor(pai, escopo):
    prox_token()

    if token in ('IDENTIFICADOR', 'ABRE_PARENTESE', 'NUMERO'):
        exp = tree.arv_sint(linha, 'EXP', pai)
        return trata_exp_mat(exp, tb_sim.verifica_tipo(escopo, 'global'),
                             escopo, False, 0)
    elif token == 'STRING':
        return trata_string(pai)
    else:
        return erro(linha,
                    "valor desconhecido")


def trata_op_logico(pai):
    if token in op_logico:
        comandos.empilha(op_logico[token])
        return tree.arv_sint(linha, op_logico[token], pai)
    else:
        erro(linha,
             "operador logico nao encontrado")


def trata_exp_log(pai, escopo):
    prox_token()
    if token == 'ABRE_PARENTESE':
        tree.arv_sint(linha, '(', pai)
        explog = tree.arv_sint(linha, "EXP_LOGICA", pai)
        prox_token()
        exp = tree.arv_sint(linha, 'EXP', explog)
        trata_exp_mat(exp, "FLOAT", escopo, False, 0)
        trata_op_logico(explog)
        prox_token()
        exp2 = tree.arv_sint(linha, 'EXP', explog)
        trata_exp_mat(exp2, "FLOAT", escopo, False, 1)
        return explog
    else:
        erro(linha,
             "Falta ( para iniciar a expressão lógica")


def trata_typedef(pai):  # struct vem aqui
    global tb_sim
    df = tree.arv_sint(linha, 'DEF_TIPO', pai)
    tree.arv_sint(linha, 'typedef', df)
    prox_token()
    if token in tipos:
        tipo = tipos[token]
    else:
        erro(linha, "Falta o tipo")
    if token == 'TIPO_STRUCT':
        return trata_struct(pai, 'global')
    prox_token()

    if token == 'IDENTIFICADOR':
        global texto
        if "[" in texto:
            nome_do_vetor, abrcol, tam = texto.partition('[')
            texto = nome_do_vetor
            trata_nome(pai, 'global')
            tb_sim.entra_sym(texto, 'def_tipo', tipo, 0, 0)
            prox_token()
            if token == 'PONTO_VIRGULA':
                tree.arv_sint(linha, ';', pai)
                return df
            else:
                erro(linha, "esperava ; para fechar o typedef")
        else:
            tipo = texto
            tipos[texto] = texto
            tb_sim.entra_sym(texto, 'def_tipo', 'global', tipo, 0, 0)
            trata_nome(df, 'global')
            prox_token()
            if token == 'PONTO_VIRGULA':
                tree.arv_sint(linha, ';', df)
                return df
            else:
                erro(linha, "esperava ; para fechar o typedef")
    else:
        erro(linha, 'esperava um identificador')


def declaracao_var(pai, escopo, tipo, param):
    global tb_sim, token, npar
    if token == 'PONTO_VIRGULA' and param is False:
        tree.arv_sint(linha, ';', pai)
        return pai
    elif token == 'PONTO_VIRGULA':
        tree.arv_sint(linha, ';', pai)
        prox_token()
        if token == 'VARIAVEL':
            return declaracao_var(pai, escopo, tipo, param)
        elif token == 'FECHA_PARENTESE':
            tb_sim.atualiza_qtd_param(escopo, 'global', npar)
            npar = 0
            return pai
        else:
            return pai
    else:
        if token != 'VIRGULA':
            prox_token()
            if token == 'IDENTIFICADOR' and texto in tipos:
                token = texto
        else:
            token = tipo
        if token in tipos:
            tipo = token
            prox_token()
            if token == 'IDENTIFICADOR':
                if param:
                    npar += 1
                if '[' in texto:
                    nome = texto.split('[')
                    tb_sim.entra_sym(nome[0], 'var', escopo,
                                     tipos[tipo], 0, npar)
                else:
                    tb_sim.entra_sym(texto, 'var', escopo,
                                     tipos[tipo], 0, npar)
                tree.arv_sint(linha, tipos[tipo], pai)
                trata_nome(pai, escopo)
                prox_token()
                if token == 'VIRGULA':
                    tree.arv_sint(linha, ',', pai)
                return declaracao_var(pai, escopo, tipo, param)
        else:
            erro(linha, "Falta o tipo da variavel")


def trata_dec_funcao(pai):
    global tb_sim
    escopo = ""
    prox_token()
    if token == 'IDENTIFICADOR':
        if texto in tipos:
            tipo = tipos[texto]
            tree.arv_sint(linha, tipo, pai)
            prox_token()
            if token == 'IDENTIFICADOR':
                nome = texto
                escopo = nome
                tb_sim.entra_sym(nome, 'funcao', 'global', tipo, 0, 0)
            else:
                erro(linha,
                     "Esperava um identificador para a função")
    elif token in tipos:
        tipo = tipos[token]
        prox_token()
        if token == 'IDENTIFICADOR':
            nome = texto
            escopo = nome
            tb_sim.entra_sym(nome, 'funcao', 'global', tipo, 0, 0)
        else:
            erro(linha,
                 "Esperava um identificador para a função")
        trata_nome(pai, 'global')
    else:
        erro(linha,
             "Falta o tipo da funcao")

    prox_token()
    if token == 'ABRE_PARENTESE':
        tree.arv_sint(linha, '(', pai)
    else:
        erro(linha,
             "falta o '(' da funcao")
    prox_token()
    if token == 'VARIAVEL':
        df_par = tree.arv_sint(linha, "DEF_PARAMETROS", pai)
        declaracao_var(df_par, escopo, 0, True)
        if token == 'FECHA_PARENTESE':
            tree.arv_sint(linha, ")", pai)
            prox_token()
        else:
            erro(linha, 'falta o ) pra fechar a lista de parametros')
        bloco = tree.arv_sint(linha, 'BLOCO', pai)
        trata_bloco(bloco, escopo)
        comandos.desempilha(nome)
        return pai
    elif token == 'FECHA_PARENTESE':
        tree.arv_sint(linha, ")", pai)
        prox_token()
        tree.arv_sint(linha, 'BLOCO', pai)
        trata_bloco(pai, escopo)
        comandos.desempilha(nome)
        return pai
    else:
        erro(linha,
             "token nao identificado na definicao de funcao")


def trata_struct(pai, escopo):
    tree.arv_sint(linha, 'struct', pai)
    prox_token()
    if token == 'IDENTIFICADOR':
        tb_sim.entra_sym(texto, 'var', 'global', 'struct', 0, 0)
        strct_escopo = texto
        trata_nome(pai, escopo)
        prox_token()
        if token == 'ABRE_CHAVE':
            tree.arv_sint(linha, '{', pai)
            defvar = tree.arv_sint(linha, 'DEF_VARIAVEIS', pai)
            prox_token()
            while token != 'FECHA_CHAVE':
                declaracao_var(defvar, strct_escopo, 0, False)
                prox_token()
            tree.arv_sint(linha, '}', pai)
            prox_token()
            if token == 'IDENTIFICADOR':
                structs[texto] = strct_escopo
                tipos[texto] = texto
                df = tree.arv_sint(linha, 'TYPEDEF', pai)
                tpdef = tree.arv_sint(linha, token, df)
                tree.arv_sint(linha, texto, tpdef)
                prox_token()
                if token == 'PONTO_VIRGULA':
                    tree.arv_sint(linha, ';', pai)
                    return pai
                else:
                    erro(linha, "esperava um ; para finalizar a struc")
            else:
                erro(linha,
                     "Esperava um identificador para a struct")
        else:
            erro(linha,
                 "Esperava um identificador para a struct")


def trata_string(pai):
    strg = tree.arv_sint(linha, token, pai)
    tree.arv_sint(linha, texto, strg)
    prox_token()
    if token == 'PONTO_VIRGULA':
        tree.arv_sint(linha, ';', pai)
    else:
        erro(linha, 'falta o ;')
    return strg


def trata_chama_funcao(pai, escopo):
    func = tree.arv_sint(linha, 'FUNCAO', pai)
    tree.arv_sint(linha, texto, func)
    nome = texto
    prox_token()
    if token == 'ABRE_PARENTESE':
        tree.arv_sint(linha, '(', func)
        trata_parametros(nome, func, escopo)
        if token == 'FECHA_PARENTESE':
            tree.arv_sint(linha, ')', func)
            return func
        else:
            erro(linha, "Falta o ')' da declaração de função")
    else:
        erro(linha, "Falta o '(' da declaração de função")


def trata_parametros(nome, pai, escopo):
    prox_token()
    cont = 0
    while token != 'FECHA_PARENTESE':
        if token == 'IDENTIFICADOR':
            cont += 1
            trata_nome(pai, escopo)
        elif token == 'VIRGULA':
            tree.arv_sint(linha, ',', pai)
        else:
            erro(linha, 'esperava um identificador ou virgula')
        prox_token()
    if tb_sim.verifica_qtd_param(nome, 'global', cont):
        return pai
    else:
        erro(linha, "qtd de parametro errada")
    # ________________________ M A I N ________________________

    # ________________________ M A I N ________________________


arquivo = open('lex.txt', 'r')
sub = tree.arv_sint(0, " ", raiz)
while True:
    prox_token()
    if token == "DEF_TIPO":
        trata_typedef(raiz)
    elif token == "FUNCAO":
        trata_dec_funcao(raiz)
    elif token == "VARIAVEL":
        declaracao_var(raiz, 'global', 0, False)
    elif token == "EOF":
        tree.arv_sint(linha, token, raiz)
        tree.imprime(raiz)
        break

tree.imprime(raiz)
tb_sim.imprime()
comandos.imprime_instrucoes()
