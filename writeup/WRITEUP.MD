# 📝 Writeup: CTF Operação Many-Time Pad

**Autor:** Luan Garcia 
**Nível:** Intermediário / Avançado
**Tópicos:** Criptoanálise, Cifras de Fluxo, Known-Plaintext Attack (KPA), Engenharia Reversa.

---

## 🔍 Resumo do Incidente

Neste cenário de resposta a incidentes, fomos acionados para investigar um ataque de ransomware customizado ("Roll your own crypto"). Os atacantes utilizavam um sistema complexo baseado em integrais triplas. No entanto, a análise revelou que, por trás da ofuscação matemática, o malware implementava uma cifra de fluxo (Stream Cipher) cíclica com uma vulnerabilidade crítica: **ausência de Vetores de Inicialização (IVs) únicos e uma semente estática**.

O desafio consistia em recuperar o banco de dados crítico da empresa (`database_corp.db.locked`) a partir de um único artefato que sobreviveu em seu estado original: o papel de parede corporativo (`wallpaper.jpg`).

---

## 🛠️ Análise Inicial e Vetor de Exploração

Recebemos três artefatos:
1. `wallpaper.jpg` (Arquivo Original / Plaintext - 80 KB)
2. `wallpaper.jpg.locked` (Arquivo Criptografado / Ciphertext - 80 KB)
3. `database_corp.db.locked` (Alvo Principal - 500 KB)

Em criptografia baseada em XOR ($\oplus$), sabemos que a cifra de fluxo gera um Keystream ($K$) que é combinado com o Plaintext ($P$) para gerar o Ciphertext ($C$):
> $P \oplus K = C$

Devido à propriedade reversível do XOR, se possuímos o arquivo original e o criptografado, podemos isolar o fluxo da chave:
> $P \oplus C = K$

---

## 🔓 Fase 1: Known-Plaintext Attack (KPA)

O primeiro passo é extrair o keystream parcial usando o wallpaper. Como o atacante reutilizou a chave (vulnerabilidade de *Many-Time Pad*), a chave do wallpaper é a mesma do banco de dados.

Fazendo o XOR byte a byte entre `wallpaper.jpg` e `wallpaper.jpg.locked`, conseguimos recuperar exatos **80 KB** de keystream.

---

## 🧠 Fase 2: O Pulo do Gato (Slack Space e Null Bytes)

Aqui encontramos um obstáculo intencional: o wallpaper possui 80 KB, mas o banco de dados possui 500 KB. Se aplicarmos apenas 80 KB em ciclo, o banco de dados será corrompido, pois o ciclo real do PRNG do malware é ligeiramente maior.

Como descobrimos o restante da chave?
Bancos de dados possuem um vasto *Slack Space* (espaços vazios preenchidos por Null Bytes - `0x00`). Pela propriedade de identidade do XOR, sabemos que:
> $0x00 \oplus K = K$

Isso significa que, nas áreas vazias do banco de dados, **o arquivo criptografado expõe o próprio Keystream em texto claro**. Ao inspecionar o arquivo `database_corp.db.locked`, notamos que o padrão de ruído entra em ciclo a cada **100 KB**. 

Comprovamos isso extraindo 100 KB do arquivo `.locked` e validando os 80 KB iniciais contra a chave extraída do wallpaper. O match foi de 100%.

---

## 🚀 Fase 3: Descriptografia e Captura da Flag

Com o ciclo completo de 100 KB em mãos, basta aplicar o XOR modular sobre todo o arquivo de 500 KB do banco de dados:
> $C_i \oplus K_{(i \mod 100KB)} = P_i$

Após gerar o `database_recuperado.db`, podemos rodar um simples comando `strings` para localizar a flag escondida no meio do banco de dados:

```bash
strings database_recuperado.db | grep CTF
``` 
