# RPA Assistente para Lançamentos no Sistema Domínio

Bem-vindo ao RPA Assistente! Esta ferramenta foi criada para tornar seus lançamentos contábeis no sistema **Domínio** mais rápidos e fáceis.

Em vez de um programa que você roda toda vez, este é um **assistente que fica rodando em segundo plano**. Depois de iniciado, basta usar um atalho de teclado para que ele leia a sua planilha do Excel aberta e lance os dados no sistema.

## Como Funciona?

1.  **Você executa o assistente uma vez.** Ele fica esperando, sem atrapalhar.
2.  **Você abre sua planilha no Excel** com os dados de lançamento.
3.  **Você abre o sistema Domínio** na tela de "Consulta e Lançamentos".
4.  **Você pressiona `Ctrl+Alt+A`**. A mágica acontece: o assistente lê os dados e preenche tudo para você.

## Guia Rápido: 4 Passos para Começar

Siga estes passos na ordem. Em poucos minutos, você estará pronto para automatizar.

### Passo 1: Instalação

Primeiro, precisamos instalar as "peças" que o robô precisa para funcionar.

>   **Dê um duplo-clique no arquivo `install.bat`**

Uma tela preta irá aparecer e instalar tudo automaticamente. Espere até o final e pressione qualquer tecla para fechar.

### Passo 2: Configuração (`config.json`)

Este é o passo mais importante. O arquivo `config.json` é o "cérebro" do robô. É aqui que você diz a ele o que procurar. Abra-o com um editor de texto (como o Bloco de Notas).

**1. Mapeamento das Colunas:**
Na seção `"colunas"`, diga ao robô quais nomes suas colunas podem ter. Por exemplo, para a conta de débito, você pode usar "conta a debitar", "debito", etc.

```json
"colunas": {
  "debito": ["conta devedora", "debito", "conta a debitar"],
  "credito": ["conta credora", "credito", "conta a creditar"],
  "valor": ["valor", "total", "valor do lancamento"],
  "historico": ["historico", "descricao", "desc"]
}
```

**2. Configuração da Interface (Avançado):**
A seção `"ui_config"` diz ao robô como encontrar os campos na tela do sistema Domínio. Os valores padrão devem funcionar para a maioria dos casos. Se a automação não conseguir encontrar um campo, você precisará usar uma ferramenta como o **"Inspect.exe"** da Microsoft para encontrar os valores corretos (`title` ou `auto_id`) e ajustá-los aqui.

### Passo 3: Criar o Programa

Agora que tudo está configurado, vamos criar o arquivo `.exe` que você irá usar.

>   **Dê um duplo-clique no arquivo `build.bat`**

Novamente, uma tela preta irá aparecer. Este processo pode demorar alguns minutos. No final, ele criará uma nova pasta chamada `dist`, e dentro dela estará o seu programa: `RPA_Assistente_Dominio.exe`.

### Passo 4: Usar o Assistente!

1.  **Copie o `RPA_Assistente_Dominio.exe`** da pasta `dist` e cole-o na pasta principal (a mesma onde está o `config.json`).
2.  **Dê um duplo-clique no `RPA_Assistente_Dominio.exe` para iniciá-lo.** Nada visível vai acontecer, mas ele já estará rodando em segundo plano.
3.  **Abra sua planilha** no Excel.
4.  **Abra o sistema Domínio** na tela de lançamentos.
5.  **Pressione `Ctrl+Alt+A`**.

A automação começará. Para monitorar o que o robô está fazendo, você pode abrir o arquivo `automacao_background.log`.

Para **encerrar o assistente**, abra o Gerenciador de Tarefas do Windows (`Ctrl+Shift+Esc`) e finalize o processo `RPA_Assistente_Dominio.exe`.
