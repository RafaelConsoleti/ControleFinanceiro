# ControleFinanceiro

## Ideia

ControleFinanceiro é uma aplicação web simples desenvolvida em Python utilizando Streamlit para gerenciar finanças pessoais simples.  
Permite registrar receitas e despesas, visualizar o histórico das transações, excluir transações específicas ou todas e baixar o extrato em Excel para melhor controle.

O sistema utiliza o banco MySQL para armazenar os dados de forma fácil e segura.

## Funcionalidades

- Cadastro de transações do tipo receita ou despesa, com categoria, valor e descrição opcional
- Visualização das transações ordenadas da mais recente para a mais antiga
- Exclusão individual de transações
- Exclusão em massa de todas as transações (com dupla confirmação)
- Download das transações em arquivo Excel em modelo (.xlsx)
- Interface simples e responsiva 

## Tecnologias Utilizadas

- Python 3
- Streamlit
- MySQL
- pandas
- mysql-connector-python
- xlsxwriter (para exportar para o Excel)

## Estrutura do Projeto

- finanças.py — interface da aplicação com Streamlit
- db.py — funções para conexão e manipulação do banco MySQL (listar e deletar transações)
- bibliotecas.txt — bibliotecas necessárias para rodar o projeto 

## Requisitos

- Python instalado
- MySQL instalado e configurado conforme seu computador
- Pacotes Python instalados (pip install -r bibliotecas.txt)

