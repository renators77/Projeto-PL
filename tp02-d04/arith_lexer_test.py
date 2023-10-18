# arith_lexer_test.py
from arith_lexer import ArithLexer

teste = ArithLexer()
teste.build()

# teste.input('ESCREVER "ESCREVER"; , = +') #ESCREVER STRING ; , = + 
# teste.input('2 + 5') #NUM + NUM 
# teste.input('VAR 2023;') #VAR NUM ; 
teste.input('ESCREVER x "y123" _variavel') #ESCREVER ID STRING ID 

while True:
    token = teste.token() 
    if not token: 
        break
    print(token,end=" ")