import os

LIMITE_DESCRICAO = 150
LIMITE_CATEGORIA = 50
# Salva na MESMA pasta deste arquivo, e nao na pasta em que o terminal foi aberto
PASTA_DO_PROGRAMA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DESPESAS = os.path.join(PASTA_DO_PROGRAMA, "despesas.txt")
SEPARADOR = ";"
DATA_VAZIA_NO_FIM = "9999-99-99"  # usada só para jogar as datas vazias para o fim

descricoes = []
valores = []
categorias = []
datas = []
pagas = []


# --- Menus -------------------------------------------------------------

def mostrar_menu():
    print("\n" + "=" * 45)
    print("   SISTEMA DE CONTROLE DE GASTOS PESSOAIS")
    print("=" * 45)
    print("1. Cadastrar despesa")
    print("2. Listar despesas")
    print("3. Remover despesa")
    print("4. Atualizar despesa")
    print("5. Marcar despesa como paga")
    print("6. Relatório")
    print("7. Buscar despesa (descrição ou categoria)")
    print("8. Listar ordenado (por valor ou por data)")
    print("9. Salvar despesas em arquivo")
    print("0. Sair")
    print("=" * 45)


def mostrar_titulo(titulo):
    print("\n" + "=" * 45)
    # Centraliza o título: metade dos espaços que sobram vai na frente dele
    print(espacos((45 - len(titulo)) // 2) + titulo)
    print("=" * 45)

def ler_opcao(mensagem="Escolha uma opção: "):
    """Devolve o número digitado, ou -1 se não for número."""
    try:
        return int(input(mensagem))
    except ValueError:
        return -1


def ler_valor(mensagem):
    """Repete até receber um número maior que zero."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        if texto.startswith("-"):
            print("Erro: o valor precisa ser maior que zero.")
            continue
        # Só sobram dígitos quando tiramos os pontos de um número como "25.90"
        if texto == "" or not texto.replace(".", "").isdigit():
            print("Erro: digite apenas números no valor (ex: 25.90).")
            continue
        try:
            valor = float(texto)
        except ValueError:
            print("Erro: digite apenas números no valor (ex: 25.90).")
            continue
        if valor <= 0:
            print("Erro: o valor precisa ser maior que zero.")
        else:
            return valor


def ler_texto(mensagem, limite, obrigatorio):
    """Repete até o texto não estar vazio (se obrigatório) e caber no limite."""
    while True:
        texto = input(mensagem).strip()
        if obrigatorio and texto == "":
            print("Erro: este campo não pode ficar vazio.")
        elif len(texto) > limite:
            print(f"Erro: o texto passou de {limite} caracteres ({len(texto)}).")
        elif SEPARADOR in texto:
            print(f"Erro: não use o caractere '{SEPARADOR}'.")
        else:
            return texto


def data_valida(data):
    """Confere se o texto está no formato AAAA-MM-DD e se a data existe."""
    partes = data.split("-")
    if len(partes) != 3:
        return False
    ano = partes[0]
    mes = partes[1]
    dia = partes[2]
    if len(ano) != 4 or len(mes) != 2 or len(dia) != 2:
        return False
    if not (ano.isdigit() and mes.isdigit() and dia.isdigit()):
        return False
    ano = int(ano)
    mes = int(mes)
    dia = int(dia)
    if mes < 1 or mes > 12:
        return False
    dias_no_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
        dias_no_mes[1] = 29  # ano bissexto
    return dia >= 1 and dia <= dias_no_mes[mes - 1]


def normalizar_data(data):
    """Transforma o que o usuário digitou no formato interno AAAA-MM-DD.

    Aceita o jeito brasileiro (17/09/2026, 17-09-2026, 17.09.2026 ou 17092026)
    e também AAAA-MM-DD, caso alguém digite a data já no formato interno.
    """
    numeros = ""
    for caractere in data:
        if caractere.isdigit():
            numeros += caractere
        elif caractere not in "-/. ":
            return data  # tem letra ou símbolo estranho: deixa como está para dar erro
    if len(numeros) != 8:
        return data
    # Se o primeiro pedaço tem 4 dígitos, já veio como AAAA-MM-DD
    primeiro = data.replace("/", "-").replace(".", "-").replace(" ", "-").split("-")[0]
    if len(primeiro) == 4:
        return numeros[0:4] + "-" + numeros[4:6] + "-" + numeros[6:8]
    # Caso normal: o usuário digitou DD/MM/AAAA
    return numeros[4:8] + "-" + numeros[2:4] + "-" + numeros[0:2]


def formatar_data(data):
    """Mostra a data do jeito brasileiro: 2026-09-17 vira 17/09/2026."""
    if data == "":
        return "-"
    partes = data.split("-")
    if len(partes) != 3:
        return data
    return partes[2] + "/" + partes[1] + "/" + partes[0]


def ler_data(mensagem):
    """Data é opcional: vazio é aceito. Repete se estiver no formato errado."""
    while True:
        data = normalizar_data(input(mensagem).strip())
        if data == "" or data_valida(data):
            return data
        print("Erro: data inválida. Digite DD/MM/AAAA (ex: 17/09/2026).")


def confirmar(mensagem):
    resposta = input(mensagem + " (s/n): ").strip().lower()
    return resposta == "s" or resposta == "sim"


# --- Funções reutilizáveis ---------------------------------------------

def lista_vazia():
    if len(descricoes) == 0:
        print("Nenhuma despesa cadastrada.")
        return True
    return False


def escolher_despesa():
    """Pede o número mostrado na lista e devolve o índice interno (ou None)."""
    numero = ler_opcao("Digite o número da despesa (0 para cancelar): ")
    if numero == 0:
        return None
    if numero < 1 or numero > len(descricoes):
        print("Despesa inválida!")
        return None
    return numero - 1  


def texto_status(paga):
    if paga:
        return "PAGA"
    return "EM ABERTO"


def encurtar(texto, tamanho):
    """Corta textos longos para não desalinhar a tabela."""
    if len(texto) > tamanho:
        return texto[:tamanho - 3] + "..."
    return texto


def espacos(quantidade):
    """Devolve a quantidade de espaços pedida (nunca menos que nenhum)."""
    if quantidade <= 0:
        return ""
    return " " * quantidade


def alinhar_esquerda(texto, tamanho):
    """Coloca espaços DEPOIS do texto até ele ocupar o tamanho pedido."""
    return texto + espacos(tamanho - len(texto))


def alinhar_direita(texto, tamanho):
    """Coloca espaços ANTES do texto até ele ocupar o tamanho pedido."""
    return espacos(tamanho - len(texto)) + texto


def mostrar_despesa(numero, i):
    """Mostra a despesa do índice i com o número 'numero' na frente."""
    descricao = encurtar(descricoes[i], 25)
    categoria = categorias[i]
    if categoria == "":
        categoria = "-"  
    categoria = encurtar(categoria, 12)
    data = formatar_data(datas[i])
    valor = f"{valores[i]:.2f}"
    print(alinhar_direita(f"{numero}", 2) + ". "
          + alinhar_esquerda(descricao, 25) + " R$ "
          + alinhar_direita(valor, 9) + "  "
          + alinhar_esquerda(categoria, 12) + " "
          + alinhar_esquerda(data, 10) + "  ["
          + texto_status(pagas[i]) + "]")


def mostrar_tabela(indices):
    """Mostra as despesas na ordem da lista de índices recebida."""
    print(alinhar_direita("Nº", 3) + " "
          + alinhar_esquerda("Descrição", 25) + " "
          + alinhar_direita("Valor", 12) + "  "
          + alinhar_esquerda("Categoria", 12) + " "
          + alinhar_esquerda("Data", 10) + "  Situação")
    print("-" * 85)
    for posicao in range(len(indices)):
        mostrar_despesa(posicao + 1, indices[posicao])


def todos_os_indices():
    """Devolve [0, 1, 2, ...] com uma posição para cada despesa."""
    indices = []
    for i in range(len(descricoes)):
        indices.append(i)
    return indices


# --- 1. Cadastrar ----------------------------------------------------------

def cadastrar_despesa():
    mostrar_titulo("CADASTRAR DESPESA")
    descricao = ler_texto(f"Descrição (até {LIMITE_DESCRICAO} caracteres): ",
                          LIMITE_DESCRICAO, True)
    valor = ler_valor("Valor: R$ ")
    categoria = ler_texto(f"Categoria (opcional, até {LIMITE_CATEGORIA} caracteres): ",
                          LIMITE_CATEGORIA, False)
    data = ler_data("Data DD/MM/AAAA (opcional): ")
    # Um append em cada vetor, para todos continuarem do mesmo tamanho
    descricoes.append(descricao)
    valores.append(valor)
    categorias.append(categoria)
    datas.append(data)
    pagas.append(False)  # toda despesa começa como NÃO paga
    print(f"\nDespesa '{descricao}' cadastrada com sucesso!")


# --- 2. Listar -------------------------------------------------------------

def listar_despesas():
    mostrar_titulo("LISTA DE DESPESAS")
    if lista_vazia():
        return
    mostrar_tabela(todos_os_indices())


# --- 3. Remover ------------------------------------------------------------

def remover_despesa():
    mostrar_titulo("REMOVER DESPESA")
    if lista_vazia():
        return
    mostrar_tabela(todos_os_indices())
    indice = escolher_despesa()
    if indice is None:
        print("Remoção cancelada.")
        return
    descricao = descricoes[indice]
    if not confirmar(f"Tem certeza que deseja remover '{descricao}'?"):
        print("Remoção cancelada.")
        return
    # Remove o mesmo índice de TODOS os vetores, senão eles se desalinham
    descricoes.pop(indice)
    valores.pop(indice)
    categorias.pop(indice)
    datas.pop(indice)
    pagas.pop(indice)
    print(f"Despesa '{descricao}' removida com sucesso!")


# --- 4. Atualizar (um campo de cada vez) -------------------------------------

def mostrar_menu_atualizar():
    print("\n--- Qual campo deseja mudar? ---")
    print("1. Descrição")
    print("2. Valor")
    print("3. Categoria")
    print("4. Data")
    print("0. Cancelar")


def atualizar_despesa():
    mostrar_titulo("ATUALIZAR DESPESA")
    if lista_vazia():
        return
    mostrar_tabela(todos_os_indices())
    indice = escolher_despesa()
    if indice is None:
        print("Atualização cancelada.")
        return
    print()
    mostrar_despesa(indice + 1, indice)
    mostrar_menu_atualizar()
    opcao = ler_opcao()
    if opcao == 1:
        descricoes[indice] = ler_texto("Nova descrição: ", LIMITE_DESCRICAO, True)
    elif opcao == 2:
        valores[indice] = ler_valor("Novo valor: R$ ")
    elif opcao == 3:
        categorias[indice] = ler_texto("Nova categoria (vazio para apagar): ",
                                       LIMITE_CATEGORIA, False)
    elif opcao == 4:
        datas[indice] = ler_data("Nova data DD/MM/AAAA (vazio para apagar): ")
    elif opcao == 0:
        print("Atualização cancelada.")
        return
    else:
        print("Opção inválida! Nada foi alterado.")
        return
    print("Despesa atualizada com sucesso!")
    mostrar_despesa(indice + 1, indice)


# --- Funções de apoio para relatório e ordenação ------------------------------

def dinheiro(valor):
    """Formata o número como dinheiro, sempre com duas casas."""
    return f"{valor:.2f}"


def indices_de(lista):
    """Devolve [0, 1, 2, ...] com uma posição para cada item da lista."""
    indices = []
    for i in range(len(lista)):
        indices.append(i)
    return indices


def somar(indices):
    """Soma os valores das despesas que estão na lista de índices."""
    total = 0.0
    for i in indices:
        total = total + valores[i]
    return total


def ordenar_indices(indices, chaves, crescente=True):
    """Selection Sort: a cada passagem o menor do resto vai para a posição i.

    Guarda o ÍNDICE do escolhido, não o valor, porque é o índice que permite
    a troca depois. As duas listas trocam juntas para continuarem casadas:
    'chaves' diz por qual campo ordenar e 'indices' é o que vai ser usado.
    """
    for i in range(len(indices)):
        indice_do_escolhido = i
        for j in range(i + 1, len(indices)):
            if crescente:
                melhor = chaves[j] < chaves[indice_do_escolhido]
            else:
                melhor = chaves[j] > chaves[indice_do_escolhido]
            if melhor:
                indice_do_escolhido = j
        indices[i], indices[indice_do_escolhido] = indices[indice_do_escolhido], indices[i]
        chaves[i], chaves[indice_do_escolhido] = chaves[indice_do_escolhido], chaves[i]
    return indices


# --- 5. Marcar como paga ----------------------------------------------------

def marcar_como_paga():
    mostrar_titulo("MARCAR DESPESA COMO PAGA")
    if lista_vazia():
        return
    mostrar_tabela(todos_os_indices())
    indice = escolher_despesa()
    if indice is None:
        print("Operação cancelada.")
        return
    descricao = descricoes[indice]
    if pagas[indice]:
        # Já está paga: aqui a única coisa útil é poder desfazer
        if confirmar(f"'{descricao}' já está paga. Voltar para EM ABERTO?"):
            pagas[indice] = False
            print(f"Despesa '{descricao}' voltou para EM ABERTO.")
        else:
            print("Nada foi alterado.")
        return
    pagas[indice] = True
    print(f"Despesa '{descricao}' marcada como PAGA!")


# --- 6. Relatório -------------------------------------------------------------

def indices_por_situacao(paga):
    """Devolve os índices das despesas que estão pagas ou em aberto."""
    indices = []
    for i in range(len(descricoes)):
        if pagas[i] == paga:
            indices.append(i)
    return indices


def nome_categoria(i):
    if categorias[i] == "":
        return "(sem categoria)"
    return categorias[i]


def totais_por_categoria():
    """Devolve duas listas casadas: o nome de cada categoria e o total dela."""
    nomes = []
    totais = []
    for i in range(len(descricoes)):
        nome = nome_categoria(i)
        if nome in nomes:
            posicao = nomes.index(nome)
            totais[posicao] = totais[posicao] + valores[i]
        else:
            nomes.append(nome)
            totais.append(valores[i])
    return nomes, totais


def linha_relatorio(rotulo, texto):
    print(alinhar_esquerda(rotulo, 24) + texto)


def gerar_relatorio():
    mostrar_titulo("RELATÓRIO")
    if lista_vazia():
        return
    quantidade = len(descricoes)
    todas = todos_os_indices()
    em_aberto = indices_por_situacao(False)
    pagas_ = indices_por_situacao(True)
    total = somar(todas)

    linha_relatorio("Despesas cadastradas:", f"{quantidade}")
    linha_relatorio("Total geral:", "R$ " + dinheiro(total))
    linha_relatorio("Total pago:",
                    f"R$ {dinheiro(somar(pagas_))} ({len(pagas_)} despesa(s))")
    linha_relatorio("Total em aberto:",
                    f"R$ {dinheiro(somar(em_aberto))} ({len(em_aberto)} despesa(s))")
    linha_relatorio("Valor médio:", "R$ " + dinheiro(total / quantidade))

    # Maior e menor despesa: uma passada guardando o melhor encontrado até agora
    maior = 0
    menor = 0
    for i in todas:
        if valores[i] > valores[maior]:
            maior = i
        if valores[i] < valores[menor]:
            menor = i
    linha_relatorio("Maior despesa:",
                    f"{descricoes[maior]} (R$ {dinheiro(valores[maior])})")
    linha_relatorio("Menor despesa:",
                    f"{descricoes[menor]} (R$ {dinheiro(valores[menor])})")

    print("\n--- Total por categoria (da maior para a menor) ---")
    nomes, totais = totais_por_categoria()
    # totais[:] é uma cópia, para a ordenação não mexer na lista original
    ordem = ordenar_indices(indices_de(nomes), totais[:], False)
    for posicao in ordem:
        parte = totais[posicao] * 100 / total
        print(alinhar_esquerda(encurtar(nomes[posicao], 24), 24)
              + alinhar_direita("R$ " + dinheiro(totais[posicao]), 14)
              + alinhar_direita(f"({parte:.1f}%)", 10))


# --- 7. Buscar --------------------------------------------------------------

def buscar_despesa():
    mostrar_titulo("BUSCAR DESPESA")
    if lista_vazia():
        return
    termo = ler_texto("Digite parte da descrição ou da categoria: ",
                      LIMITE_DESCRICAO, True).lower()
    encontrados = []
    for i in range(len(descricoes)):
        if termo in descricoes[i].lower() or termo in categorias[i].lower():
            encontrados.append(i)
    if len(encontrados) == 0:
        print(f"Nenhuma despesa encontrada para '{termo}'.")
        return
    print()
    mostrar_tabela(encontrados)
    print(f"{len(encontrados)} despesa(s) | Total: R$ {dinheiro(somar(encontrados))}")


# --- 8. Listar ordenado ------------------------------------------------------

def mostrar_menu_ordenar():
    print("\n--- Ordenar por ---")
    print("1. Valor (do menor para o maior)")
    print("2. Valor (do maior para o menor)")
    print("3. Data (da mais antiga para a mais nova)")
    print("4. Data (da mais nova para a mais antiga)")
    print("0. Cancelar")


def chaves_de_valor(indices):
    chaves = []
    for i in indices:
        chaves.append(valores[i])
    return chaves


def chaves_de_data(indices):
    """Datas AAAA-MM-DD comparadas como texto ficam na ordem certa.
    Quem não tem data recebe DATA_VAZIA_NO_FIM e vai para o fim."""
    chaves = []
    for i in indices:
        if datas[i] == "":
            chaves.append(DATA_VAZIA_NO_FIM)
        else:
            chaves.append(datas[i])
    return chaves


def listar_ordenado():
    mostrar_titulo("LISTAR ORDENADO")
    if lista_vazia():
        return
    mostrar_menu_ordenar()
    opcao = ler_opcao()
    indices = todos_os_indices()
    if opcao == 1:
        ordenar_indices(indices, chaves_de_valor(indices), True)
    elif opcao == 2:
        ordenar_indices(indices, chaves_de_valor(indices), False)
    elif opcao == 3:
        ordenar_indices(indices, chaves_de_data(indices), True)
    elif opcao == 4:
        ordenar_indices(indices, chaves_de_data(indices), False)
    elif opcao == 0:
        print("Operação cancelada.")
        return
    else:
        print("Opção inválida!")
        return
    print()
    mostrar_tabela(indices)


# --- 9. Salvar (e carregar ao abrir o programa) ------------------------------

def salvar_despesas():
    """Grava uma despesa por linha: descrição;valor;categoria;data;paga"""
    with open(ARQUIVO_DESPESAS, "w", encoding="utf-8") as arquivo:
        for i in range(len(descricoes)):
            paga = "1" if pagas[i] else "0"
            arquivo.write(f"{descricoes[i]}{SEPARADOR}{valores[i]:.2f}"
                          f"{SEPARADOR}{categorias[i]}{SEPARADOR}{datas[i]}"
                          f"{SEPARADOR}{paga}\n")
    print(f"{len(descricoes)} despesa(s) salva(s) em '{ARQUIVO_DESPESAS}'.")


def carregar_despesas():
    """Lê o arquivo ao abrir o programa. Linhas com problema são ignoradas."""
    ignoradas = 0
    try:
        with open(ARQUIVO_DESPESAS, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(SEPARADOR)
                if len(dados) != 5:
                    ignoradas = ignoradas + 1
                    continue
                try:
                    valor = float(dados[1])
                except ValueError:
                    ignoradas = ignoradas + 1
                    continue
                if dados[0] == "" or valor <= 0:
                    ignoradas = ignoradas + 1
                    continue
                data = dados[3]
                if data != "" and not data_valida(data):
                    data = ""
                descricoes.append(dados[0])
                valores.append(valor)
                categorias.append(dados[2])
                datas.append(data)
                pagas.append(dados[4] == "1")
    except FileNotFoundError:
        return  # sem arquivo: começa vazio
    print(f"{len(descricoes)} despesa(s) carregada(s) de '{ARQUIVO_DESPESAS}'.")
    if ignoradas > 0:
        print(f"Atenção: {ignoradas} linha(s) inválida(s) do arquivo foram ignoradas.")


# --- Programa principal ------------------------------------------------------

def main():
    carregar_despesas()
    while True:
        mostrar_menu()
        opcao = ler_opcao()
        if opcao == 1:
            cadastrar_despesa()
        elif opcao == 2:
            listar_despesas()
        elif opcao == 3:
            remover_despesa()
        elif opcao == 4:
            atualizar_despesa()
        elif opcao == 5:
            marcar_como_paga()
        elif opcao == 6:
            gerar_relatorio()
        elif opcao == 7:
            buscar_despesa()
        elif opcao == 8:
            listar_ordenado()
        elif opcao == 9:
            salvar_despesas()
        elif opcao == 0:
            if len(descricoes) > 0 and confirmar("Deseja salvar as despesas antes de sair?"):
                salvar_despesas()
            print("\nAté logo!")
            break
        else:
            print("Opção inválida! Escolha um número de 0 a 9.")


if __name__ == "__main__":
    main()
