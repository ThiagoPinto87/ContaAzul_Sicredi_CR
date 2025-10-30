# CRCASI
## O que é?
Trata-se de uma automação que faz a importação de Contas a Receber ao sistema Conta Azul utilizando como Base os arquivos do Sicredi.

### Versão 1.01


### Como ele funciona?
- Ele pega o arquivo de emissão de boletos e o arquivo de cadastro de pagadores e transforma em um único arquivo de importação para facilitar o trabalho do dia-a-dia das equipes de contas a receber.

### Como compilar o executável.
- É recomendável utilizar a biblioteca `pyintaller` utilizando o seguinte comando no seu terminal:
 
```sh
pyinstaller --name="Vidotti_Ferreira_CR_CA_Importacao" --onefile --icon="ÍconeCaliber.ico" --hidden-import=pandas --hidden-import=openpyxl --hidden-import=numpy main.py
```

## Melhorias

- Melhorar no parcelamento sendo que na parcela atual ele conte individualmente cada nome ou CPF;
- Combater homonimos (Neste caso, sugiro perguntar ao usuário validar o CPF antes de criar o arquivo de importação, caso não seja o CPF do cliente, solicitar a ele que digite o CPF correto do cliente.);