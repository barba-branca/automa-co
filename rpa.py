import pandas as pd
import json
import logging
from utils import detectar_coluna
from automacao_interface import preencher_formulario # <-- 1. IMPORTAÇÃO ADICIONADA

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def processar_planilha(config_path):
    """
    Lê uma planilha, mapeia colunas dinamicamente e retorna os dados.
    """
    try:
        logging.info(f"Carregando arquivo de configuração: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error(f"Arquivo de configuração não encontrado em: {config_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar o JSON em: {config_path}")
        return None

    caminho_planilha = config.get("caminho_planilha")
    colunas_cfg = config.get("colunas")

    if not caminho_planilha or not colunas_cfg:
        logging.error("Configuração incompleta. 'caminho_planilha' e 'colunas' são obrigatórios.")
        return None

    try:
        logging.info(f"Lendo cabeçalho da planilha: {caminho_planilha}")
        # Otimização: ler apenas o cabeçalho primeiro
        df_header = pd.read_excel(caminho_planilha, nrows=0)
        df_cols = df_header.columns.tolist()

        mapa_colunas = {}
        for chave, aliases in colunas_cfg.items():
            coluna_detectada = detectar_coluna(df_cols, aliases)
            if coluna_detectada:
                mapa_colunas[chave] = coluna_detectada
                logging.info(f"Coluna '{chave}' mapeada para '{coluna_detectada}'")
            else:
                logging.warning(f"Nenhuma coluna encontrada para '{chave}'")

        colunas_necessarias = [col for col in mapa_colunas.values() if col is not None]
        if not colunas_necessarias:
            logging.error("Nenhuma coluna foi mapeada. Verifique os aliases no config.json.")
            return None

        logging.info("Lendo dados das colunas mapeadas...")
        # Otimização: ler apenas as colunas necessárias
        df = pd.read_excel(caminho_planilha, usecols=colunas_necessarias)

        # Renomear colunas para o padrão definido no config.json
        mapa_rename = {v: k for k, v in mapa_colunas.items()}
        df.rename(columns=mapa_rename, inplace=True)

        # Remover colunas que não foram mapeadas
        colunas_a_manter = list(mapa_rename.values())
        df = df[colunas_a_manter]

        logging.info(f"Leitura e processamento da planilha concluídos. {len(df)} linhas lidas.")
        return df.to_dict('records')

    except FileNotFoundError:
        logging.error(f"Arquivo da planilha não encontrado em: {caminho_planilha}")
        return None
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado: {e}")
        return None

if __name__ == '__main__':
    # Passo 1: Processar os dados da planilha
    dados_processados = processar_planilha("config.json")

    # Passo 2: Se os dados foram processados, iniciar a automação da interface
    if dados_processados:
        logging.info("Dados processados com sucesso. Iniciando automação do preenchimento...")
        preencher_formulario(dados_processados) # <-- 2. CHAMADA PARA A AUTOMAÇÃO
    else:
        logging.error("A automação não será iniciada devido a erros no processamento dos dados.")
