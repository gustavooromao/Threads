import threading
import subprocess
import time
import datetime

import pyautogui
import pygetwindow as gw

'''
 Event usado para SINCRONIZAR as duas threads: a thread de escrita só pode agir depois que a thread de abertura sinalizar que o Bloco de Notas já está realmente aberto e pronto para receber o texto.
'''

bloco_pronto = threading.Event()


def hora():
    """Retorna o horário atual formatado (HH:MM:SS), usado nas mensagens de log."""
    return datetime.datetime.now().strftime("%H:%M:%S")


def abrir_bloco_de_notas():
    """Thread 1 - Parte 1: abre o Bloco de Notas do Windows."""
    print(f"[{hora()}] Thread 'Abertura' iniciada.")


    # Cria um novo PROCESSO do Windows para o Bloco de Notas
    processo = subprocess.Popen(["notepad.exe"])
    print(f"[{hora()}] Bloco de Notas solicitado (PID do processo: {processo.pid}).")

    """Aguarda a janela do Bloco de Notas realmente existir antes de liberar a próxima etapa (evita que a Thread 2 escreva "no vazio").""" 
    janela_encontrada = False
    tentativas = 0
    while not janela_encontrada and tentativas < 20:
        titulos = gw.getAllTitles()
        if any("notepad" in t.lower() or "bloco de notas" in t.lower() for t in titulos):
            janela_encontrada = True
        else:
            time.sleep(0.3)
            tentativas += 1

    print(f"[{hora()}] Thread 'Abertura' concluída. Bloco de Notas está pronto para uso.")

    # Sinaliza para a Thread 2 que ela já pode escrever
    bloco_pronto.set()


def escrever_texto():
    """Thread 2 - Parte 2: escreve automaticamente um texto no Bloco de Notas."""
    print(f"[{hora()}] Thread 'Escrita' iniciada (aguardando o Bloco de Notas abrir)...")

    # Espera o sinal da Thread 1 - é a sincronização entre as duas threads
    bloco_pronto.wait()

    # Traz a janela do Bloco de Notas para frente antes de digitar
    janelas = gw.getWindowsWithTitle("Bloco de Notas") or gw.getWindowsWithTitle("Notepad")
    if janelas:
        janelas[0].activate()
        time.sleep(0.3)

    texto = (
        "Nome: Gustavo Romao\n"
        "Disciplina: Sistemas Operacionais\n"
        f"Data da execucao: {datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n"
        "Frase: Sem objetivo = Sem resultados !\n"
    )

    pyautogui.typewrite(texto, interval=0.03)

    print(f"[{hora()}] Thread 'Escrita' concluída. Texto inserido com sucesso.")


if __name__ == "__main__":
    print(f"[{hora()}] Programa principal iniciado (processo pai).")

    thread_abertura = threading.Thread(target=abrir_bloco_de_notas, name="Thread-Abertura")
    thread_escrita = threading.Thread(target=escrever_texto, name="Thread-Escrita")

    thread_abertura.start()
    thread_escrita.start()

    thread_abertura.join()
    thread_escrita.join()

    print(f"[{hora()}] As duas threads terminaram. Encerrando o programa principal.")
  
# Gustavo Romão $$
