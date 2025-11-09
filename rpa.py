import logging
import keyboard
import time
from utils import carregar_configuracao, processar_planilha_ativa
from automacao_interface import preencher_formulario

# --- Configuração de Logging ---
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Log para arquivo
file_handler = logging.FileHandler("automacao_background.log", "w", "utf-8")
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# Log para console
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

# --- Variável de Controle Global ---
# Evita que a automação seja acionada múltiplas vezes se o usuário pressionar o atalho repetidamente.
automacao_em_execucao = False

def trigger_automacao(config):
    """
    Esta função é chamada quando o atalho de teclado é pressionado.
    Ela orquestra todo o fluxo da automação.
    """
    global automacao_em_execucao
    if automacao_em_execucao:
        logging.warning("Automação já está em execução. Aguarde a conclusão.")
        return

    automacao_em_execucao = True
    logging.info("==================================================")
    logging.info("Atalho pressionado! Iniciando a automação...")

    try:
        # 1. Obter dados da planilha Excel atualmente aberta
        dados_processados = processar_planilha_ativa(config)

        # 2. Se os dados foram obtidos, iniciar a automação da interface
        if dados_processados:
            ui_config = config.get("ui_config")
            if ui_config:
                logging.info("Dados extraídos com sucesso. Iniciando preenchimento no sistema Domínio...")
                preencher_formulario(dados_processados, ui_config)
            else:
                logging.error("A seção 'ui_config' não foi encontrada no config.json.")
        else:
            logging.error("Não foi possível extrair dados da planilha. A automação foi interrompida.")

    except Exception as e:
        logging.critical(f"Ocorreu um erro crítico e inesperado durante a automação: {e}")

    finally:
        logging.info("Automação concluída. Aguardando próximo atalho...")
        logging.info("==================================================")
        automacao_em_execucao = False

def main():
    """
    Função principal. Carrega a configuração e fica escutando o atalho de teclado.
    """
    logging.info("Serviço de Automação RPA iniciado em segundo plano.")
    logging.info("Pressione 'Ctrl+Alt+A' com a planilha do Excel em foco para iniciar os lançamentos.")
    logging.info("Para encerrar o serviço, feche esta janela.")

    config = carregar_configuracao("config.json")

    if not config:
        logging.error("Falha ao carregar a configuração. O serviço não pode continuar.")
        time.sleep(10)
        return

    # Cria uma função parcial que já inclui o objeto 'config'
    # Isso é necessário para passar argumentos para a função de callback do keyboard
    callback_com_config = lambda: trigger_automacao(config)

    # Registra o atalho global
    keyboard.add_hotkey('ctrl+alt+a', callback_com_config)

    # Mantém o script rodando para escutar o atalho
    keyboard.wait()

if __name__ == '__main__':
    main()
