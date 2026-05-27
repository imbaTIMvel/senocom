# SeNoCom

Repositório oficial do programa SeNoCom (*Se*para e *No*meia *Com*provantes), para separar e nomear comprovantes automaticamente.

![Ícone - SeNoCom](assets/icons/senocom.ico)

## 1. Requisitos

Para uso adequado do programa, o usuário deve possuir:
- **Sistema Operacional:** Windows 10 ou 11

Para uso da funcionalidade de conversão `DOC/DOCX`→`PDF`, o usuário deve ter o *Microsoft Word* instalado na versão mais recente.

## 2. Guia de Uso

### 2.1 Baixando e Instalando o Programa

Para usar o `JuntaPDF`, primeiro, você deve baixar o arquivo `.exe` disponível [aqui](https://github.com/imbaTIMvel/juntapdf/releases). Procure pela versão mais recente (*Latest*) e clique no arquivo `.exe` para fazer o download.

> [!Warning]
> Caso você ainda tenha o executável de uma versão antiga do programa, recomenda-se excluí-lo.

Baixado o programa, você pode colocar o arquivo `.exe` onde achar melhor.

### 2.2 Abrindo o Programa

Feito isso, clique no arquivo `.exe` para abrir o programa.

![Abrindo o .exe](assets/tutorial/exe_in_downloads.png)

> [!Warning]
> É possível que o *Windows Defender* acuse o programa como "software perigoso". Neste caso, para executá-lo, você deve clicar em `Mais Informações` e, depois, no botão `Executar assim mesmo`.

![Windows Defender acusando o programa](assets/tutorial/windows_defender_01.png)

![Executar assim mesmo](assets/tutorial/windows_defender_02.png)

Antes de iniciar uma operação, junte os arquivos que você deseja emendar em uma pasta. O programa utiliza uma convenção de nomenclatura de arquivos para saber quais arquivos emendar e em que ordem fazê-lo.

### 2.3 Organizando os Arquivos de Entrada

Todos os arquivos colocados na pasta devem ser nomeados como:

`nome_numero.pdf`

Sendo que:
- `nome` pode ser qualquer texto (incluindo letras maiúsculas, minúsculas, acentos, sinais e números)
- `_` entre `nome` e `numero` é **INDISPENSÁVEL**
- `numero` deve ser expresso em números inteiros, na ordem desejada para emenda dos arquivos do conjunto `nome`
- O conjunto de arquivos de entrada com o mesmo elemento `nome` será mesclado em um único arquivo `nome.pdf`, seguindo a ordem dos índices `numero`

Para que o programa seja capaz de processá-los e emendá-los adequadamente.

Observe o exemplo:

![Pasta "test_0"](assets/tutorial/test_files.png)

Aqui, tenho 5 diferentes grupos de arquivos (disponíveis na pasta [test/test_0](test/test_0)):
- Grupo "batch": `batch_1.pdf`, `batch_2.pdf`
- Grupo "copy_test": `copy_test_1.pdf`, `copy_test_2.pdf`, `copy_test_3.doc`, `copy_test_4.pdf`, `copy_test_5.pdf`
- Grupo "exodia": `exodia_0.pdf`, `exodia_1.pdf`, `exodia_2.pdf`, `exodia_3.pdf`, `exodia_4.pdf`
- Grupo "lorem ipsum": `lorem ipsum_1.pdf`, `lorem ipsum_2.pdf`, `lorem ipsum_3.pdf`, `lorem ipsum_4.pdf`, `lorem ipsum_5.pdf`, `lorem ipsum_6.pdf`, `lorem ipsum_7.pdf`, `lorem ipsum_8.pdf`, `lorem ipsum_9.pdf`, `lorem ipsum_10.pdf`, `lorem ipsum_11.docx`
- Grupo "something 04-05-26": `something 04-05-26_1.pdf`, `something 04-05-26_2.pdf`, `something 04-05-26_3.pdf`, `something 04-05-26_4.pdf`, `something 04-05-26_5.pdf`, `something 04-05-26_6.pdf`

O programa reconhece o grupo do arquivo e a ordem em que ele deve ser emendado ao arquivo de saída através da nomenclatura do documento. Tomemos o arquivo `lorem ipsum_5.pdf`, por exemplo:
- Nome do arquivo (sem a extensão): `lorem ipsum_5`
- Texto **antes** do underscore ("_"): `lorem ipsum`
- Texto **depois** do underscore ("_"): `5`
Logo, este arquivo pertence ao grupo "lorem ipsum", e é o arquivo de índice 5.

Para o conjunto de arquivos apresentados acima, o programa processará os seguintes arquivos de saída:
- `batch.pdf`
- `copy_test.pdf`
- `exodia.pdf`
- `lorem ipsum.pdf`
- `something 04-05-26.pdf`

Em suma:

| Arquivos de entrada | Operação | Arquivo(s) de saída | Nota |
| ------------------- | -------- | ------------------- | ---- |
| `batch_1.pdf`, `batch_2.pdf` | Emendar na ordem: batch_1 + batch_2 | `batch.pdf` | Arquivos de entrada disponíveis em [test_batch](test/test_batch) |
| `copy_test_1.pdf`, `copy_test_2.pdf`, `copy_test_3.doc`, `copy_test_4.pdf`, `copy_test_5.pdf` | Converter `copy_test_3.doc` em `copy_test_3.pdf`. Emendar na ordem: copy_test_1 + copy_test_2 + copy_test_3 + copy_test_4 + copy_test_5 | `copy_test.pdf` | Arquivos de entrada disponíveis em [test_copy_test](test/test_copy_test) |
| `exodia_0.pdf`, `exodia_1.pdf`, `exodia_2.pdf`, `exodia_3.pdf`, `exodia_4.pdf` | Emendar na ordem: exodia_0 + exodia_1 + exodia_2 + exodia_3 + exodia_4 | `exodia.pdf` | Arquivos de entrada disponíveis em [test_exodia](test/test_exodia) |
| `lorem ipsum_1.pdf`, `lorem ipsum_2.pdf`, `lorem ipsum_3.pdf`, `lorem ipsum_4.pdf`, `lorem ipsum_5.pdf`, `lorem ipsum_6.pdf`, `lorem ipsum_7.pdf`, `lorem ipsum_8.pdf`, `lorem ipsum_9.pdf`, `lorem ipsum_10.pdf`, `lorem ipsum_11.docx` | Converter `lorem ipsum_11.docx` em `lorem ipsum_11.pdf`. Emendar na ordem: lorem_ipsum_1 + lorem_ipsum_2 + lorem_ipsum_3 + lorem_ipsum_4 + lorem_ipsum_5 + lorem_ipsum_6 + lorem_ipsum_7 + lorem_ipsum_8 + lorem_ipsum_9 + lorem_ipsum_10 + lorem_ipsum_11 | `lorem_ipsum.pdf` | Arquivos de entrada disponíveis em [test_lorem_ipsum](test/test_lorem_ipsum) |
| `something 04-05-26_1.pdf`, `something 04-05-26_2.pdf`, `something 04-05-26_3.pdf`, `something 04-05-26_4.pdf`, `something 04-05-26_5.pdf`, `something 04-05-26_6.pdf` | Emendar na ordem: something 04-05-26_1 + something 04-05-26_2 + something 04-05-26_3 + something 04-05-26_4 + something 04-05-26_5 + something 04-05-26_6 | `something 04-05-26.pdf` | Arquivos de entrada disponíveis em [test_something](test/test_something) |

### 2.4 Selecionando a Pasta

Na janela do programa, clique no botão `Selecionar Pasta` para escolher a pasta onde seus arquivos de entrada estão salvos.

![Clicando no botão](assets/tutorial/input_folder_01.png)

![Escolhendo pasta de entrada](assets/tutorial/input_folder_02.png)

### 2.5 Emendando os Arquivos

Para emendar os PDFs, clique no botão `Juntar PDFs`.

![Clicando no botão](assets/tutorial/link_pdfs_01.png)

![Emendando PDFs](assets/tutorial/link_pdfs_02.png)

Após o processamento dos arquivos, o programa abrirá uma janela para que você escolha a pasta onde os arquivos de saída serão salvos.

![Escolhendo pasta de saída](assets/tutorial/end_of_operation_01.png)

![Mensagem de sucesso](assets/tutorial/end_of_operation_02.png)

![PDFs emendados](assets/tutorial/end_of_operation_03.png)

## 3. Releases

### `v0.1.0` JuntaPDF (*beta release*)

> [!Warning]
> O lançamento beta (*beta release*) foi desenvolvido para **testes internos**, visando identificar e corrigir bugs antes do lançamento de uma versão estável.

Data de lançamento: `13/05/2026`

Para fazer o download desta versão, clique [aqui](https://github.com/imbaTIMvel/juntapdf/releases/download/v0.1.0/JuntaPDF.exe).

*Release* inicial do programa de emenda local de arquivos PDF e documentos Word (.doc e .docx) em lote.

**Features:**

- Recebe arquivos .pdf, juntando-os em PDFs "costurados" de acordo com a nomenclatura e numeração dos arquivos. Por exemplo:
  - Arquivos de entrada: `string1_1.pdf`, `string1_2.pdf`, `...`, `string1_10.pdf`, `string2_1.pdf`, `string2_2.pdf`, `...`, `string2_10.pdf`, `string3_1.pdf`, `string3_2.pdf`, `...`, `string3_10.pdf`;
  - Arquivos de saída: `string1.pdf`, `string2.pdf`, `string3.pdf`
  - Onde "string1", "string2" e "string3" podem ser quaisquer strings de texto (incluindo letras maiúsculas, minúsculas, acentos, sinais e números).
- Compatível com arquivos .doc e .docx, convertendo-os em .pdf antes da mescla.
- Permite que o usuário escolha o diretório de salvamento para o(s) arquivo(s) de saída.

Clique [aqui](https://github.com/imbaTIMvel/juntapdf/releases) para acessar o **changelog completo**.

## 4. Desenvolvimento

#### Autor:

Timóteo Altoé (*handle:* [imbaTIMvel](https://github.com/imbaTIMvel))

#### Datas:

`04/05/2026` Início do projeto

`05/05/2026` Lançamento da versão *alfa* - para testes internos

`13/05/2026` Publicação da primeira versão oficial no GitHub

`21/05/2026` Lançamento da versão *beta* - para testes
