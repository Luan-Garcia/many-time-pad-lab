import sys

def solve():
    print("[*] Iniciando resgate...")

    # =========================================================================
    # 1. Known-Plaintext Attack (KPA) e Extração de PRNG
    # =========================================================================
    # Explorando a vulnerabilidade de Many-Time Pad. Como o algoritmo proprietário 
    # não utiliza IVs (Initialization Vectors) únicos por arquivo, o keystream 
    # se repete, permitindo a extração via XOR.
    with open("wallpaper.jpg", "rb") as f_orig, open("wallpaper.jpg.locked", "rb") as f_cifr:
        wall_orig = f_orig.read()
        wall_cifr = f_cifr.read()
        
    # Isolamento do Keystream (K). 
    # Propriedade matemática: se C = P ⊕ K, então K = P ⊕ C.
    keystream_parcial = bytearray([a ^ b for a, b in zip(wall_orig, wall_cifr)])
    print(f"[*] Keystream parcial recuperado: {len(keystream_parcial)} bytes.")
    
    # =========================================================================
    # 2. Key Extension via Leak de Null-Bytes
    # =========================================================================
    # O Wallpaper possui apenas 80KB, mas a cifra entra em 
    # ciclo em 100KB. A aplicação prematura do módulo corromperia os dados.
    # Solução: Bancos de dados possuem grande quantidade de 'slack space' (0x00).
    # Pela propriedade da identidade do XOR (0x00 ⊕ K = K), o arquivo cifrado
    # expõe o keystream em plain sight nas áreas vazias.

    with open("database_corp.db.locked", "rb") as f_db_locked:
        db_cifrado = f_db_locked.read()
        
    # Extraindo o limite real do ciclo determinístico
    tamanho_real_chave = 100 * 1024
    keystream_completo = bytearray(db_cifrado[:tamanho_real_chave])
    
    # Validação Criptográfica: Confirma a consistência do fluxo parcial recuperado
    # contra o fluxo extraído do DB, provando a estaticidade do PRNG.
    if keystream_completo[:len(keystream_parcial)] == keystream_parcial:
        print(f"[+] Integridade de fluxo validada. Tamanho do ciclo: {tamanho_real_chave} Bytes.")
    else:
        print("[-] Inconsistência no PRNG detectada. Abortando operação.")
        sys.exit(1)

    # =========================================================================
    # 3. Descriptografia em Massa e Quebra da Criptografia
    # =========================================================================
    db_recuperado = bytearray()
    
    # Aplicação do ataque. O índice modular (i % tamanho_real_chave) explora 
    # a falha de reinicialização cíclica do algoritmo (falta de difusão/entropia).
    for i, byte in enumerate(db_cifrado):
        db_recuperado.append(byte ^ keystream_completo[i % tamanho_real_chave])
        
    with open("database_recuperado.db", "wb") as f_out:
        f_out.write(db_recuperado)
        
    print("[+] Operação concluída. Arquivo gerado: database_recuperado.db")

if __name__ == "__main__":
    solve()
