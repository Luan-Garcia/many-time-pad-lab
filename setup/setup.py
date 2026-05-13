import hashlib
import logging
import secrets
import sys
from pathlib import Path
from itertools import cycle

# =============================================================================
# Configuração de Logs e Constantes 
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Extrair "Magic Numbers" para o topo facilita a manutenção do código
TAMANHO_CHAVE = 100 * 1024      # 100 KB
TAMANHO_WALLPAPER = 80 * 1024   # 80 KB
TAMANHO_DB = 500 * 1024         # 500 KB
SEED = "CHANGEME"
FLAG = b"CTF{m4th_c4nt_s4v3_b4d_k3y_m4n4g3m3nt}"

# =============================================================================
# Funções do Laboratório
# =============================================================================

def simular_integral_tripla(seed: str, tamanho_desejado: int) -> bytes:
    """
    Simula o motor de criptografia ruim do ransomware.
    Gera um keystream estático baseado em uma semente fixa via Hash Chaining.
    """
    logger.info(f"Gerando {tamanho_desejado} bytes de keystream estático (PRNG determinístico)...")
    
    keystream = bytearray()
    hash_atual = hashlib.md5(seed.encode()).digest()
    
    # Adiciona blocos de 16 bytes (MD5), o que simula a geração de integral
    while len(keystream) < tamanho_desejado:
        keystream.extend(hash_atual)
        hash_atual = hashlib.md5(hash_atual).digest()
        
    return bytes(keystream[:tamanho_desejado])

def encriptar_arquivo(caminho_arquivo: Path, keystream: bytes, sufixo: str = ".locked") -> Path:
    """
    Lê o arquivo original, aplica o XOR cíclico de alta performance e salva a versão sequestrada.
    """
    logger.info(f"Sequestrando artefato: {caminho_arquivo.name}")
    
    try:
        dados_originais = caminho_arquivo.read_bytes()
    except IOError as e:
        logger.error(f"Falha ao ler o arquivo {caminho_arquivo}: {e}")
        raise

    # Abordagem Pythonic: O itertools.cycle repete a chave infinitamente.
    # O zip combina os bytes sem precisarmos gerenciar o operador de módulo (%) manualmente.
    dados_cifrados = bytes([byte_arquivo ^ byte_chave for byte_arquivo, byte_chave in zip(dados_originais, cycle(keystream))])
    
    caminho_saida = caminho_arquivo.with_suffix(caminho_arquivo.suffix + sufixo)
    
    try:
        caminho_saida.write_bytes(dados_cifrados)
    except IOError as e:
        logger.error(f"Falha ao gravar arquivo criptografado {caminho_saida}: {e}")
        raise
        
    return caminho_saida

def criar_cenario_ctf() -> None:
    """
    Criação do ambiente: gera arquivos, injeta a flag e simula o ataque.
    """
    try:
        # 1. Gera a chave mestra com a vulnerabilidade
        chave_mestra = simular_integral_tripla(SEED, TAMANHO_CHAVE)
        
        # 2. Cria o arquivo Wallpaper usando gerador seguro de entropia
        caminho_wallpaper = Path("wallpaper.jpg")
        caminho_wallpaper.write_bytes(secrets.token_bytes(TAMANHO_WALLPAPER)) 
        logger.info("Artefato original (Wallpaper) gerado com sucesso.")
        
        # 3. Cria o Banco de Dados com a Flag escondida no 'Slack Space' 
        caminho_db = Path("database_corp.db")
        db_dados = bytearray(b"\x00" * TAMANHO_DB)
        
        offset_injecao = TAMANHO_DB // 2
        db_dados[offset_injecao:offset_injecao + len(FLAG)] = FLAG
        caminho_db.write_bytes(db_dados)
        logger.info("Banco de dados provisionado e Flag injetada.")
        
        # 4. Simula ataque Ransomware
        encriptar_arquivo(caminho_wallpaper, chave_mestra)
        encriptar_arquivo(caminho_db, chave_mestra)
        
        # 5. Simula a perda dos dados 
        caminho_db.unlink()
        logger.info("Banco de dados original apagado (simulando criptografia destrutiva).")
        
        print("\n[+] Setup do Lab concluído! Arquivos prontos para o CTF:")
        print(f" ├── {caminho_wallpaper.name}")
        print(f" ├── {caminho_wallpaper.name}.locked")
        print(f" └── {caminho_db.name}.locked")
        
    except Exception as e:
        logger.critical(f"Erro ao provisionar o cenário do CTF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    criar_cenario_ctf()
