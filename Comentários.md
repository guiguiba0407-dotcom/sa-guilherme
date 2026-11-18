# Devolutiva formativa — Atividade 01 da SA

**Estudante:** Guilherme  
**Turma:** Rio Negrinho — Tarde  
**Unidade Curricular:** Programação de Aplicativos  
**Projeto implementado:** Gerenciamento de estoque  
**Código analisado:** `codigo/app.py`  
**Referência:** Situação de Aprendizagem nº 1 — *Da Ideia ao Código*

## O que você já conseguiu desenvolver

Guilherme, seu programa apresenta uma solução inicial de controle de estoque com cadastro, listagem, movimentação e exclusão de produtos. Você aplicou funções, estruturas condicionais, repetição e tratamento de entradas, além de experimentar a gravação das informações em um banco SQLite.

Pontos positivos identificados:

- Organizou o código em **funções com responsabilidades identificáveis**, como `conectar()`, `cadastrar_produto()`, `listar_produtos()`, `movimentar_estoque()` e `excluir_produto()`.
- Implementou as operações de **cadastro, consulta, alteração de quantidade e exclusão** de produtos.
- Utilizou **comandos SQL parametrizados**, evitando montar consultas com os valores digitados pelo usuário.
- Criou verificações para impedir a **saída de uma quantidade maior que o estoque disponível**.
- Tratou erros de conversão numérica com `try/except ValueError` nos campos de quantidade, preço e identificação do produto.
- Incluiu um menu de navegação por teclado e uma função reutilizável para limpar a tela em diferentes sistemas operacionais.
- Utilizou `if __name__ == "__main__":` para iniciar o programa de forma organizada.

## O que precisa ser corrigido

### 1. Corrigir a identificação do projeto no README

No final do `README.md`, o projeto está identificado como **aplicativo de transporte**, mas o programa entregue implementa um **gerenciamento de estoque**. Ambos são temas previstos na Situação de Aprendizagem, porém a documentação precisa corresponder ao sistema desenvolvido.

**Como melhorar:** confirmar o tema escolhido e atualizar o README para que o título, o objetivo e as funcionalidades descritas estejam de acordo com o código entregue. Se o projeto correto for transporte, será necessário esclarecer essa diferença antes de continuar.

### 2. Validar os dados no cadastro de produtos

A função `cadastrar_produto()` recebe nome, quantidade e preço, mas o fluxo de cadastro ainda permite informar **nome vazio, quantidade inicial negativa ou preço negativo**. Essas entradas podem gerar informações incoerentes no estoque.

**Como melhorar:** verificar se o nome contém caracteres além de espaços, se a quantidade é maior ou igual a zero e se o preço é maior ou igual a zero antes de gravar o produto. Caso uma informação seja inválida, informar o problema ao usuário e solicitar a correção.

### 3. Documentar a dependência da biblioteca `keyboard`

O programa importa a biblioteca externa `keyboard` para capturar teclas, mas o README não apresenta instruções específicas de instalação. Assim, a aplicação pode não iniciar em um computador onde essa biblioteca não esteja instalada. A captura global de teclas também pode apresentar restrições em alguns ambientes.

**Como melhorar:** registrar a dependência e as instruções de instalação no README e testar o programa no ambiente em que será apresentado. Considere também uma alternativa baseada em `input()` caso a captura de teclas não seja compatível.

## Oportunidades de melhoria

### 4. Incluir comentários explicativos e docstrings

O código está dividido em funções, mas praticamente não contém comentários que expliquem as decisões e regras de negócio. Uma pessoa que não participou do desenvolvimento precisa descobrir o funcionamento apenas pela leitura das instruções.

**Como melhorar:** adicionar docstrings curtas explicando a finalidade das funções e comentários nos trechos que exigem mais interpretação, como a alteração de quantidades, a seleção horizontal de produtos e o controle das operações no banco. Evite comentários que apenas repitam uma linha simples de código.

### 5. Melhorar os textos da interface

Na seleção horizontal de produtos, a tela mostra o título `Documentos / Itens`, embora o sistema trabalhe com estoque.

**Como melhorar:** utilizar termos consistentes, como `Produtos disponíveis` ou `Selecione um produto`, e manter mensagens claras para situações de sucesso e erro.

### 6. Organizar os testes do programa

O código já trata algumas situações inválidas, mas não encontrei arquivos de testes específicos no repositório. É importante confirmar que as operações funcionam em sequência e que as informações permanecem corretas.

**Como melhorar:** executar e registrar, pelo menos, os seguintes cenários:

1. Cadastrar um produto com dados válidos e conferir sua exibição na listagem.
2. Tentar cadastrar um produto com nome vazio, quantidade negativa e preço negativo.
3. Tentar cadastrar um produto com nome repetido.
4. Registrar entrada e saída de unidades, incluindo uma saída maior que o saldo.
5. Tentar alterar ou excluir um produto inexistente.
6. Reiniciar o programa e verificar se os produtos cadastrados continuam disponíveis.

### 7. Continuar organizando a evolução da aplicação

A integração com SQLite é uma iniciativa positiva, mas **não era uma exigência da Atividade 01**, cujo foco estava na construção inicial do código Python. Na continuidade do projeto, vale separar gradualmente a interação com o usuário, as regras de negócio e as operações de armazenamento. Isso facilitará a manutenção e a futura criação da interface.

## Prioridades para a próxima versão

1. **Alinhar o README ao projeto efetivamente desenvolvido.**
2. **Impedir o cadastro de produtos com informações inválidas.**
3. **Documentar a instalação da biblioteca `keyboard` e a execução do programa.**
4. **Acrescentar comentários úteis às funções e regras importantes.**
5. **Executar os testes recomendados e registrar os resultados.**

## Mensagem final

Guilherme, seu trabalho demonstra que você já consegue organizar funcionalidades em Python e aplicar conceitos de entrada de dados, condicionais, repetição, funções e manipulação de informações. A implementação do cadastro e da movimentação de estoque mostra uma boa iniciativa para construir um programa com utilidade prática.

Agora, procure dar atenção especial à **validação dos dados**, à **clareza da documentação** e à **consistência entre o tema do projeto e o código entregue**. Essas melhorias vão tornar seu sistema mais confiável e mais fácil de compreender. Continue desenvolvendo o projeto por etapas e registrando sua evolução no GitHub.
