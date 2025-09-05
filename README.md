# Relatório de Risco/Performance para Fundos de Investimentos (UFFinance)



#
## Descrição

Este projeto foi desenvolvido para automatizar a geração de relatórios de risco para o fundo de investimento da UFFinance - Liga de Mercado Financeiro da UFF.

Permite aos analistas avaliarem métricas de risco importantes historicamente: volatilidade, *drawdown*, VaR (Value at Risk) e liquidez do fundo.



O sistema é modular, facilitando a adição de novas funcionalidades. Ele processa dados da carteira fornecida em arquivo Excel, realiza cálculos de risco e exporta os resultados em formato CSV.



#
## Exemplo de relatório

Basta inserir o seu portfólio em `input` e rodar o código em `main.py`. Arquivos CSV serão criados na pasta `outputs` que alimentarão o relatório excel via Power Query.


![Relatório em excel que trás a performance do fundo contra benchmark, além das métricas de risco.](dashboard_example.png)
A T E N Ç Ã O 

Para uma leitura correta dos dados é necessário que `dashboard` tenha o mesmo prefixo que o escolido em `main.py`. Assim se `prefix=week1`, renomeie o dashboard para `week1_dashboard.xlsx`. Esta estrutura permite gerenciar diversos relatórios diferentes com bases de dados diferentes. As bases de dados, em CSV, serão geradas automaticamente com o préfixo.

É necessário que os arquivos CSV estejam a uma pasta, `em outputs`, de distância de `{prefix}_dashboard.xlsx`, como na estrutura a baixo.



#
## 📁Estrutura do Projeto

Visão geral dos principais diretórios e arquivos:

```
.
├── main.py
│
├── inputs/
│   └── portfolio1.xlsx
│
├── dashboards/
│   └── {prefix}_dashboard.xlsx
│
├── outputs/
│   ├── {prefix}_liquidity_matrix.csv
│   └── {prefix}_series.csv
│
└── src/
    ├── assistants/
    │   ├── bcb_api.py
    │   └── read_portfolio.py
    ├── complete_report.py
    └── functions.py
```

*   `main.py`: O script principal que orquestra a leitura dos dados da carteira, a geração dos relatórios de risco e a exportação dos resultados.


* `complete_report.py`: Contém a lógica para calcular as diversas métricas de risco (volatilidade, drawdown, VaR, matriz de liquidez) e exportar os resultados para arquivos CSV.
 

* `functions.py`: Contém a classe `Portfolio` utilizada para simular uma carteira ao longo do tempo.


* `read_portfolio.py`: Ler os dados da carteira a partir de arquivos Excel.


*   `dashboard.xlsx`: Dashboard em Excel utilizado para visualizar os resultados gerados.






## ▶️ Configuração do Ambiente

Antes de executar, crie um ambiente virtual (venv). Certifique-se de ter o (Python >= 3.12) instalado.
1.  **Crie um ambiente virtual, digite no terminal:**
    ```bash
    python -m venv venv
    ```

2.  **Ative o ambiente virtual:**
    *   No Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   No macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Instale as dependências necessárias:**
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Como Executar

Com o ambiente configurado e as dependências instaladas. Para gerar o relatório de risco:


#
1.  **Prepare os arquivos de entrada**: Coloque seus arquivos de carteira de investimento (no formato `.xlsx`) no diretório `inputs/`. Certifique-se de que a primeira coluna sejam os `tickers` e a segunda os pesos `weights`.


#
2.  **Configure o `main.py`**: Abra o arquivo `main.py` e ajuste as variáveis `start`, `portfolio` e `prefix`.

*    `start`: Define a data de início do portfolio

*    `portfolio`: Deve corresponder ao nome do arquivo da sua carteira (sem a extensão `.xlsx`).

*    `prefix`: Deve condizer com o prefixo posto no seu dashboard.

#
Exemplo de configuração em `main.py`:


    ```python
    start = '2025-04-01'
    portfolio = 'portfolio2'
    # ...
    p1_report = general_report(p1_t, p1_w, start, name="semana1", portfolio_inicial_value=100000000)
    ```

#
3.  **Execute o script principal**:
    ```bash
    python main.py
    ```

#
4.  **Resultado**: Os dados gerados serão salvos, em CSV, no diretório `outputs/`. Você encontrará arquivos como:
    `{prefix}_liquidity_matrix.csv`
    
    `{prefix}_series.csv`




#
## 👨‍💻 Autor
* João Fernando
* LinkedIn: https://www.linkedin.com/in/joaoffialho/
