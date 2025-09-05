# N1 - Atividade Cifra de César + Diffie Hellman (Criptografia Simétrica)

![N1](https://img.shields.io/badge/atividade-N1-blue) ![Python](https://img.shields.io/badge/python-3.8%2B-green) ![Licença](https://img.shields.io/badge/license-MIT-lightgrey)

> Projeto didático que combina um *handshake* Diffie–Hellman simples para derivação de chave com uma cifra por deslocamento a nível de bytes (estilo "Cifra de César" por bytes) — comunicação cliente/servidor via TCP sockets.

---

## Visão geral

O objetivo deste projeto é demonstrar, de forma prática e simples, como dois pares (cliente e servidor) podem:

1. Trocar valores públicos e calcular uma chave secreta compartilhada usando Diffie–Hellman.
2. Usar essa chave como deslocamento (K) para cifrar/decifrar mensagens por adição/subtração de bytes.
3. Enviar/receber mensagens através de sockets TCP.

> **Importante:** Esta implementação é educacional — **não** deve ser usada em produção. A chave é pequena (módulo `N` no exemplo é 127) e a cifra é trivial; para aplicações reais use bibliotecas de criptografia consolidadas (ex.: `cryptography`).

---

## Funcionalidades principais

* Handshake Diffie–Hellman (classe `DiffieHellman` em `modules/dh.py`).
* Cifra simples por deslocamento de bytes (`CriptoSuperCão` em `modules/criptografia.py`).
* Exemplo de servidor (`server.py`) que recebe, decifra, processa (converte para MAIÚSCULAS) e responde.
* Exemplo de cliente (`client.py`) que envia uma mensagem, recebe resposta e decifra.

---

## Estrutura do projeto

```
project-root/
├─ client.py            # cliente TCP
├─ server.py            # servidor TCP
├─ modules/
│  ├─ criptografia.py   # CriptoSuperCão (handshake + cifragem/decifragem)
│  └─ dh.py             # DiffieHellman (G, N, R, K)
├─ README.md            # (este arquivo)
└─ requirements.txt     # dependências (opcional)
```

---

## Pré-requisitos

* Python 3.8 ou superior
* Dependências listadas em `requirements.txt` (apenas `yaspin` no exemplo)

Exemplo de `requirements.txt`:

```
yaspin
```

Instalação (recomendado criar virtualenv):

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate    # Windows (PowerShell/CMD)
pip install -r requirements.txt
```

Ou instalar direto:

```bash
pip install yaspin
```

---

## Como executar

1. Abra um terminal e rode o servidor:

```bash
python server.py
```

2. Em outro terminal rode o cliente (no mesmo host usa `localhost`):

```bash
python client.py
```

> Se servidor e cliente estiverem em máquinas diferentes, ajuste `serverName` em `client.py` para o IP do servidor (porta padrão: `1300`).

---

## Exemplos de comportamento (console)

**Cliente**

```
Mensagem enviada original:  ola mundo
Mensagem enviada criptogradada:  bytearray(b'...')
Mensagem recebida criptogradada:  bytearray(b'...')
Mensagem recebida original:  OLA MUNDO
```

**Servidor**

```
Mensagem recebida criptogradada:  bytearray(b'...')
Mensagem recebida original:  ola mundo
Mensagem enviada original:  OLA MUNDO
Mensagem enviada criptogradada:  bytearray(b'...')
```

---

## Como funciona (passo a passo)

1. **Diffie–Hellman**

   * `DiffieHellman(G, N)` gera um valor secreto aleatório `meuvalor` e calcula `R = G**meuvalor mod N`.
   * `client` envia seu `R` ao `server`. O `server` envia o seu `R` de volta.
   * Cada lado chama `calcK(outroR)` para calcular `K = outroR**meuvalor mod N` — chave compartilhada.

2. **Cifragem / Decifragem (CriptoSuperCão)**

   * `criptografar(dh, sentence)` transforma a `sentence` em `bytearray`, somando `dh.K` a cada byte.
   * `decriptografar(dh, sentence)` subtrai `dh.K` de cada byte e decoda de volta para `utf-8`.

3. **Troca de mensagens**

   * Cliente cifra e envia; servidor decifra, processa (ex.: `upper()`), cifra a resposta e envia de volta; cliente decifra.

---

## APIs / Assinaturas relevantes

* `DiffieHellman(G: int, N: int)`

  * `calcR()` — calcula `self.R` (invocado no construtor)
  * `calcK(outroR: int)` — calcula `self.K`

* `CriptoSuperCão` (métodos estáticos):

  * `client_conversa(dh: DiffieHellman, clientSocket: socket)` — realiza a troca inicial de `R`s (cliente -> servidor -> cliente)
  * `server_conversa(dh: DiffieHellman, connectionSocket: socket)` — realiza a troca inicial de `R`s (recebe do cliente e responde)
  * `criptografar(dh: DiffieHellman, sentence: str) -> bytearray` — cifra por deslocamento de bytes
  * `decriptografar(dh: DiffieHellman, sentence: bytearray) -> str` — decifra e retorna string

---

## Observações de segurança (leia com atenção)

* **Não use** esta implementação em sistemas reais. Motivos principais:

  * Módulo `N` muito pequeno (127 no exemplo) → espaço de chaves muito restrito.
  * Cifra por soma de bytes é equivalente a uma cifra de substituição com deslocamento fixo — trivialmente quebrável.
  * Ausência de autenticação (man-in-the-middle possível) e ausência de integridade/assinatura.
  * Uso de `random.randint` em vez de `secrets` para gerar segredo; usar `secrets.randbelow` seria mais adequado.

**Melhorias recomendadas:**

* Usar primos grandes e geradores seguros (bibliotecas como `pycryptodome` ou `cryptography`).
* Substituir a cifra caseira por AES-GCM (autenticação + confidencialidade) via `cryptography`.
* Autenticar peers (certificados, chaves públicas assinadas) para evitar MITM.
* Usar `secrets` para geração de valores secretos.

---

## Testes sugeridos

* Teste handshake trocando `G`/`N` diferentes e verificando que `cliente.K == servidor.K`.
* Teste mensagens vazias, mensagens com acentuação e caracteres especiais.
* Teste envio de mensagens maiores (atenção ao buffer `recv(65000)`).

---

## TODO / Possíveis melhorias

* Extrair constantes (porta, G, N) para um arquivo de configuração.
* Implementar logs mais claros (ex.: `logging` configurável).
* Substituir implementação caseira por primitives seguras.
* Adicionar testes automatizados (pytest).

---

## Contribuindo

1. Abra uma *issue* descrevendo a melhoria/bug.
2. Fork e crie um *pull request* com alterações e testes.

---

## Licença

Este projeto está sob a licença **MIT**.

---
