import os
import io
import requests
import pandas as pd

def download_pdf(url: str, dest_path: str):
    """Baixa o PDF para dest_path (sobrescreve se existir)."""
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    with open(dest_path, "wb") as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)
    return dest_path

def try_tabula_extract(pdf_path: str, pages: str):
    """
    Tenta extrair tabelas com tabula-py.
    pages: string no formato '12-15' ou '12' ou '12,13'
    Retorna um DataFrame (concat de todas as tabelas extraídas)
    """
    try:
        import tabula
        # retorna lista de dfs
        dfs = tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True, lattice=True)
        if not dfs:
            return None
        # concat careful (some tables may be header/footer)
        df = pd.concat(dfs, ignore_index=True)
        return df
    except Exception as e:
        print("tabula failed:", e)
        return None

def pdfplumber_extract(pdf_path: str, pages: list):
    """
    Extrai tabelas usando pdfplumber como fallback.
    pages: lista de 1-based page numbers (ex: [12,13])
    Retorna DataFrame concatenado.
    """
    import pdfplumber
    import pandas as pd
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for p in pages:
            page_index = p - 1
            if page_index < 0 or page_index >= len(pdf.pages):
                continue
            page = pdf.pages[page_index]
            # tenta extrair tabelas detectadas
            page_tables = page.extract_tables()
            for t in page_tables:
                df = pd.DataFrame(t[1:], columns=t[0])
                tables.append(df)
    if not tables:
        return None
    df = pd.concat(tables, ignore_index=True)
    return df

def normalize_table(df: pd.DataFrame, col_uf_candidates=None, col_val_candidates=None):
    """
    Tenta normalizar DataFrame extraído do PDF para duas colunas:
    'UF' e 'value' (valor numérico).
    col_uf_candidates / col_val_candidates: listas de strings com nomes possíveis.
    """
    import re
    df = df.copy()
    # lower columns
    cols = {c: c.strip() for c in df.columns}
    df.rename(columns=cols, inplace=True)
    # heurística: encontrar coluna com sigla UF (2 letras) e coluna com números
    uf_col = None
    val_col = None
    # candidates provided?
    if col_uf_candidates:
        for c in col_uf_candidates:
            if c in df.columns:
                uf_col = c
                break
    if col_val_candidates:
        for c in col_val_candidates:
            if c in df.columns:
                val_col = c
                break

    # fallback heuristics
    if uf_col is None:
        # buscar coluna com valores que parecem siglas (2 letras ou nomes de estados)
        for c in df.columns:
            sample = df[c].astype(str).str.strip().head(10).tolist()
            if all((len(s) <= 3 and s.isalpha()) or (s == '') for s in sample):
                uf_col = c
                break
    if val_col is None:
        # buscar coluna que contenha números (com . e ,)
        for c in df.columns[::-1]:  # preferir colunas à direita (normalmente valores)
            sample = df[c].astype(str)
            if sample.str.contains(r'\d').any():
                val_col = c
                break

    if uf_col is None or val_col is None:
        # última tentativa: pegar primeiras duas colunas
        cols_list = list(df.columns)
        if len(cols_list) >= 2:
            uf_col = uf_col or cols_list[0]
            val_col = val_col or cols_list[1]
        else:
            raise ValueError("Não foi possível localizar colunas UF/valor na tabela.")

    # limpar valores e converter números
    def parse_num(x):
        if x is None:
            return None
        s = str(x).strip()
        # remover asteriscos e notas
        s = re.sub(r'[*†].*', '', s)
        s = s.replace('.', '').replace(',', '.')
        s = re.sub(r'[^\d\.\-]', '', s)
        try:
            if s == '':
                return None
            # inteiro
            if '.' not in s:
                return int(s)
            return float(s)
        except:
            return None

    out = pd.DataFrame()
    out['UF'] = df[uf_col].astype(str).str.strip()
    out['value_raw'] = df[val_col].astype(str).apply(parse_num)
    # drop rows without UF or value
    out = out[~out['UF'].str.strip().isin(['', 'UF', ''])].copy()
    out = out[~out['value_raw'].isnull()].copy()
    out = out.drop_duplicates(subset=['UF'])
    out = out.reset_index(drop=True)
    return out.rename(columns={'value_raw': 'value'})
