import difflib

def detectar_coluna(df_cols, aliases):
    """
    Detecta a coluna correspondente a uma lista de aliases.

    Args:
        df_cols (list): Lista de colunas do DataFrame.
        aliases (list): Lista de aliases para a coluna desejada.

    Returns:
        str: O nome da coluna correspondente, ou None se não for encontrada.
    """
    df_cols_lower = [str(c).lower().strip() for c in df_cols]
    for alias in aliases:
        match = difflib.get_close_matches(alias.lower(), df_cols_lower, n=1, cutoff=0.6)
        if match:
            # Encontra a coluna original com base no match em minúsculas
            for original_col in df_cols:
                if str(original_col).lower().strip() == match[0]:
                    return original_col
    return None
