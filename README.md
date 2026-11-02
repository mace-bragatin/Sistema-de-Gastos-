APRESENTAÇÃO DO SISTEMA DE GASTOS

giovanna — Introdução, configurações e armazenamento

TEMPO: 0:00 – 1:15

Bom dia! Nosso grupo desenvolveu um Sistema de Controle de Gastos Pessoais utilizando python

O objetivo do nosso projeto é permitir que o usuário organize suas despesas, acompanhe seus gastos e saiba quais contas já foram pagas e quais ainda estão em aberto.

Começando pela primeira parte do código, temos a importação da biblioteca OS, que utilizamos para trabalhar com arquivos e localizar a pasta onde o programa está salvo.

Depois, definimos alguns limites, como o máximo de caracteres para as descrições e categorias.

Em seguida, criamos cinco listas: descrições, valores, categorias, datas e pagas. Cada uma armazena um tipo de informação, mas todas trabalham juntas. Por exemplo, a primeira posição de cada lista representa a mesma despesa.

Também criamos funções para mostrar os menus e receber as informações digitadas pelo usuário.

Essa organização permite que o sistema funcione de maneira mais simples e organizada.



luiz - Cadastro, listagem, remoção e atualização

TEMPO: 1:15 – 2:30

Agora vou explicar as primeiras funcionalidades do nosso sistema.

A primeira é o cadastro de despesas. Nela, o usuário informa a descrição, o valor, a categoria e a data. Essas informações são adicionadas às listas por meio do comando append.

Depois temos a função de listar despesas, que apresenta todas as informações em uma tabela organizada.

Também é possível remover despesas. Para isso, o usuário escolhe uma delas e confirma a exclusão. Utilizamos o comando pop para retirar as informações das listas.

Outra funcionalidade é a atualização, que permite modificar a descrição, o valor, a categoria ou a data de uma despesa já cadastrada.

Um detalhe importante é que, tanto na remoção quanto no cadastro, precisamos manter as cinco listas sincronizadas, para que cada informação continue pertencendo à despesa correta.

Assim, essas funções permitem que o usuário tenha controle sobre os dados cadastrados.




nicolah - Pagamento, relatórios, busca e ordenação

TEMPO: 2:30 – 3:45

Na terceira parte, temos funcionalidades que ajudam o usuário a analisar e organizar melhor seus gastos.

Primeiro, temos a opção de marcar uma despesa como paga. Utilizamos os valores booleanos True e False para identificar se ela foi paga ou continua em aberto.

Depois temos a função de relatório, que apresenta informações como o total de despesas, o valor total gasto, quanto já foi pago, quanto ainda está em aberto, a média dos gastos e as maiores e menores despesas.

Também desenvolvemos uma ferramenta de busca, que permite encontrar despesas utilizando parte da descrição ou da categoria.

Por último, temos a listagem ordenada, que permite organizar as despesas por valor ou por data.

Para essa organização, utilizamos o algoritmo Selection Sort, que procura o menor ou maior elemento e o coloca na posição correta.

Essas funções tornam o sistema mais útil para acompanhar os gastos pessoais.




cecília - Salvamento, carregamento e conclusão

TEMPO: 3:45 – 5:00

Para finalizar, vou explicar como funciona o armazenamento das informações e o funcionamento geral do programa.

Criamos uma função chamada salvar despesas, que grava todas as informações em um arquivo de texto chamado despesas.txt.

Também temos a função carregar despesas, que recupera os dados salvos quando o programa é iniciado novamente. Dessa forma, as informações não precisam ser cadastradas novamente toda vez que o sistema é aberto.

No final do código, temos a função main, que é responsável por iniciar o programa, carregar os dados, mostrar o menu e direcionar o usuário para a funcionalidade escolhida.

O sistema continua funcionando por meio de um laço de repetição até que o usuário escolha a opção de sair.

Concluindo, nosso projeto reúne diferentes recursos da programação em Python para criar uma ferramenta de organização financeira, permitindo cadastrar, consultar, atualizar, remover e analisar despesas de maneira prática.

Obrigado pela atenção!
