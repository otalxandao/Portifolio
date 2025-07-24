# 📁 Portfólio – Automação de Processos com Python

Este repositório reúne dois projetos independentes que demonstram a aplicação de Python para **automatização de processos com dados não estruturados** e **integração de plataformas via API**.

---

## 📄 Projeto 1: Leitor de PDF para Banco de Dados

### 🧠 Objetivo
Extrair dados de arquivos PDF de forma automatizada e organizá-los em um banco de dados relacional.

### 🔧 Funcionalidades
- Leitura de PDFs estruturados e semi-estruturados
- Extração de tabelas e campos específicos
- Conversão para DataFrame e persistência no banco
- Tratamento de valores nulos, strings e formatações

### 🚀 Tecnologias
- `PyPDF2` / `pdfplumber`
- `pandas`
- `SQLAlchemy` 

### 📁 Arquivo principal:
- `pdf_to_excel.py` 

---

## 🔗 Projeto 2: Integração com API Pipefy

### 🧠 Objetivo
Automatizar operações no Pipefy via API, como criação de cards, leitura de fases e movimentações.

### 🔧 Funcionalidades
- Autenticação com API Key
- Leitura de dados de cards
- Criação e atualização de registros
- Organização em rotinas para reuso

### 🚀 Tecnologias
- `requests`
- Manipulação de JSON
- Autenticação HTTP Bearer

### 📁 Arquivo principal:
- `api_pipefy`

---

## 🚀 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/otalxandao/Portifolio.git
```