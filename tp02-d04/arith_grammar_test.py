# arith.py
from arith_grammar import ArithGrammar
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)

teste = ArithGrammar()
teste.build()

exemplos = [ # exemplos a avaliar de forma independente... 
            'ESCREVER "ola mundo!";',
            'ESCREVER "PL ", 2 ,"o ano de", "ESI";',
            'ESCREVER "soma de ", 9, "com ", 3*4 , "=", 9+2*3;',
            'VAR ano=2023, mes="maio";',
            'VAR B, c;',
            ]
for frase in exemplos:
    print(f"----------------------")
    print(f"--- frase '{frase}'")
    resposta = teste.parse ( frase ) 
    print("resultado: ")
    pp.pprint(resposta)