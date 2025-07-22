import streamlit as st  # cria a interface com streamlit
import pandas as pd  # tratamentos de dados
from db import (
    inserir_transacao,
    listar_transacoes,
    deletar_transacao_por_id,
    deletar_todas_transacoes,
)  # funções do mysql
import io  # manipula arquivos em memória

st.title("Controle Financeiro")

# Formulário para cadastrar uma nova transação
with st.form("form_transacao"):
    tipo = st.radio("Tipo", ["receita", "despesa"], horizontal=True)
    categoria = st.text_input(
        "Categoria", placeholder="Ex: alimentação, salário, lazer"
    )
    valor = st.number_input("Valor (R$)", min_value=1.00, format="%.2f")
    descricao = st.text_input("Descrição (opcional)", placeholder="Ex: Lanche ")
    enviar = st.form_submit_button("Salvar Transação")

    if enviar:
        if categoria and valor > 0:
            inserir_transacao(tipo, categoria, valor, descricao)
            st.rerun()  # Atualiza a página
        else:
            st.warning("Preencha todos os campos obrigatórios.")

st.divider()

st.subheader("Transações Registradas")

transacoes = listar_transacoes()

if transacoes:
    df = pd.DataFrame(
        transacoes,
        columns=["ID", "Tipo", "Categoria", "Valor (R$)", "Descrição", "Data"],
    )
    df["Data"] = pd.to_datetime(df["Data"]).dt.strftime("%d/%m/%y %H:%M")


    for index, row in df.iterrows():
        cols = st.columns([1, 1, 1, 1, 2, 2, 1])
        cols[0].write(row["ID"])
        cols[1].write(row["Tipo"])
        cols[2].write(row["Categoria"])
        cols[3].write(f"R$ {row['Valor (R$)']:.2f}")
        cols[4].write(row["Descrição"])
        cols[5].write(row["Data"])
        if cols[6].button("Excluir", key=f"del_{row['ID']}"):
            try:
                deletar_transacao_por_id(row["ID"])
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao excluir transação: {e}")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Transações")
    processed_data = output.getvalue()

    st.download_button(
        label="⬇️ Baixar transações em Excel",
        data=processed_data,
        file_name="transacoes.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    total_receitas = df[df["Tipo"] == "receita"]["Valor (R$)"].sum()
    total_despesas = df[df["Tipo"] == "despesa"]["Valor (R$)"].sum()
    saldo = total_receitas - total_despesas

    st.divider()

    st.metric("📈 Total de Receitas", f"R$ {total_receitas:,.2f}")
    st.metric("📉 Total de Despesas", f"R$ {total_despesas:,.2f}")
    st.metric("💼 Saldo Atual", f"R$ {saldo:,.2f}", delta_color="normal")

    st.divider()

    with st.expander("⚠️ Apagar TODAS as transações"):
        confirmar = st.checkbox("Tenho certeza que desejo apagar tudo.")
        if st.button("Deletar TODAS as receitas e despesas", disabled=not confirmar):
            deletar_todas_transacoes()
            st.rerun()

else:
    st.info("Nenhuma transação registrada ainda.")
