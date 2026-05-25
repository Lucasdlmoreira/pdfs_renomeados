import streamlit as st
import fitz  # PyMuPDF
import easyocr
import re
import numpy as np
import io
import zipfile

# Configuração visual da página web
st.set_page_config(page_title="Renomeador Inframerica", page_icon="📄", layout="centered")

st.title("Renomear PDFs")
st.markdown("Arraste seus PDFs escaneados.")

# Carrega o leitor do EasyOCR apenas uma vez e guarda na memória (Cache)
@st.cache_resource
def load_reader():
    # gpu=False para notebooks comuns sem placa de vídeo dedicada
    return easyocr.Reader(['pt'], gpu=False)

reader = load_reader()

# Campo de Upload na tela
arquivos_pdf = st.file_uploader("Selecione os arquivos PDF", type="pdf", accept_multiple_files=True)

if arquivos_pdf:
    if st.button("Iniciar Renomeação"):
        progresso = st.progress(0)
        status_text = st.empty()
        
        # Buffer para criar o arquivo ZIP diretamente na memória RAM
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            sucessos = 0
            falhas = 0
            
            for i, file_input in enumerate(arquivos_pdf):
                try:
                    # Ler o PDF enviado pelo navegador
                    pdf_bytes = file_input.read()
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    pagina = doc.load_page(0)
                    
                    # --- CORTE DA PÁGINA (Pega apenas o topo) ---
                    rect = pagina.rect 
                    # Limitamos em 25% da altura (0.25) para focar só na Ordem e ignorar o resto da folha A4
                    area_cabecalho = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 * 0.25)
                    
                    # --- RENDERIZAÇÃO LEVE ---
                    # Matrix(1.0, 1.0) gera uma imagem leve e o 'clip' garante que só o topo vire imagem
                    pix = pagina.get_pixmap(matrix=fitz.Matrix(1.0, 1.0), clip=area_cabecalho)
                    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
                    
                    # O OCR roda instantaneamente porque a imagem é bem pequena
                    resultado = reader.readtext(img_data, detail=0)
                    texto_todo = " ".join(resultado)
                    
                    # Busca pelo número de 7 ou 8 dígitos da Ordem
                    busca = re.search(r'\b(\d{7,8})\b', texto_todo)
                    
                    if busca:
                        novo_nome = f"{busca.group(1)}.pdf"
                        zf.writestr(f"Finalizados/{novo_nome}", pdf_bytes)
                        sucessos += 1
                    else:
                        zf.writestr(f"Revisar_Manualmente/{file_input.name}", pdf_bytes)
                        falhas += 1
                    
                    doc.close()
                except Exception as e:
                    st.error(f"Erro no arquivo {file_input.name}: {e}")
                
                # Atualiza a barra de progresso na tela do navegador
                percentual = (i + 1) / len(arquivos_pdf)
                progresso.progress(percentual)
                status_text.text(f"Processando: {i+1} de {len(arquivos_pdf)}")

        st.success(f"Pronto! {sucessos} renomeados com sucesso | {falhas} enviados para revisão.")
        
        # Disponibiliza o botão de baixar o arquivo .ZIP gerado
        st.download_button(
            label="Baixar Arquivos Renomeados (.zip)",
            data=zip_buffer.getvalue(),
            file_name="pdfs_inframerica_renomeados.zip",
            mime="application/zip"
        )