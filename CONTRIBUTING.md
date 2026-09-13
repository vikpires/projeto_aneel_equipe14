# Guia de Contribuição e Boas Práticas

Este documento orienta o fluxo de trabalho da equipe no repositório do projeto. Siga o passo a passo abaixo para garantir que todos trabalhem de forma sincronizada e sem conflitos de código.

---

## Sumário

- [1. Configuração Inicial do Ambiente](#1-configuração-inicial-do-ambiente)
- [2. Fluxo de Trabalho com Git](#2-fluxo-de-trabalho-com-git)
- [3. Gestão de Tarefas com GitHub Projects](#3-gestão-de-tarefas-com-github-projects)

---

## 1. Configuração Inicial do Ambiente

Escolha uma das abordagens abaixo de acordo com a sua preferência (Google Colab ou máquina local):

### Opção A: Execução via Google Colab

- Acesse o **Google Colab**.

- Selecione a aba `GitHub`, vincule sua conta e escolha o repositório do projeto.

- Abra o notebook desejado a partir da sua branch de trabalho (Branch padrão: `develop`).

- Para salvar alterações: vá em `Arquivo > Salvar uma cópia no GitHub...`, e insira a mensagem de commit.

- Para clonar o repositório e baixar os dados de Release, siga as instruções do arquivo: [references/download_release.ipynb](references/download_release.ipynb)

> [!WARNING]  
> Atenção no Colab: O armazenamento temporário é volátil. Sempre salve sua cópia no GitHub antes de fechar a aba do navegador. Nunca salve senhas, tokens ou credenciais nas células de código.

---

### Opção B: Configuração Local (VS Code / Terminal)

#### **1. Clonar o Repositório:**

```bash
git clone git@github.com:vikpires/projeto_aneel_equipe14.git
cd projeto_aneel_equipe14

```

#### **2. Criar e Ativar o Ambiente Virtual:**

- Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

- Linux/macOS:

```bash
cd projeto_aneel_equipe14
python3 -m venv .venv
source .venv/bin/activate
```

#### **3. Instalar as Dependências:**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

#### **4. Executar Script do Pipeline:**

```bash
python main.py
```

---

## 2. Fluxo de Trabalho com Git

> 📌 **Branch Principal de Trabalho:** Todo o desenvolvimento do projeto acontece a partir da branch **`develop`**, configurada como padrão. A branch `main` é restrita apenas para entregas finais avaliadas.

#### **1. Garantir que a branch `develop` está ativa e atualizada antes de iniciar qualquer alteração:**

```bash
git checkout develop      # Troca para a branch develop, caso esteja em outra
git fetch origin          # Busca novidades no GitHub sem aplicá-las ainda
git pull origin develop   # Baixa e sincroniza as atualizações mais recentes
```

> [!TIP]
> Se estiver no Google Colab, utilize o sinal de exclamação (!) antes de qualquer comando git. Ex.: `!git pull`

#### **2. Após realizar as alterações nos arquivos, salvar o progresso:**

```bash
git add . # Adiciona as alterações salvas no Stage
git commit -m ":sparkles: feat: descricao sucinta do que foi feito (#numero_da_issue)" # Salva as alterações realizadas


```

> [!NOTE]  
> Na aba Issues ou Project do GitHub, consulte o identificador numérico da task após o título (ex.: `Task 1.1 - Ingestão de Dados #2`). Inserir `#2` vincula automaticamente o commit ao card.

**Exemplos de Mensagens de Commits:**

:sparkles: feat: adiciona notebook de analise exploratoria (#6)

:recycle: refactor: adiciona notebook de analise exploratoria (#6)

:bug: fix: corrige tipagem da coluna de apuracao (#8)

:wrench: chore: atualiza dicionario de dados (#4)

:books: docs: adiciona o arquivo de README (#1)

> [!TIP]  
> Para saber mais, acesse o link sobre [padrões de commits](https://github.com/iuricode/padroes-de-commits).

#### **3. Envio do commit para o GitHub:**

```bash
git push origin develop
```

> [!CAUTION]
> Aviso importante: Evite editar um mesmo arquivo no qual outra pessoa esteja trabalhando simultaneamente para evitar conflitos de versão.

---

## 3. Gestão de Tarefas com GitHub Projects

Para a organização e o acompanhamento das atividades da equipe, utilizamos o **GitHub Projects** integrado ao repositório. O painel adota o fluxo Kanban, acessível pela aba superior **Projects** no GitHub, estruturado nas seguintes colunas:

* **Backlog:** Repositório com todas as tarefas (tasks) adicionadas aguardando escolha por um ou mais membros da equipe.

* **To Do:** Tarefas priorizadas para desenvolvimento. Cada membro deve selecionar **no máximo 2 tarefas** simultâneas para iniciar.

* **In Progress:** Tarefa em desenvolvimento ativo no momento. Mantenha apenas uma atividade aqui para manter o foco.

* **In Review:** Tarefa concluída aguardando validação de código, regras de negócio ou revisão de documentação por outro integrante do time.

* **Done:** Tarefa aprovada, validada e devidamente mesclada na branch `develop`.

### Como assumir e gerenciar uma tarefa:
1. **Escolha da tarefa:** Acesse a coluna **Backlog**, abra o card que deseja assumir e, no menu lateral direito em **Assignees**, selecione o seu usuário do GitHub.

2. **Priorização:** Mova o card para a coluna **To Do** (limite de no máximo 2 tarefas simultâneas por membro).

3. **Início do trabalho:** Ao começar o desenvolvimento técnico, arraste o card para **In Progress**.

4. **Vínculo de commits:** Sempre que realizar um commit referente à atividade, referencie o número da issue na mensagem (ex.: `:sparkles: feat: script de limpeza dec fec (#2)`) para atualizar o histórico automaticamente no Projects.

5. **Revisão entre pares:** Ao concluir a tarefa e subir os arquivos para a branch `develop`, mova o card para **In Review** e avise no grupo da equipe para que um colega confira o código/notebook.

6. **Finalização:** Após a validação do colega (e sem pendências de correção), o card é movido para **Done**, encerrando a entrega.

---
> [!NOTE]
> Estas são diretrizes gerais para padronizar o trabalho colaborativo. Qualquer dúvida técnica ou conflitos de código, informe ao grupo da equipe ou aproveite as reuniões de alinhamento.
