import os
import re
import PyPDF2

# Caminho para a pasta do OneDrive no seu computador
onedrive_folder_path = r'C:\Users\Alexandre\OneDrive\pdfs'


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

# Abrir o arquivo txt onde as linhas serão escritas
with open(r'C:\Users\Alexandre\OneDrive\pdfspdf_invoice.txt', 'w') as txt_file:
    # Iterar sobre todas as pastas e subpastas na pasta do OneDrive
    for root, dirs, files in os.walk(onedrive_folder_path):
        for filename in files:
            # Verificar se o arquivo é um PDF
            if filename.endswith('.pdf'):
                # Caminho completo para o arquivo
                file_path = os.path.join(root, filename)

                # Abrir o arquivo PDF
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)

                    # Extrair o texto do PDF
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text()

                    # Procurar as informações no texto
                    try:
                        account_number = re.search(r'Account Number: (\d+)', text).group(1)
                        invoice_date = re.search(r'Invoice Date: (\d{2}/\d{2}/\d{4})', text).group(1)
                        invoice_number = re.search(r'Invoice Number: (INV\d+)', text).group(1)
                        due_date = re.search(r'Due Date: (\d{2}/\d{2}/\d{4})', text).group(1)
                    except AttributeError:
                        # Se não encontrou uma das informações, imprimir o nome do arquivo e continuar para o próximo arquivo
                        print(f"Could not find all necessary information in file {filename}")
                        continue

                    # Substituir "LD Usage" por "LD_Usage"
                    text = text.replace('LD Usage', 'LD_Usage')
                    text = text.replace('One Time', 'One_Time')
                    text = text.replace('from\nBrazil', 'from_Brazil')
                    text = text.replace('from Brazil,\n', 'from Brazil,_')
                    text = text.replace('(prorated refund -\n#', '_')
                    text = text.replace(')', ') ')
                    text = text.replace('023.', '023 ')
                    text = text.replace('dated ', 'dated_')
                    text = text.replace('dated_6/30/2023', 'dated_6/30/2023 ')
                    # Replace "Case 0" with "Case_0"
                    text = text.replace(". The 15% withholding tax", "._The_15%_withholding_tax")
                    text = text.replace("Brazil - payment", "Brazil_-_payment")
                    # Antes de extrair o texto
                    text = re.sub('SaaS', 'SaaS ', text)

                    # Verificar se "Surcharge&Fee*" está no PDF
                    surcharge_and_fee = "Surcharge&Fee*" in text

                    # Se "Surcharge&Fee*" não estiver presente no PDF, pular para o próximo arquivo
                    if not surcharge_and_fee:
                        continue

                    # Dividir o texto em linhas
                    lines = text.splitlines()
                    # Para cada linha, verificar se começa com uma data
                    for line in lines:
                        if re.match(r'^\d{2}/\d{2}/\d{4}', line):
                            if "One_Time" in line:
                                match = re.match(r'(\d{2}/\d{2}/\d{4})', line)
                                if match:
                                    date = match.group()
                                    line = f'{date}|{date} {line[len(date)+1:]}'
                            elif not any(category in line for category in ["LD_Usage", "Recurring", "SaaS", "Prorated", "One_Time"]):
                                match = re.search(r'(\d{2}/\d{2}/\d{4})\-(\d{2}/\d{2}/\d{4})', line)
                                if match:
                                    line = line[:match.end()] + ' Credts ' + line[match.end():]

                            line += f' {invoice_number} {invoice_date} {due_date} {account_number}\n'
                            
                            if "Credts" in line:
                                line = line.replace("-", "|", 1)
                                line = line.replace(" ", "|", 1)
                                line = line.replace(" ", "|", 1)
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")#até começar o total
                                line = replace_last(line, " ", "|")#total 
                                line = replace_last(line, " ", "|")#tax
                                line = replace_last(line, " ", "|")#Surcharge
                                line = replace_last(line, " ", "||")#sub
                                line = replace_last(line, " ", "|")
                            else:
                                line = line.replace("-", "|", 1)
                                line = line.replace(" ", "|", 1)
                                line = line.replace(" ", "|", 1)
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                line = replace_last(line, " ", "|")
                                
                            txt_file.write(line)


print('PDFs processados e linhas salvas no arquivo txt!')



import pandas as pd
import pyodbc 

# Conexão com o SQL Server
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=server;'
                      'DATABASE=tabela_nome ;'
                      'UID=login;'
                      'PWD=senha')
cursor = conn.cursor()
# Leitura da segunda planilha do arquivo Excel
df = pd.read_excel(r'C:\Users\Alexandre\OneDrive\pdfs'pdf_final_agosto.xlsx', sheet_name='Planilha2', engine='openpyxl')
# Substituir '-' por 0 na coluna 'Qty'
df['Qty'] = df['Qty'].replace('-', 0)
# Dicionário com os novos tipos de dados
novos_tipos = {
    'Begin of Period': 'datetime64[ns]',
    'End of Period': 'datetime64[ns]',
    'Charge Type': 'object',
    'Description': 'object',
    'Qty': 'int64',
    'Unit0Price': 'float64',
    'SubTotal': 'float64',
    'Surcharge&Fee': 'float64',
    'Tax': 'float64',
    'Total': 'float64',
    'Invoice Number': 'object',
    'Invoice Date': 'datetime64[ns]',
    'Due Date': 'datetime64[ns]',
    'Account Number': 'int64'  # Se você quiser manter essa coluna como objeto
}
# Aplicar os novos tipos de dados ao DataFrame
df = df.astype(novos_tipos)
# Inserção dos dados na tabela do SQL Server
for index, row in df.iterrows():
    cursor.execute("""
    INSERT INTO fato.invoice (BeginOfPeriod, EndOfPeriod, ChargeType, Description, Qty, Unit0Price, SubTotal, SurchargeAndFee, Tax, Total, InvoiceNumber, InvoiceDate, DueDate, AccountNumber)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, 
    row['Begin of Period'], 
    row['End of Period'], 
    row['Charge Type'], 
    row['Description'], 
    row['Qty'], 
    row['Unit0Price'], 
    row['SubTotal'], 
    row['Surcharge&Fee'], 
    row['Tax'], 
    row['Total'], 
    row['Invoice Number'], 
    row['Invoice Date'], 
    row['Due Date'], 
    row['Account Number'])
conn.commit()
