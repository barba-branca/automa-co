# automacao_interface.py
import time
from pywinauto.application import Application
import logging

def preencher_formulario(dados):
    """
    Automatiza o preenchimento do formulário "Consulta e Lançamentos" no sistema Domínio.

    Args:
        dados (list): Uma lista de dicionários, onde cada dicionário representa um lançamento.
    """

    # Título da janela principal do aplicativo Domínio.
    # Usamos uma correspondência parcial para evitar problemas com a atualização de versões.
    titulo_app_principal = "Domínio Contabilidade Fiscal"

    # Título da janela secundária onde os dados são inseridos.
    titulo_janela_lancamentos = "Consulta e Lançamentos"

    try:
        logging.info(f"Tentando se conectar à aplicação principal: '{titulo_app_principal}'...")
        # Conecta-se à aplicação principal que já deve estar aberta.
        app = Application(backend="uia").connect(title_re=f".*{titulo_app_principal}.*", timeout=15)

        # A partir da aplicação, busca a janela de lançamentos específica.
        main_dlg = app.window(title=titulo_janela_lancamentos)
        main_dlg.set_focus()
        logging.info("Conectado com sucesso à janela 'Consulta e Lançamentos'.")

    except Exception as e:
        logging.error(f"Não foi possível encontrar a janela '{titulo_janela_lancamentos}'.")
        logging.error("Verifique se o sistema Domínio está aberto e se a janela de lançamentos está na tela.")
        logging.error(f"Detalhe do erro: {e}")
        return

    # Loop para processar cada linha de dados (cada lançamento)
    for i, registro in enumerate(dados):
        logging.info(f"Processando lançamento {i+1}/{len(dados)}: {registro}")

        try:
            # --- ATENÇÃO: VERIFIQUE OS IDENTIFICADORES ABAIXO ---
            # Os identificadores (auto_id, title, control_type) podem variar.
            # Use a ferramenta "Inspect.exe" (da Microsoft) para encontrar os valores corretos para os campos
            # da sua versão do sistema Domínio.

            # Exemplo de como encontrar um campo:
            # campo_debitar = main_dlg.child_window(title="Debitar", control_type="Edit")
            # Ou, se tiver o AutomationId:
            # campo_debitar = main_dlg.child_window(auto_id="txtContaDebito", control_type="Edit")

            # Campo Debitar
            # Supondo que o campo de débito tenha o título "Debitar"
            campo_debitar = main_dlg.child_window(title="Debitar", control_type="Edit")
            campo_debitar.set_edit_text(str(registro.get('debito', '')))
            campo_debitar.type_keys("{F2}") # Pressiona F2 para validar a conta
            logging.info(f"Campo 'Debitar' preenchido com '{registro.get('debito', '')}' e F2 pressionado.")
            time.sleep(1)

            # Campo Creditar
            campo_creditar = main_dlg.child_window(title="Creditar", control_type="Edit")
            campo_creditar.set_edit_text(str(registro.get('credito', '')))
            campo_creditar.type_keys("{F2}") # Pressiona F2 para validar a conta
            logging.info(f"Campo 'Creditar' preenchido com '{registro.get('credito', '')}' e F2 pressionado.")
            time.sleep(1)

            # Campo Valor
            # O campo de valor pode não ter um título visível, então buscar por um ID é mais seguro.
            # Este é um palpite, ajuste conforme necessário.
            campo_valor = main_dlg.child_window(auto_id="txtValorLancamento", control_type="Edit")
            campo_valor.set_edit_text(str(registro.get('valor', '')))
            logging.info(f"Campo 'Valor' preenchido com '{registro.get('valor', '')}'.")

            # Campo Histórico
            # Semelhante ao campo Valor, o ID pode ser mais confiável.
            campo_historico = main_dlg.child_window(auto_id="txtHistoricoPadrao", control_type="Edit")
            campo_historico.set_edit_text(str(registro.get('historico', '')))
            logging.info(f"Campo 'Histórico' preenchido com '{registro.get('historico', '')}'.")

            # Botão Incluir
            botao_incluir = main_dlg.child_window(title="Incluir", control_type="Button")
            botao_incluir.click()
            logging.info("Botão 'Incluir' clicado com sucesso.")

            time.sleep(2) # Aguarda um tempo para a interface responder antes do próximo lançamento.

        except Exception as e:
            logging.warning(f"Não foi possível processar o lançamento {i+1}: {registro}")
            logging.warning(f"Erro ao tentar interagir com um dos campos do formulário. Verifique os seletores (title, auto_id).")
            logging.warning(f"Detalhe do erro: {e}")
            # Se ocorrer um erro, pula para o próximo registro.
            continue

    logging.info("Automação do preenchimento de lançamentos concluída.")
