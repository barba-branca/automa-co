import difflib
import logging
import json
import pandas as pd
import xlwings as xw

def detectar_coluna(df_cols, aliases):
    """Detecta a coluna correspondente a uma lista de aliases."""
    df_cols_lower = [str(c).lower().strip() for c in df_cols]
    for alias in aliases:
        match = difflib.get_close_matches(alias.lower(), df_cols_lower, n=1, cutoff=0.6)
        if match:
            for original_col in df_cols:
                if str(original_col).lower().strip() == match[0]:
                    return original_col
    return None

def carregar_configuracao(config_path="config.json"):
    """Carrega o arquivo de configuração JSON."""
    try:
        logging.info(f"Carregando arquivo de configuração: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Arquivo de configuração não encontrado em: {config_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Erro ao decodificar o JSON em: {config_path}. Verifique a formatação.")
        return None

def processar_planilha_ativa(config):
    """
    Usa xlwings para se conectar à instância ativa do Excel, ler os dados da planilha
    em foco e processá-los.
    """
    colunas_cfg = config.get("colunas")
    if not colunas_cfg:
        logging.error("Seção 'colunas' não encontrada no config.json.")
        return None

    try:
        logging.info("Tentando se conectar a uma instância ativa do Excel...")
        # Conecta-se à instância do Excel que o usuário está usando
        app = xw.apps.active
        if not app:
            logging.warning("Nenhuma instância do Excel encontrada.")
            return None

        # Pega a planilha (workbook) e a aba (sheet) ativas
        wb = app.books.active
        sheet = wb.sheets.active
        logging.info(f"Conectado com sucesso à planilha '{wb.name}' na aba '{sheet.name}'.")

        # Converte os dados da planilha para um DataFrame do Pandas
        # 'expand' garante que ele pegue toda a tabela de dados adjacentes
        df = sheet.range('A1').expand().options(pd.DataFrame, index=False, header=True).value

        if df.empty:
            logging.warning("A planilha ativa está vazia.")
            return None

        # --- Lógica de mapeamento de colunas (reutilizada) ---
        df_cols = df.columns.tolist()
        mapa_colunas = {}
        for chave, aliases in colunas_cfg.items():
            coluna_detectada = detectar_coluna(df_cols, aliases)
            if coluna_detectada:
                mapa_colunas[chave] = coluna_detectada
                logging.info(f"Coluna '{chave}' mapeada para '{coluna_detectada}'")
            else:
                logging.warning(f"Nenhuma coluna encontrada para '{chave}' na planilha ativa.")

        # Filtra o DataFrame para manter apenas as colunas que foram mapeadas
        colunas_a_manter = [col for col in mapa_colunas.values() if col is not None]
        if not colunas_a_manter:
            logging.error("Nenhuma coluna da planilha correspondeu à configuração. Verifique os nomes das colunas.")
            return None

        df_filtrado = df[colunas_a_manter]

        # Renomeia as colunas para o padrão interno do RPA
        mapa_rename = {v: k for k, v in mapa_colunas.items()}
        df_filtrado.rename(columns=mapa_rename, inplace=True)

        logging.info(f"{len(df_filtrado)} linhas de dados extraídas e processadas da planilha.")
        return df_filtrado.to_dict('records')

    except Exception as e:
        logging.error(f"Ocorreu um erro ao tentar ler a planilha ativa do Excel: {e}")
        return None
