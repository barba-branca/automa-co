# RPA para Lançamentos Contábeis no Sistema Domínio

Este projeto automatiza o processo de lançamento de dados de uma planilha Excel no sistema de contabilidade "Domínio Contabilidade Fiscal". A solução foi desenvolvida em Python e utiliza uma abordagem modular para otimizar a leitura de dados e a automação da interface gráfica (GUI).

## Funcionalidades Principais

- **Leitura Otimizada de Excel**: Lê apenas o cabeçalho e as colunas necessárias da planilha, garantindo alta performance mesmo com arquivos grandes.
- **Mapeamento Dinâmico de Colunas**: Identifica as colunas corretas na planilha com base em uma lista de possíveis nomes (aliases), tornando a automação flexível a diferentes layouts de planilhas.
- **Automação de Interface Robusta**: Utiliza `pywinauto` para interagir com o sistema Domínio, preenchendo os campos de lançamento de forma automática.
- **Logging Detalhado**: Gera logs de todas as etapas do processo, facilitando o monitoramento e a identificação de erros.
- **Configuração Centralizada**: Todas as configurações, como o caminho da planilha e o mapeamento de colunas, são gerenciadas em um único arquivo `config.json`.

## Estrutura do Projeto

```
.
├── automacao_interface.py  # Script responsável pela automação da interface gráfica (pywinauto).
├── config.json             # Arquivo de configuração (caminho da planilha, colunas).
├── rpa.py                  # Orquestrador principal: lê a config, processa os dados e chama a automação.
├── utils.py                # Funções auxiliares (ex: detecção de colunas).
└── requirements.txt        # Lista de dependências Python.
```

## Pré-requisitos

- Python 3.8 ou superior
- Acesso ao sistema "Domínio Contabilidade Fiscal" em uma máquina Windows.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-seu-repositorio>
    cd <nome-do-repositorio>
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    O projeto precisa das bibliotecas listadas no `requirements.txt`. Crie este arquivo com o seguinte conteúdo e depois execute o comando `pip install`.

    **`requirements.txt`:**
    ```
    pandas
    openpyxl
    pywinauto
    ```

    **Comando para instalar:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuração (`config.json`)

Antes de executar, ajuste o `config.json` com suas informações:

```json
{
  "caminho_planilha": "C:\\caminho\\para\\sua\\planilha.xlsx",
  "colunas": {
    "debito": ["conta devedora", "debito", "conta a debitar"],
    "credito": ["conta credora", "credito", "conta a creditar"],
    "valor": ["valor", "total", "valor do lancamento"],
    "historico": ["historico", "descricao", "desc"]
  }
}
```

- `caminho_planilha`: **(Obrigatório)** O caminho completo para o arquivo Excel. Use barras duplas `\\` no Windows.
- `colunas`: **(Obrigatório)** Um dicionário onde:
    - A **chave** (`"debito"`, `"credito"`, etc.) é o nome padrão que o script usará.
    - O **valor** é uma lista de possíveis nomes que a coluna pode ter na sua planilha (aliases).

## Como Executar

1.  Abra o sistema **Domínio Contabilidade Fiscal** e navegue até a tela **"Consulta e Lançamentos"**.
2.  Abra um terminal (como o PowerShell ou CMD) no diretório do projeto.
3.  Ative o ambiente virtual (se estiver usando um).
4.  Execute o orquestrador principal:
    ```bash
    python rpa.py
    ```

O script irá processar a planilha e começar a preencher os dados na janela do sistema. Acompanhe os logs no terminal.

## **IMPORTANTE: Ajuste dos Seletores da Interface**

A automação da interface depende de "seletores" (como `title` e `auto_id`) para encontrar os campos e botões. **É muito provável que você precise ajustar esses seletores.**

1.  **Baixe a ferramenta `Inspect.exe`**: Ela faz parte do Windows SDK, mas pode ser encontrada separadamente. É a melhor forma de inspecionar os elementos da interface.
2.  **Execute `Inspect.exe`** e passe o mouse sobre os campos (Debitar, Creditar, Valor, etc.) e botões (Incluir) na janela do Domínio.
3.  Anote as propriedades `Name` e `AutomationId` de cada elemento.
4.  Abra o arquivo `automacao_interface.py` e atualize os valores nos comandos `main_dlg.child_window(...)` para que correspondam ao que você encontrou.
