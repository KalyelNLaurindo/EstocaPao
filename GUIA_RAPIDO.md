# 🥖 Guia Rápido — EstocaPão

**Para quem nunca abriu um terminal antes.** Siga os passos em ordem e em 10 minutos o EstocaPão estará rodando no seu computador.

---

## Passo 1 — Instale o Python

O EstocaPão funciona com **Python 3.10 ou mais novo**. Se você já tem, pode pular para o Passo 2.

1. Acesse: **https://www.python.org/downloads/**
2. Clique em **"Download Python 3.x.x"** (o botão amarelo grande)
3. Execute o instalador baixado
4. ⚠️ **IMPORTANTE:** Marque a caixa **"Add Python to PATH"** antes de clicar em *Install Now*

Para confirmar que deu certo, abra o **PowerShell** (Windows) ou **Terminal** (Mac/Linux) e digite:

```
python --version
```

Deve aparecer algo como `Python 3.10.x`. Se aparecer, está pronto.

---

## Passo 2 — Baixe o EstocaPão

Você vai precisar do **Git** instalado, ou pode baixar o projeto como arquivo ZIP direto do GitHub:

### Opção A — Com Git (recomendado)
```
git clone https://github.com/KalyelNLaurindo/estocapao.git
```

### Opção B — Sem Git
1. Acesse **https://github.com/KalyelNLaurindo/estocapao**
2. Clique no botão verde **"Code"**
3. Clique em **"Download ZIP"**
4. Extraia o arquivo ZIP em uma pasta de sua escolha

---

## Passo 3 — Entre na pasta do projeto

No terminal, navegue até onde o EstocaPão foi baixado:

```
cd estocapao
```

> **Dica:** Se não souber navegar pelo terminal, abra a pasta do projeto no Explorador de Arquivos, clique com o botão direito dentro dela e escolha "Abrir no Terminal" (Windows 11) ou "Abrir PowerShell aqui".

---

## Passo 4 — Instale o programa

```
pip install .
```

Aguarde finalizar. Isso instala o comando `estocapao` no seu sistema.

---

## Passo 5 — Configure o arquivo de configuração

Copie o arquivo de exemplo de configuração:

**Windows (PowerShell):**
```
copy config.ini.example config.ini
```

**Mac / Linux:**
```
cp config.ini.example config.ini
```

---

## Passo 6 — Inicialize o sistema (primeira vez)

```
estocapao --init
```

Isso cria o banco de dados local e os arquivos de log. Só precisa fazer isso uma vez.

---

## ✅ Pronto! Agora você pode usar

---

## Como usar no dia a dia

### 📦 Registrar um novo lote de ingrediente

Use `add` para cadastrar um ingrediente que chegou na padaria:

```
estocapao add farinha 25.5 --exp 2026-07-20 --limit 10
```

| Parte do comando | O que significa |
| :--- | :--- |
| `farinha` | Nome do ingrediente |
| `25.5` | Quantidade em kg (ou qualquer unidade que você use) |
| `--exp 2026-07-20` | Data de validade no formato ANO-MÊS-DIA |
| `--limit 10` | Quantidade mínima — abaixo disso, o sistema vai te avisar |

---

### 📊 Ver o estoque atual

```
estocapao status
```

Mostra todos os ingredientes com:
- ✅ Estoque ok
- ⚠️ Estoque baixo (abaixo do limite definido)
- 🔴 Vencido ou em quarentena

---

### ➕➖ Registrar consumo ou reposição

Para **consumir** (saída de estoque):
```
estocapao update farinha -3
```
_(remove 3 kg de farinha do estoque)_

Para **repor** (entrada de estoque):
```
estocapao update farinha 10
```
_(adiciona 10 kg de farinha ao estoque)_

---

### 🗑️ Descartar um lote danificado

```
estocapao discard farinha
```

O lote vai para **quarentena** (não some dos registros, apenas fica separado do estoque ativo).

---

## Exemplo de um dia completo de uso

```
# Manhã: chegou uma entrega de fermento e manteiga
estocapao add fermento 5 --exp 2026-06-25 --limit 1
estocapao add manteiga 12 --exp 2026-06-20 --limit 3

# Durante o dia: produção consumiu ingredientes
estocapao update farinha -8
estocapao update fermento -1.5
estocapao update manteiga -4

# Fim do turno: conferência do estoque
estocapao status

# Uma embalagem de manteiga caiu no chão e não pode ser usada
estocapao discard manteiga
```

---

## ❓ Deu algum erro?

| Mensagem de erro | O que fazer |
| :--- | :--- |
| `estocapao: comando não encontrado` | Feche e abra um novo terminal e tente de novo |
| `python: comando não encontrado` | Reinstale o Python marcando "Add to PATH" |
| `FileNotFoundError: config.ini` | Rode `copy config.ini.example config.ini` e depois `estocapao --init` |
| Qualquer outro erro | Verifique o arquivo `estocapao.log` na pasta do projeto para detalhes |

---

## 🔄 Atualizar o programa (versão nova disponível)

```
git pull
pip install .
```

---

*EstocaPão — Feito com ❤️ por Kalyel N. | Software Developer*
