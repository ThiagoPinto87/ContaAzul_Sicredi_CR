# CRCASI
## O que é?
Trata-se de uma automação que faz a importação de Contas a Receber ao sistema Conta Azul utilizando como Base os arquivos do Sicredi.

### Versão 1.02


### Como ele funciona?
- Ele pega o arquivo de emissão de boletos e o arquivo de cadastro de pagadores e transforma em um único arquivo de importação para facilitar o trabalho do dia-a-dia das equipes de contas a receber.
- Ele utiliza como princípio o arquivo de cadastro de pagadores para fazer o cadastro do cliente;
- Do arquivo de boletos, utiliza o nome e une com o cadastro de pagadores para formar cada parcela (atenção com homônimos, pois eles tendem a ter parcelas duplicadas).
- ATENÇÃO: Esta automação não exime a responsabilidade do usuário verificar se todas as parcelas estão lançadas corretamente como: Nome/Razão Social, CPF/CNPJ, descrição, competencia, vencimento, emissão, descrição, observações, entre outros. Esta aplicação serve como um facilitador do processo de inserção de clientes no sistema.



### Como compilar o executável.
- É recomendável utilizar a biblioteca `pyintaller` utilizando o seguinte comando no seu terminal:
 
```sh
pyinstaller --name="Vidotti_Ferreira_CR_CA_Importacao" --onefile --icon="ÍconeCaliber.ico" --hidden-import=pandas --hidden-import=openpyxl --hidden-import=numpy main.py
```

## Melhorias
- Combater homonimos (Neste caso, sugiro perguntar ao usuário validar o CPF antes de criar o arquivo de importação, caso não seja o CPF do cliente, solicitar a ele que digite o CPF correto do cliente.);

## Relatório de fixação de bug's e aprimoramento:
### 04/11/25
- Corrigido os erros de datas de vencimento, emissão e competencia que estavam puxando a data no formato americano, para isso, usei o `dayfirst=True`;
- Corrigido a contagem de parcelas em ordem crescente usando como base o CPF;