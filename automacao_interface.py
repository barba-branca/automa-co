# automacao_interface.py
import time
from pywinauto.application import Application
import logging

def _find_control(main_dlg, selector_config):
    """
    Função auxiliar para encontrar um controle (widget) na janela.
    Constrói os argumentos para `child_window` dinamicamente, ignorando valores nulos.
    """
    if not selector_config:
        raise ValueError("Configuração de seletor para o controle está vazia.")

    # Filtra apenas os seletores que não são nulos (None)
    kwargs = {key: value for key, value in selector_config.items() if value is not None}

    if not kwargs:
        raise ValueError(f"Configuração de seletor {selector_config} não possui valores válidos.")

    logging.debug(f"Procurando controle com os seguintes critérios: {kwargs}")
    return main_dlg.child_window(**kwargs)

def preencher_formulario(dados, ui_config):
    """
    Automatiza o preenchimento do formulário com base nas configurações da UI.

    Args:
        dados (list): Lista de dicionários, cada um representando um lançamento.
        ui_config (dict): Dicionário com os seletores e títulos da interface.
    """

    titulo_app_principal = ui_config.get("titulo_app_principal")
    titulo_janela_lancamentos = ui_config.get("titulo_janela_lancamentos")
    seletores = ui_config.get("seletores", {})

    if not all([titulo_app_principal, titulo_janela_lancamentos, seletores]):
        logging.error("A seção 'ui_config' no config.json está incompleta ou ausente.")
        return

    try:
        logging.info(f"Conectando à aplicação principal: '{titulo_app_principal}'...")
        app = Application(backend="uia").connect(title_re=f".*{titulo_app_principal}.*", timeout=15)

        logging.info(f"Buscando a janela de lançamentos: '{titulo_janela_lancamentos}'...")
        main_dlg = app.window(title=titulo_janela_lancamentos)
        main_dlg.set_focus()
        logging.info("Conectado com sucesso à janela de lançamentos.")

    except Exception as e:
        logging.error(f"Não foi possível encontrar a janela '{titulo_janela_lancamentos}'.")
        logging.error("Verifique se o sistema está aberto e se a janela correta está na tela.")
        logging.error(f"Detalhe do erro: {e}")
        return

    for i, registro in enumerate(dados):
        logging.info(f"Processando lançamento {i+1}/{len(dados)}: {registro}")

        try:
            # Encontra os controles usando a configuração do config.json
            campo_debitar = _find_control(main_dlg, seletores.get("campo_debito"))
            campo_creditar = _find_control(main_dlg, seletores.get("campo_credito"))
            campo_valor = _find_control(main_dlg, seletores.get("campo_valor"))
            campo_historico = _find_control(main_dlg, seletores.get("campo_historico"))
            botao_incluir = _find_control(main_dlg, seletores.get("botao_incluir"))

            # Preenche os campos
            campo_debitar.set_edit_text(str(registro.get('debito', '')))
            campo_debitar.type_keys("{F2}")
            logging.info(f"Campo 'Debitar' preenchido e F2 pressionado.")
            time.sleep(1)

            campo_creditar.set_edit_text(str(registro.get('credito', '')))
            campo_creditar.type_keys("{F2}")
            logging.info(f"Campo 'Creditar' preenchido e F2 pressionado.")
            time.sleep(1)

            campo_valor.set_edit_text(str(registro.get('valor', '')))
            logging.info(f"Campo 'Valor' preenchido.")

            campo_historico.set_edit_text(str(registro.get('historico', '')))
            logging.info(f"Campo 'Histórico' preenchido.")

            botao_incluir.click()
            logging.info("Botão 'Incluir' clicado.")

            time.sleep(2)

        except Exception as e:
            logging.warning(f"Não foi possível processar o lançamento {i+1}: {registro}")
            logging.warning("Verifique se os seletores no 'config.json' correspondem à interface do sistema.")
            logging.warning(f"Detalhe do erro: {e}")
            continue

    logging.info("Automação do preenchimento de lançamentos concluída.")
