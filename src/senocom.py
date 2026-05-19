import os
import re
import pdfplumber
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter

# =========================================================
# CONFIGURAÇÕES
# =========================================================

DOCUMENT_TYPES = {
    "Comprovante de Transferência": { "id": 1,
        "anchor": "Comprovante de Transferência",
        "date": ["data da transferencia:"],
        "name": ["nome do recebedor:"],
        "value": ["valor:"],
    },
    "Comprovante de pagamento de boleto": { "id": 2,
        "anchor": "Comprovante de pagamento de boleto",
        "date": ["data de pagamento:"],
        "name": ["razao social:"],
        "value": ["(=) valor do pagamento (r$):"],
    },
    "Comprovante de Transferência CC": { "id": 3,
        "anchor": "conta corrente para conta corrente", # Comprovante de Transferência de conta corrente para conta corrente
        "date": ["transferencia efetuada em"],
        "name": ["nome:"],
        "value": ["valor:"],
    },
    "Comprovante TED": { "id": 4,
        "anchor": "TED solicitada em", # Comprovante de pagamento TED C - outra titularidade
        "date": ["ted solicitada em"],
        "name": ["nome do favorecido:"],
        "value": ["valor da ted:"],
    },
    "Comprovante concessionárias": { "id": 5,
        "anchor": "Comprovante de Pagamento de concessionárias",
        "date": ["operacao efetuada em"],
        "name": ["informacoes fornecidas pelo"],
        "value": ["valor do documento:"],
    },
    "Comprovante DARF": { "id": 6,
        "anchor": "Comprovante de pagamento - DARF",
        "date": ["data do pagamento:"],
        "name": ["agente arrecadador:"],
        "value": ["valor total:"],
    },
    "Comprovante QR Code": { "id": 7,
        "anchor": "Comprovante de pagamento QR Code",
        "date": ["pagamento efetuado em"],
        "name": ["nome do recebedor:"],
        "value": ["valor da transacao:"],
    },
    "Comprovante código de barras": { "id": 8,
        "anchor": "Comprovante de Pagamento com código de barras",
        "date": ["operacao efetuada em"],
        "name": ["informacoes fornecidas pelo"],
        "value": ["valor do documento:"],
    },
    "TED entre bancos": { "id": 9,
        "anchor": "COMPROVANTE DE TRANSFERÊNCIA ENTRE BANCOS", # COMPROVANTE DE TRANSFERÊNCIA ENTRE BANCOS - TED
        "date": ["data da transferencia"],
        "name": ["nome do titular"],
        "value": ["valor da transferencia"],
    },
    "PIX": { "id": 10,
        "anchor": "COMPROVANTE DE PAGAMENTO PIX",
        "date": ["data do pagamento"],
        "name": ["nome do titular"],
        "value": ["valor"],
    },
    "Títulos outros bancos": { "id": 11,
        "anchor": "COMPROVANTE PAGAMENTO TÍTULOS OUTROS BANCOS",
        "date": ["data do pagamento"],
        "name": ["nome do beneficiario"],
        "value": ["valor do pagamento"],
    },
}

INVALID_NAME_TERMS = [
    'cpf',
    'cnpj',
    'conta',
    'valor',
    'r$',
    'pagador'
]

# =========================================================
# UTILITÁRIOS
# =========================================================

def is_valid_name(text):

    text_lower = text.lower()

    if len(text.strip()) < 3:
        return False

    for term in INVALID_NAME_TERMS:
        if term in text_lower:
            return False

    # evita linhas só numéricas
    if re.fullmatch(r'[\d\s\./,-]+', text):
        return False

    return True

def sanitize_filename(text):
    invalid_chars = r'<>:"/\\|?*'

    for char in invalid_chars:
        text = text.replace(char, '')

    text = re.sub(r'\s+', ' ', text).strip()

    return text

def normalize_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ASCII', 'ignore').decode('ASCII')
    text = text.replace('\t', ' ')
    text = re.sub(r' +', ' ', text)
    return text

def extract_value(text):
    match = re.search(r'\d{1,3}(?:\.\d{3})*,\d{2}', text)

    if match:
        return f'R$ {match.group(0)}'

    return 'R$ 0,00'

def extract_date(text):
    match = re.search(r'\d{2}/\d{2}/\d{4}', text)

    if match:
        date = match.group(0)
        parts = date.split('/')
        return f'{parts[0]}-{parts[1]}'

    return 'SEM-DATA'

def find_value_after_keyword(lines, keywords):
    for i, line in enumerate(lines):

        line_lower = line.lower()

        for keyword in keywords:

            if keyword.lower() in line_lower:

                # tenta mesma linha
                value = extract_value(line)

                if value != 'R$ 0,00':
                    return value

                # tenta próximas linhas
                for j in range(1, 4):

                    if i + j < len(lines):

                        next_line = lines[i + j]
                        value = extract_value(next_line)

                        if value != 'R$ 0,00':
                            return value

    return 'R$ 0,00'

def find_date_after_keyword(lines, keywords):
    for i, line in enumerate(lines):

        line_lower = line.lower()

        for keyword in keywords:

            if keyword.lower() in line_lower:

                date = extract_date(line)

                if date != 'SEM-DATA':
                    return date

                for j in range(1, 4):

                    if i + j < len(lines):

                        next_line = lines[i + j]
                        date = extract_date(next_line)

                        if date != 'SEM-DATA':
                            return date

    return 'SEM-DATA'

def find_name_after_keyword(lines, keywords, context=None):

    start_index = 0

    # =====================================================
    # CONTEXTO ESPECIAL PIX BRB
    # =====================================================

    if context:

        for i, line in enumerate(lines):

            if context.lower() in line.lower():
                start_index = i
                break

    # =====================================================
    # PROCURA KEYWORDS
    # =====================================================

    for i in range(start_index, len(lines)):

        line = lines[i]
        line_lower = line.lower()

        for keyword in keywords:

            keyword_lower = keyword.lower()

            if keyword_lower in line_lower:

                # =========================================
                # CASO 1 -> INLINE SEM :
                # Ex:
                # Nome do Titular FULANO
                # =========================================

                candidate = re.sub(
                    re.escape(keyword),
                    '',
                    line,
                    flags=re.IGNORECASE
                ).strip()

                candidate = candidate.replace(':', '').strip()

                if (
                    candidate
                    and len(candidate) > 3
                    and is_valid_name(candidate)
                ):
                    return sanitize_filename(candidate)

                # =========================================
                # CASO 2 -> próximas linhas
                # =========================================

                for j in range(1, 4):

                    if i + j < len(lines):

                        next_line = lines[i + j].strip()

                        if (
                            len(next_line) > 2
                            and is_valid_name(next_line)
                        ):
                            return sanitize_filename(next_line)

    return 'SEM-NOME'

def find_line_after_anchor(lines, anchor):
    for i, line in enumerate(lines):

        if anchor.lower() in line.lower():

            if i + 1 < len(lines):

                return sanitize_filename(lines[i + 1].strip())

    return 'SEM-NOME'

def detect_document_type(text):

    text_lower = text.lower()

    matches = []

    for doc_name, config in DOCUMENT_TYPES.items():

        anchor = config['anchor'].lower()

        if anchor in text_lower:
            matches.append((len(anchor), doc_name))
    
    if not matches:
        return None
    
    matches.sort(reverse=True)

    return matches[0][1]

# =========================================================
# EXTRAÇÃO PRINCIPAL
# =========================================================

def extract_metadata(text):

    lines = [normalize_text(line.strip()) for line in text.split('\n') if line.strip()]

    doc_type = detect_document_type(text)

    if not doc_type:
        return {
            'id': 0,
            'type': 'DESCONHECIDO',
            'date': 'SEM-DATA',
            'name': 'SEM-NOME',
            'value': 'R$ 0,00'
        }

    config = DOCUMENT_TYPES[doc_type]
    context = None

    if doc_type == 'PIX':
        context = 'Dados de Destino do Pix'
    if doc_type == 'TED entre bancos':
        context = 'Dados de destino'
    if doc_type == 'Comprovante de Transferência CC':
        context = 'Dados da conta creditada'
    if doc_type == 'Comprovante concessionárias':
        name = find_line_after_anchor(lines, normalize_text(config['anchor']))
    else:
        name = find_name_after_keyword(lines, config['name'], context=context)

    doc_id = config['id']
    date = find_date_after_keyword(lines, config['date'])
    value = find_value_after_keyword(lines, config['value'])

    return {
        'id': doc_id,
        'type': doc_type,
        'date': date,
        'name': name,
        'value': value,
    }

# =========================================================
# PDF
# =========================================================

def split_pdf(input_pdf, output_folder):

    print(f'Processando: {input_pdf}')

    reader = PdfReader(input_pdf)

    with pdfplumber.open(input_pdf) as pdf:

        page_buffer = []

        for page_number, page in enumerate(pdf.pages):

            try:

                text = page.extract_text()

                if not text:
                    continue

                # guarda página atual no buffer
                page_buffer.append(page_number)

                metadata = extract_metadata(text)

                # ainda não chegou no final do comprovante
                if metadata['type'] == 'DESCONHECIDO':
                    continue

                # =====================================================
                # FINAL DO COMPROVANTE ENCONTRADO
                # =====================================================

                filename = (
                    f"[{metadata['id']:02d}] " # RETIRAR DEPOIS - PARA VERSÃO FINAL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    f"{metadata['date']} "
                    f"{metadata['name']} "
                    f"{metadata['value']}.pdf"
                )

                filename = sanitize_filename(filename)

                output_path = os.path.join(output_folder, filename)

                # evita sobrescrever
                counter = 1
                original_output_path = output_path

                while os.path.exists(output_path):

                    base, ext = os.path.splitext(original_output_path)

                    output_path = f'{base}_{counter}{ext}'

                    counter += 1

                writer = PdfWriter()

                # salva todas páginas do buffer
                for p in page_buffer:
                    writer.add_page(reader.pages[p])

                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)

                print(f'OK -> {filename}')

                # limpa buffer para próximo comprovante
                page_buffer = []

            except Exception as e:
                print(f'Erro na página {page_number + 1}: {e}')

            # ==============================
            # DEBUGGING
            # ==============================

            # print('\n')
            # print('=' * 80)
            # print(f'PÁGINA {page_number + 1}')
            # print('=' * 80)
            # print(text)
            # print('=' * 80)

# =========================================================
# PROCESSAMENTO EM LOTE
# =========================================================

def process_folder(input_folder, output_folder):

    pdf_files = []

    for root, dirs, files in os.walk(input_folder):

        for file in files:

            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))

    if not pdf_files:
        messagebox.showwarning('Aviso', 'Nenhum PDF encontrado.')
        return

    for pdf_file in pdf_files:
        split_pdf(pdf_file, output_folder)

# =========================================================
# INTERFACE
# =========================================================

input_folder = ''
output_folder = ''

def select_input_folder():
    global input_folder

    folder = filedialog.askdirectory(title='Selecione a pasta de entrada')

    if folder:
        input_folder = folder
        input_label.config(text=folder)

def start_process():

    if not input_folder:
        messagebox.showerror('Erro', 'Selecione a pasta de entrada.')
        return

    output_folder = filedialog.askdirectory(
        title='Selecione a pasta de destino final'
    )

    if not output_folder:
        messagebox.showwarning(
            'Aviso',
            'Nenhuma pasta de saída selecionada.'
        )
        return

    try:
        process_folder(input_folder, output_folder)
    except Exception as e:
        messagebox.showerror('Erro', f'{e}')
        return
    
    messagebox.showinfo(
        'Concluído',
        'Arquivos processados com sucesso.'
    )

# =========================================================
# GUI
# =========================================================

root = tk.Tk()
root.title('Separador de Comprovantes PDF')
root.geometry('400x240')

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill='both', expand=True)

btn_input = tk.Button(
    frame,
    text='Selecionar Pasta de Entrada',
    command=select_input_folder,
    width=30,
    height=2
)
btn_input.pack(pady=10)

input_label = tk.Label(frame, text='Nenhuma pasta selecionada', wraplength=650)
input_label.pack()

btn_start = tk.Button(
    frame,
    text='Executar Processamento',
    command=start_process,
    width=30,
    height=2,
    bg='green',
    fg='white'
)
btn_start.pack(pady=30)

root.mainloop()
