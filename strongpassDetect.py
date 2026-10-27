import re

passwordRegex = re.compile(r'''
(^(?=.*[A-Z].*[A-Z])        #Pelomenos duas letras maiúsculas devem estar na senha.
(?=.*[!@#$&*])              #Pelomenos um desses caracteres devem estar na senha
(?=.*[0-9].*[0-9])          #Obrigatoriamente dois caracteres númericos
(?=.*[a-z].*[a-z].*[a-z])   #Pelomenos 3 letras minúsculas
.{12,}                       #Total de 12 dígitos.
)''', re.VERBOSE)

def verificaçãoDeSenha():
    while True:
        senha = input('Forneça uma senha forte: ')
        if ' ' in senha:
            print('A senha não pode conter espaços.')
            continue
        else:
            check = passwordRegex.search(senha)
            if not check:
                print("Senha fraca, tente novamente")
                continue
            else:
                print('Senha forte!')
                return True


# testes realizados: teruioryouirty@@123AA / aa3AA@@123hfh
verificaçãoDeSenha()
