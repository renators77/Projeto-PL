import ply.lex as plex

class ArithLexer:
    tokens= (
        "NUM", # numero inteiro
        "STRING", # string delimitada por aspas duplas
        "FIM",  # atribuicao para o "FIM" do programa.
        "ID",  # identificador de variável ou função
        "ESCREVER", # identificador 
        "VAR", # atribuicao de uma variavel
        "PARA", # atribuicao "PARA" o ciclo
        "EM", # atribuicao para "EM" ciclo
        "FAZER", # atribuicao para "FAZER" ciclo
        "COMENTARIO", #identificador de um comentario
    )
    
    literals = [
        '+', # sinal de soma
        '-', # sinal de subtração
        '*', # sinal de multiplicação
        '/', # sinal de divisão
        '=', # sinal de igual
        '(', # parêntese esquerdo
        ')', # parêntese direito
        '[', # parêntese reto esquerdo
        ']', # parêntese reto direito
        '>', # sinal de maior que
        '<', # sinal de menor que
        ',', # vírgula
        ';', # ponto-e-vírgula
        '.', # . para o ciclo   
    ]
    
    #Ignorar espacos
    t_ignore = " "
    
    #Inicializa o lexer como None
    def __init__(self):
        self.lexer = None
    
    #Reconhecer numeros inteiros e decimais     
    def t_NUM(self, t):
        r'[0-9]+(\.[0-9]+)?'
        
        t.value = int (t.value)
        return t
    
    #Reconhecer a Palavra ESC ou ESCREVER
    def t_ESCREVER(self, t):
        r'ESC(REVER)?'
        return t
    
    #Reconhecer a Palavra VAR
    def t_VAR(self, t):
        r'VAR'
        return t
    
    #Reconhecedor de FIM
    def t_FIM(self, t):
        r"FIM"
        return t
    
    
    #Reconhecedor de PARA
    def t_PARA(self, t):
        r"PARA"
        return t
    
    
    #Reconhecedor de EM
    def t_EM(self, t):
        r"EM"
        return t

    
    #Reconhecedor de FAZER
    def t_FAZER(self, t):
        r"FAZER"
        return t
    
    
    #Reconhecer um identificador 
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*' 
        return t
    
    #Reconhecedor de uma string
    def t_STRING(self, t):
        r'".*?"'
        
        t.value = t.value[1:-1]  # Remove quotes
        return t
    

    #Reconhecedor de COMENTARIO
    def t_COMENTARIO(self, t):
        r'//[^;]*'
        return t
    
    
    #cria o lexer
    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)

    #define a entrada do lexer
    def input(self, string):
        self.lexer.input(string)
    
    #Obter proximo token do lexer
    def token(self):
        token = self.lexer.token() #percorrer todos os tokens
        return token if token is None else token.type 
    
    #Ocorre quando ocorre erro lexico
    def t_error(self, t):
        print(f"Unexpected token: [{t.value[:10]}]")
        exit(1)
        
    