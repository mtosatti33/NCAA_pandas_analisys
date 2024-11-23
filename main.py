try:
    import pandas as pd
except ModuleNotFoundError:
    print("Módulo pandas não encontrado.\nPor favor instale o pandas através do comando 'pip(.exe) install pandas'")
    quit()

import os

# variáveis e constantes
arquivo = "NCAA.csv"
TAM_HEAD = 20

def limpa_tela():
    os.system("cls" if os.name == "nt" else "clear")

def ordenar_menu():
    print("\n")
    print("1. Melhores Campanhas")
    print("2. Piores Campanhas")
    try:
        op = int(input("Escolha: "))
    except ValueError:
        op = 1 # Valor Padrão se erro

    match op:
        case 1:
            return False
        case 2:
            return True
        case _:
            quit()

def ordenar_campo_yd():
    print("\n")
    print("1. Jardas/Jogo")
    print("2. Jardas permitidas/Jogo")
    try:
        op = int(input("Escolha: "))
    except ValueError:
        op = 1 # Valor Padrão se erro

    match op:
        case 1:
            return "Yds/Game"
        case 2:
            return "Yds/Game Allowed"
        case _:
            quit()

def ordenar_campo_td():
    print("\n")
    print("1. Touchdowns/Jogo")
    print("2. Touchdowns permitidos/Jogo")
    try:
        op = int(input("Escolha: "))
    except ValueError:
        op = 1 # Valor Padrão se erro

    match op:
        case 1:
            return "TD/Game"
        case 2:
            return "TD/Game Allowed"
        case _:
            quit()

def transformar_dataframe(campo = None, filtro = None, excluir_indice = False, ascendente = False):
    df = pd.DataFrame
    # Quando o 'filtro' for diferente de None
    if filtro is not None:
        df = performance.loc[performance['Year'] == filtro]
        # Quando o 'campo' for diferente de None
        if campo is not None:
            df = df.sort_values(campo, ascending=ascendente)
        else:
            df = df.sort_values(['Win pct.', 'Year', 'Games'], ascending=ascendente)
    else:
        if campo is not None:
            df = performance.sort_values(campo, ascending=ascendente)
        else:
            df = performance.sort_values(['Win pct.', 'Year', 'Games'], ascending=ascendente)

    df = df.reset_index()
    df.index = df.index + 1
    # quando o 'excluir_indice' for True(Verdadeiro) 
    if excluir_indice:
        df = df.drop('index', axis=1)

    return df.head(TAM_HEAD)

# DataFrame Base
try:
    df = pd.read_csv(arquivo, sep=';')
except FileNotFoundError:
    print(f"Arquivo {arquivo} não encontrado")
    quit()

# Campos Calculados--------------------------------------------------------------------------------------
df['Win pct.'] = df['Win'] / df['Games']    # percentual de vitórias
df['Yd. Dif'] = df['Off.Yards'] - df['Yards.Allowed'] # Diferença yds anotadas - permitidas
df['TD Dif'] = df['Off.TDs'] - df['Off.TDs.Allowed'] # Diferença TD anotados - permitidos

df['Yds/Game'] = df['Off.Yards'] / df['Games'] # Yds por jogo
df['Yds/Game Allowed'] = df['Yards.Allowed'] / df['Games'] # Yds permitidas por jogo

df['TD/Game'] = df['Off.TDs'] / df['Games'] # TD por jogo
df['TD/Game Allowed'] = df['Off.TDs.Allowed'] / df['Games'] # TD permitidos por jogo

# Dataframe transformado 
performance = df[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.', 
                'Off.Yards','Yards.Allowed', 'Yd. Dif',
                'Off.TDs', 'Off.TDs.Allowed', 'TD Dif',  
                'Yds/Game',  'Yds/Game Allowed',
                'TD/Game',  'TD/Game Allowed']]
#Laço principal
while True:
    limpa_tela()
    # Menu
    print("-------------------------------------------")
    print("1.Campanhas")
    print("2.Campanhas por temporada")
    print("3.TOP 20 de Performance (Yds)")
    print("4.TOP 20 de Performance (TD)")
    print("5.Top 20 de Performance por Temporada (Yds)")
    print("6.Top 20 de Performance por Temporada (TD)")
    print("0.Sair")
    print("-------------------------------------------")
    try:
        op = int(input("Opção: "))
    except:
        input("Opção Inválida")
        continue
    
    match op:
        case 1: #Campanhas-----------------------------------------------------------------------------------------------
            limpa_tela()
            print("-------------------")
            print("Top 20 de Campanhas")
            print("-------------------")
            ascendente = ordenar_menu() # retorna True ou False e será usado para ordenar ascendetnte ou descendente
            campanha = transformar_dataframe(ascendente=ascendente) # Retorna um Dataframe
            limpa_tela()
            print(f"Campo Ordenado: Win pct. Ascendente: {ascendente}\n")
            print(campanha[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.']])
            input("\n\nPressione ENTER para continuar...")
        case 2: # Campanha por temporada---------------------------------------------------------------------------------
            limpa_tela()
            # Tenta informar o ano. Caso seja Nulo retornará o último ano (2023)
            try:
                year = int(input("Informe a Temporada Desejada: ")) # Filtro por Temporada
            except ValueError:
                year = 2023

            print("------------------------------")
            print("Top 20 Campanhas por Temporada")
            print("------------------------------")
            ascendente = ordenar_menu() # retorna True ou False e será usado para ordenar ascendetnte ou descendente
            campanha_temp = transformar_dataframe(filtro=year, ascendente=ascendente) # Retorna um Dataframe
            limpa_tela()
            print(f"Campo Ordenado: Win pct. Ascendente: {ascendente}\n")
            print(campanha_temp[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.']])
            input("\n\nPressione ENTER para continuar...")
        case 3: # TOP 20 de Performance (Yds)----------------------------------------------------------------------------
            limpa_tela()
            print("---------------------------")
            print("Top 20 de Performance (Yds)")
            print("---------------------------")
            ascendente = ordenar_menu() # retorna True ou False e será usado para ordenar ascendetnte ou descendente
            campo = ordenar_campo_yd() # retorna o campo a ser ordenado
            if campo == 'Yds/Game Allowed': # Se esse for o campo inverte o valor de ascendente abaixo
                ascendente = not ascendente
            top_20_yds = transformar_dataframe(campo=campo, excluir_indice=True, ascendente=ascendente) # Retorna um Dataframe
            limpa_tela()
            print(f"Campo Ordenado: {campo}. Ascendente: {ascendente}\n")
            print(top_20_yds[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.', 
                            'Off.Yards','Yards.Allowed', 'Yd. Dif',  
                            'Yds/Game',  'Yds/Game Allowed']])
            input("\n\nPressione ENTER para continuar...")
        case 4: # TOP 20 de Performance (TD)-----------------------------------------------------------------------------
            limpa_tela()
            print("--------------------------")
            print("Top 20 de Performance (TD)")
            print("--------------------------")
            ascendente = ordenar_menu() # retorna True ou False e será usado para ordenar ascendetnte ou descendente
            campo = ordenar_campo_td() # retorna o campo a ser ordenado
            if campo ==  'TD/Game Allowed': # Se esse for o campo inverte o valor de ascendente abaixo
                ascendente = not ascendente
            top_20_td = transformar_dataframe(campo=campo, excluir_indice=True, ascendente=ascendente) # Retorna um Dataframe
            limpa_tela()
            print(f"Campo Ordenado: {campo}. Ascendente: {ascendente}\n")
            print(top_20_td[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.', 
                            'Off.TDs', 'Off.TDs.Allowed', 'TD Dif', 
                            'TD/Game', 'TD/Game Allowed']])
            input("\n\nPressione ENTER para continuar...")
        case 5: # TOP 20 de Performance por Temporada (Yds)--------------------------------------------------------------
            limpa_tela()
            # Tenta informar o ano. Caso seja Nulo retornará o último ano (2023)
            try:
                year = int(input("Informe a Temporada Desejada: ")) # Filtro por Temporada
            except ValueError:
                year = 2023

            print("-----------------------------------------")
            print("Top 20 de Performance por Temporada (Yds)")
            print("-----------------------------------------")
            ascendente = ordenar_menu() # retorna True ou False e será usado para ordenar ascendetnte ou descendente
            campo = ordenar_campo_yd() # retorna o campo a ser ordenado
            if campo == 'Yds/Game Allowed': # Se esse for o campo inverte o valor de ascendente abaixo
                ascendente = not ascendente
            top_20_yds_temp = transformar_dataframe(campo=campo, filtro=year, excluir_indice=True, ascendente=ascendente) # Retorna um Dataframe
            limpa_tela()
            print(f"Campo Ordenado: {campo}. Ascendente: {ascendente}\n")
            print(top_20_yds_temp[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.', 
                                'Off.Yards', 'Yards.Allowed', 'Yd. Dif',
                                'Yds/Game',  'Yds/Game Allowed']])
            input("\n\nPressione ENTER para continuar...")
        case 6: # TOP 20 de Performance por Temporada (TD)---------------------------------------------------------------
            limpa_tela()
            # Tenta informar o ano. Caso seja Nulo retornará o último ano (2023)
            try:
                year = int(input("Informe a Temporada Desejada: ")) # Filtro por Temporada
            except ValueError:
                year = 2023

            print("----------------------------------------")
            print("Top 20 de Performance por Temporada (TD)")
            print("----------------------------------------")
            ascendente = ordenar_menu() # retorna True ou False e será usado para ordenar ascendetnte ou descendente
            campo = ordenar_campo_td() # retorna o campo a ser ordenado
            if campo == 'TD/Game Allowed': # Se esse for o campo inverte o valor de ascendente abaixo
                ascendente = not ascendente
            top_20_td_temp = transformar_dataframe(campo=campo, filtro=year, excluir_indice=True, ascendente=ascendente) # Retorna um Dataframe
            limpa_tela()
            print(f"Campo Ordenado: {campo}. Ascendente: {ascendente}\n")
            print(top_20_td_temp[['Year','Team', 'Conference', 'Games', 'Win', 'Loss', 'Win pct.', 
                                'Off.TDs', 'Off.TDs.Allowed', 'TD Dif', 
                                'TD/Game', 'TD/Game Allowed']])
            input("\n\nPressione ENTER para continuar...")
        case 0: # Sai do Programa-----------------------------------------------------------------------------------------
            break
        case _:
            continue

print("Saindo...")
