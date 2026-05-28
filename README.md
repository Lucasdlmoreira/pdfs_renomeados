# Renomeador de PDFs - Inframerica

Sistema web desenvolvido em Python para automatizar a renomeação de arquivos PDF escaneados utilizando OCR.

O sistema identifica automaticamente números presentes no cabeçalho dos documentos e gera um arquivo `.zip` com os PDFs organizados e renomeados.

---

# Funcionalidades

- Upload múltiplo de PDFs
- Leitura automática de documentos escaneados
- OCR utilizando EasyOCR
- Identificação automática de números com Regex
- Renomeação automática dos arquivos
- Separação de arquivos com falha para revisão manual
- Geração de arquivo `.zip` para download
- Interface web simples e intuitiva

---

# Tecnologias Utilizadas

## Linguagem
- Python

## Framework Web
- Streamlit

## Bibliotecas
- PyMuPDF (`fitz`)
- EasyOCR
- NumPy
- Regex (`re`)
- zipfile
- io

---

# Como Funciona

O sistema executa o seguinte fluxo:

1. Usuário envia os arquivos PDF
2. O sistema abre o PDF
3. A primeira página é processada
4. O cabeçalho do documento é recortado
5. O OCR realiza a leitura do texto
6. Uma expressão regular identifica o número do documento
7. O PDF é renomeado automaticamente
8. O sistema gera um arquivo `.zip` com:
   - PDFs renomeados corretamente
   - PDFs para revisão manual

---

# Executando o Projeto

```bash
streamlit run app.py
```

Após iniciar, o sistema abrirá automaticamente no navegador.
