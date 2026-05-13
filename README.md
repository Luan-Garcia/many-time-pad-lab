# 🏴‍☠️ CTF: Operação Many-Time Pad (Baseado em Fatos Reais)

Sejam bem-vindos a um laboratório de CTF criado baseado em um incidente de resposta a ransomware em larga escala. Neste caso, o grupo criminoso havia desenvolvido sua própria criptografia para poder crptografar o malware, o cerne deste modelo focava em Integrais Triplas, mas falharam no modelo de implementação.

Atue como um Security Engineer contratado para resgatar os dados da empresa sem pagar um único centavo de resgate.

## 📜 O Cenário

A empresa CorpX sofreu um ataque massivo. Mais de 1.000 máquinas e Terabytes de dados foram criptografados com uma extensão `.locked`. Analistas descobriram que o ransomware utiliza um algoritmo proprietário bizarro baseado em cálculo multivariável. 

O cliente não tem backups recentes do banco de dados principal. No entanto, durante a triagem, você encontrou **um único arquivo original** que sobreviveu em um pendrive esquecido: o papel de parede padrão das máquinas da empresa (`logo_empresa.png`).

Na máquina infectada, você coletou a versão criptografada desse mesmo logo (`logo_empresa.png.locked`), além do alvo principal: o banco de dados da empresa (`database_critico.db.locked`).

## 🎯 Objetivo

Sua missão é extrair a chave de criptografia explorando falhas na implementação do algoritmo e aplicá-la para recuperar o banco de dados. 
Dentro do banco de dados recuperado, você encontrará a Flag.

**Formato da Flag:** `CTF{...}`

## 📁 Arquivos Fornecidos

Neste repositório, você tem:
1. `logo_empresa.png` -> O arquivo original em texto claro (Plaintext).
2. `logo_empresa.png.locked` -> O mesmo arquivo cifrado pelo ransomware.
3. `database_critico.db.locked` -> O banco de dados sequestrado.

## 🧠 Dicas (Se precisar)
* Como funciona o processo de operação XOR em cifras de fluxo? Se $P \oplus K = C$, como você acha o $K$?
* A chave gerada pelo malware não é infinita, ela entra em loop (é cíclica). Tente descobrir como aplicar um pedaço pequeno de chave em um arquivo muito grande.
* Depois de descriptografar o DB, não tente abrir em um visualizador. Comandos simples de terminal (como `strings` no Linux) são seus melhores amigos.

# ❗ Write-up
* O Write-up está descrito na pasta write-up. O processo está descrito em um arquivo nomeado de WRITEUP.md e todos os códigos utilizados estão nesta pasta.

---
*Autor: Luan Garcia - Security Researcher and Pentester*
