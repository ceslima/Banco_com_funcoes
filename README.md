Sistema Bancário em Python (Console Application)
Este projeto é uma simulação de um sistema bancário desenvolvida em Python, executada inteiramente em um ambiente de linha de comando (CLI). A aplicação permite gerenciar contas de usuários e realizar operações financeiras básicas, com uma distinção clara entre as funcionalidades de um Administrador e de um Usuário da conta.
Visão Geral do Projeto
O sistema foi construído de forma procedural e modular, com funções específicas para cada operação. Ele utiliza um arquivo banco_dados.json para persistir todos os dados, incluindo informações de usuários, senhas, saldos e históricos de transações. A aplicação possui um fluxo de login que direciona o acesso para dois painéis distintos, cada um com suas próprias permissões e funcionalidades.
Funcionalidades Implementadas
Painel do Administrador
O acesso de administrador é feito com credenciais pré-definidas no sistema. Suas responsabilidades são focadas no gerenciamento de contas de usuários.
 * Login Seguro: Acesso com usuário e senha específicos para o administrador (ceslima / 12345).
 * Criação de Contas: Cadastro de novos usuários, solicitando nome e definindo uma senha. O número da conta e um ID único são gerados automaticamente.
 * Listagem de Contas: Visualização de uma lista com todas as contas cadastradas, exibindo nome do titular, número da conta e saldo atual.
 * Exclusão Segura de Contas: Permite deletar uma conta existente, mas apenas se o saldo for zero. Uma etapa de confirmação, mostrando os dados da conta, é exigida para prevenir exclusões acidentais.
Painel do Usuário
O usuário acessa o sistema com o número da conta e a senha cadastrada pelo administrador. Todas as operações são vinculadas à sua própria conta.
 * Login de Usuário: Autenticação via número da conta e senha pessoal. A digitação da senha é oculta para maior segurança.
 * Depósitos: Adição de valores positivos ao saldo da conta.
 * Saques: Retirada de valores, sujeita a três regras de negócio:
   * O valor do saque não pode exceder o saldo disponível.
   * Limite de 3 saques diários.
   * Limite de R$ 500,00 por saque.
 * Extrato Detalhado: Consulta do histórico de todas as transações (depósitos e saques), com data, hora e valor de cada operação, além do saldo final.
 * Logout: Encerramento da sessão do usuário de forma segura.
Estrutura de Dados
O estado completo do banco é salvo no arquivo banco_dados.json. Este arquivo contém uma lista, onde cada item é um dicionário representando uma conta com a seguinte estrutura:
