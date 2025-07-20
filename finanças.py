import streamlit as st  # cria a interface com streamlit
import pandas as pd  # tratamentos de dados
from db import inserir_transacao, listar_transacoes  # funções de acesso para o mysql
import io  # manipula arquivos em memoria

st.title("Controle Financeiro")

with st.form("form_transacao"):
    # Campo de seleção única para o tipo de transação
    tipo = st.radio("Tipo", ["receita", "despesa"], horizontal=True)
    # Campo de texto para categoria da transação
    categoria = st.text_input(
        "Categoria", placeholder="Ex: alimentação, salário, lazer"
    )
    # Campo numérico para o valor da transação obrigando valor mínimo
    valor = st.number_input("Valor (R$)", min_value=1.00, format="%.2f")
    # Campo de texto para descrição
    descricao = st.text_input("Descrição (opcional)", placeholder="Ex: Lanche ")
    # Botão de envio
    enviar = st.form_submit_button("Salvar Transação")

    if enviar:
        if categoria and valor > 0:
            inserir_transacao(tipo, categoria, valor, descricao)
            st.success("Transação salva com sucesso!")
        else:
            st.warning("Preencha todos os campos obrigatórios.")

st.divider()

st.subheader("Transações Registradas")  # visualiza as transações feitas

transacoes = listar_transacoes()

if transacoes:  # verifica se existe alguma transação
    # converte para DataFrame
    df = pd.DataFrame(
        transacoes,
        columns=["ID", "Tipo", "Categoria", "Valor (R$)", "Descrição", "Data"],
    )
    # atualiza a coluna "Data" com o formato desejado
    df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%y %H:%M")

    # exibe o dataframe
    st.dataframe(df, use_container_width=True)

    # Botão para download do Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Transações')
        # Não precisa chamar writer.save() ou writer.close() aqui

    processed_data = output.getvalue()

    st.download_button(
        label="⬇️ Baixar transações em Excel",
        data=processed_data,
        file_name="transacoes.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # calculo total
    total_receitas = df[df["Tipo"] == "receita"]["Valor (R$)"].sum()
    total_despesas = df[df["Tipo"] == "despesa"]["Valor (R$)"].sum()
    saldo = total_receitas - total_despesas

    st.divider()

    # Exibe o total

    st.metric("📈 Total de Receitas", f"R$ {total_receitas:,.2f}")
    st.metric("📉 Total de Despesas", f"R$ {total_despesas:,.2f}")
    st.metric("💼 Saldo Atual", f"R$ {saldo:,.2f}", delta_color="normal")

else:
    st.info("Nenhuma transação registrada ainda.")
