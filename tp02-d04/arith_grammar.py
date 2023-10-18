# arith_grammar.py
from arith_lexer import ArithLexer
import ply.yacc as pyacc

class ArithGrammar:
    
    # #Adicionar as Variaveis declaradas
    declared = set()
    
    precedence = (
        ('left', '+', '-'),    # level=1, assoc=left
        ('left', '*', '/'),    # level=2, assoc=left
        ('right', 'simetrico'),
    )

    # Construtor da classe Grammar onde inicializa:
    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None
        self.declared = set()

    # Construir o analisador sintatico, pega no lexer e configura-o
    def build(self, **kwargs):
        self.lexer = ArithLexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)# cria analisador sintatico

    
    # Realiza a analise sintatica do Input fornecido
    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)
    

    # Regras Producao da Gramatica:


    # Lista de instruções da gramatica seguida de ;
    def p_s(self, p):
        """ S : LstV ';' """
        
        p[0] = p[1] # Atribuicao das instruçoes à producao

    
    #Definicao do FIM do programa
    def p_fim(self, p):
        """ S : FIM ';' """
        exit(0)
    
    
    # Construir uma lista de instruções separadas por  ;
    def p_expr_tail(self, p):
        """ LstV : LstV ';' Instrucao """
        
        lstArgs =  p[1]['args']
        lstArgs.append(p[3])
        p[0] = dict(op='seq', args= lstArgs  ) # retorna o valor da Producao LstV

    
    # Lista de Instrucao contendo uma unica instrucao
    def p_expr_head(self, p):
        """ LstV : Instrucao """
        
        p[0] = dict(op='seq', args=[p[1]]) # Permite construir a AST atraves da sequencia de instrucoes

    
    # *Representa a Instrucao ESCREVER, seguida de um identificador
    def p_expr_inst_operacao(self, p):
        """ Instrucao : ESCREVER Resultado 
                      | VAR ListaSimbolos """
        
        p[0] = {'op': 'esc', 'args': [p[2]]}    # Cria Dicionario *
        
    
    #Representa a operacao de que Instrucao pode ser um Identificador
    def p_expr_inst_operacao_identificador(self, p):
        """ Instrucao : Identificador """
        
        p[0] = p[1]    # Cria Dicionario *
    
    
    #Representao a operacao comentario
    def p_expr_inst_operacao_comentario(self, p):
        """ Instrucao : COMENTARIO """
    
        p[0] = dict(op='comentario', args=[p[1]])    # Cria Dicionario *
    
    
    #Rpresenta a operacao Ciclo
    def p_expr_inst_operacao_ciclo(self, p):
        """ Instrucao : PARA ID EM '[' MATH '.' '.' MATH ']' FAZER Resultado FIM PARA """
        
        p[0] = dict(op='ciclo', args=[p[2], p[5], p[8], p[11]])    # Cria Dicionario *
        
    
    #Representa a operacao Escrever ou VAR com o uso do comentario 
    def p_expr_inst_operacao_ESCVAR_comentario(self, p):
        """ Instrucao : ESCREVER Resultado COMENTARIO
                      | VAR ListaSimbolos COMENTARIO """
        
        p[0] = {'op': 'esc', 'comentario': p[3], 'args': [p[2]]}  # Cria Dicionario *
    
    
    #Define que a ListaSimbolos pode ser uma lista de IDs
    def p_expr_atribuicao_simbolo_id(self, p):
        """ ListaSimbolos : ListaIDs """
        
        p[0] = p[1]    #Cria no dicionario 
    
    
    #Representa que podemos ter separacao ',' entre a listaSimbolos
    def p_expr_multiplo_simbolo(self, p):
        """ ListaSimbolos : ListaIDs ',' ListaSimbolos """
        
        p[0] = dict(op='seq', args=[p[1], p[3]])    #Cria no dicionario
        
    
    #Define que a Lista de IDs, pode ser composta por ID
    def p_expr_id(self, p):
        """ ListaIDs : ID """
        
        ArithGrammar.declared.add(p[1])    #Adiciona o ID  ao set dos ID declarados
        
        p[0] = p[1]    #Cria no dicionario  
    
    
    #Define a atribuicao de um ID a um valor do math
    def p_expr_atribuicao_id(self, p):
        """ ListaIDs : ID '=' MATH """
        
        p[0] = dict(op='atr', args=[p[1], p[3]])    #Cria no dicionario
    
    
    #Representa a Atribuicao de um ID a um MATH
    def p_expr_atribuicao_identificador(self, p):
        """ Identificador : ID '=' MATH """
        
        # #Verifica se o ID está declarado se Sim, executa esta produção senão dá exit
        if p[1] not in ArithGrammar.declared:
            print(f"Syntax error: undeclared ID '{p[1]}'") 
        
            exit(1)
        p[0]= dict(op='atr',args= [ p[1] , p[3]] ) #Cria no dicionario
        
    
    #Define que Resultado pode ser um MATH do ID definido pela producao VAR
    def p_expr_listaResultados(self, p):
        """ Resultado : ListaResultados """
        
        p[0] = p[1]     #Cria no dicionario
       
    #Define que Resultado pode ter varios, resultado
    def p_args_multiplo_resultado(self, p):
        """ Resultado : ListaResultados ',' Resultado """
        
        p[0] = str(p[1]) + str(p[3])     #Cria no dicionario
    
    
    #Define que Resultado pode ser um MATH do ID definido pela producao VAR
    def p_args_resultado(self, p):
        """ ListaResultados : MATH """
        
        p[0] = p[1]     #Cria no dicionario
    
 
    # Define as operacoes matematicas entre simbolo e o seu grau de precedencia
    def p_expr_operacao_math(self, p):
        """ MATH : MATH '+' MATH
                 | MATH '-' MATH
                 | MATH '*' MATH
                 | MATH '/' MATH """
        
        p[0] = dict(op=p[2], args=[p[1], p[3]])   #Cria no dicionario
    
    
    #Define MATH Negativos
    def p_expr_sinalmenos(self, p):
        """ MATH : '-' MATH   %prec simetrico """
        
        p[0] = dict(op='-', args=[p[2]])    #Cria no dicionario 
    
    #Trata de MATH entre parenteses
    def p_expr_parenteses(self, p):
        """ MATH : '(' MATH ')' """
        
        # p[0] = {'entreParenteses': p[2 ]} #Cria no dicionario
        p[0] = p[2]
    
    #Define identificadores que sejam numeros inteiros ou decimais
    def p_expr_numero(self, p):
        """ MATH : NUM """
        
        # p[0] = {'numero': p[1]} #Cria no dicionario
        p[0] = p[1]
        
    #Define Identificadores que sejam ID
    def p_expr_var(self, p):
        """ MATH : ID """
        
        p[0] = {'var': p[1]}    #Cria no dicionario
    
    
    #Define Identificadores que sejam strings
    def p_expr_string(self, p):
        """ MATH : STRING """
        
        # p[0] = {'String': p[1]} #Cria no dicionario
        p[0] = p[1]
    
    
     #mensagem erro
    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        exit(1)