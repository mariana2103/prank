import os
import sys
import time
import threading
import webbrowser
import ctypes
import subprocess
import winreg

# ─── auto-install deps ─────────────────────────────────────────────────────────
REQUIRED = {"pygetwindow": "pygetwindow", "pystray": "pystray", "PIL": "Pillow", "keyboard": "keyboard"}
for mod, pkg in REQUIRED.items():
    try:
        __import__(mod)
    except ImportError:
        print(f"Instalando {pkg}...")
        subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)

import pygetwindow as gw
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import keyboard

# ╔══════════════════════════════════════════════════════════════╗
# ║  ANJO V14 - WINDOWS EDITION                                  ║
# ║                                                              ║
# ║  HOTKEY SECRETO: muda aqui se quiseres outro atalho         ║
# ║  (ctrl+alt+shift+a  significa: CTRL + ALT + SHIFT + A)      ║
# ╚══════════════════════════════════════════════════════════════╝

HOTKEY_SECRETO  = "ctrl+alt+shift+a"   # ← muda aqui o teu atalho secreto

LINK_VOVO  = "https://www.youtube.com/watch?v=bDCBj15vKTE"
LINK_RELAX = "https://www.youtube.com/watch?v=92xTPH7OtLs"
LINK_FOCO  = "https://www.youtube.com/watch?v=Xdn0-lnDecw"

LIMITE_SEGUNDOS = 10   # segundos no YouTube antes de disparar
VIDEO_DURACAO   = 15   # segundos que ele tem de ver cada vídeo

# ─── nome falso para o ícone (aparece no hover e no gestor de tarefas) ────────
NOME_FALSO  = "Windows Update Assistant"

ativo = True
tray_icon_ref = None

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def popup(mensagem, titulo):
    ctypes.windll.user32.MessageBoxW(0, mensagem, titulo, 0x10 | 0x1000)

def fechar_tabs_youtube():
    try:
        for w in gw.getAllWindows():
            if "YouTube" in w.title and ("Edge" in w.title or "Chrome" in w.title):
                try:
                    w.close()
                except Exception:
                    pass
    except Exception:
        pass

def abrir_video(link):
    try:
        webbrowser.open(link)
        time.sleep(4)
    except Exception as e:
        print(f"Erro ao abrir vídeo: {e}")

def youtube_esta_aberto():
    try:
        return any(
            "YouTube" in w.title and ("Edge" in w.title or "Chrome" in w.title)
            for w in gw.getAllWindows()
        )
    except Exception:
        return False

def get_frontmost_title():
    try:
        active = gw.getActiveWindow()
        return active.title if active else ""
    except Exception:
        return ""

def youtube_em_foco():
    title = get_frontmost_title()
    return "YouTube" in title and ("Edge" in title or "Chrome" in title)

# ─────────────────────────────────────────────
# WATCHER
# ─────────────────────────────────────────────

def vigiar_video(link, parar_event, msg_fecho, msg_fim=None):
    tempo_visto = 0
    while not parar_event.is_set():
        if youtube_esta_aberto():
            tempo_visto += 3
            print(f"  A ver vídeo... {tempo_visto}/{VIDEO_DURACAO}s")
            if tempo_visto >= VIDEO_DURACAO:
                print("  Tempo cumprido!")
                if msg_fim:
                    popup(msg_fim, "💌")
                parar_event.set()
                break
        else:
            print("  Fechou o vídeo — popup + reabrir + reiniciar contador!")
            tempo_visto = 3
            popup(msg_fecho, "👀")
            abrir_video(link)
        time.sleep(3)

def reproduzir_video_com_vigilancia(link, msg_fecho, msg_fim=None):
    print("A abrir vídeo...")
    abrir_video(link)
    parar = threading.Event()
    t = threading.Thread(target=vigiar_video, args=(link, parar, msg_fecho, msg_fim), daemon=True)
    t.start()
    t.join()

# ─────────────────────────────────────────────
# CICLO COMPLETO
# ─────────────────────────────────────────────

def ciclo_prank():
    print("GATILHO ATIVADO")

    fechar_tabs_youtube()
    popup("A TRABALHAR MUITO NÃO É ?",                                                                   "PRODUTIVIDADE ZERO")
    popup("PRODUTIVIDADE ZERO",                                                                          "PRODUTIVIDADE ZERO")
    popup("E depois ainda diz que trabalha? Sim confia",                                                 "PRODUTIVIDADE ZERO")
    reproduzir_video_com_vigilancia(
        LINK_VOVO,
        msg_fecho="Não estás a gostar do banger? Infelizmente vais ter de ouvir até ao fim. Upsi!",
    )
    print("Video 1 terminado.")

    fechar_tabs_youtube()
    popup("A tua namorada é um anjo na terra, linda e perfeita.",                                        "MENSAGEM DO ANJO")
    popup("Respira um pouco, relaxa, não me mates",                                                     "MENSAGEM DO ANJO")
    popup("Sabes que te amo muito certo? Reflete nisso enquanto respiras antes de vires falar comigo!", "MENSAGEM DO ANJO")
    reproduzir_video_com_vigilancia(
        LINK_RELAX,
        msg_fecho="Eu acho mesmo que tu queres relaxar! Essa tensão é provavelmente irritação não te fazem bem!",
    )
    print("Video 2 terminado.")

    fechar_tabs_youtube()
    popup("VOLTA AO TRABALHO! MEXE ESSE CU!",                                                            "AVISO FINAL")
    popup("AVISO FINAL",                                                                                  "AVISO FINAL")
    popup("Agora volta ao trabalho! Já está na altura de fazeres um caralho, pá!",                       "AVISO FINAL")
    reproduzir_video_com_vigilancia(
        LINK_FOCO,
        msg_fecho="Vá só uns 15 segundinhos! Precisas de um pouco de motivação",
        msg_fim="Okay agora a escolha é tua! Aproveita o vídeo até ao fim ou finalmente faz algo de produtivo! Um beijo e um queijo <3",
    )
    print("Video 3 terminado.")
    print("Ciclo completo.\n")

# ─────────────────────────────────────────────
# HOTKEY SECRETO
# ─────────────────────────────────────────────

def on_hotkey():
    global ativo
    ativo = not ativo
    status = "ATIVO" if ativo else "PAUSADO"
    print(f"Anjo {status} via hotkey.")
    # notificação discreta via balloon do tray (só tu vês, some sozinha)
    if tray_icon_ref:
        tray_icon_ref.notify(
            f"Monitorização {'ATIVA' if ativo else 'PAUSADA'}",
            NOME_FALSO
        )

def iniciar_hotkey():
    keyboard.add_hotkey(HOTKEY_SECRETO, on_hotkey)
    keyboard.wait()   # bloqueia esta thread para manter o listener vivo

# ─────────────────────────────────────────────
# SYSTEM TRAY  (disfarçado)
# ─────────────────────────────────────────────

def criar_icone():
    """Ícone cinzento genérico — parece um serviço do sistema."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # círculo cinzento com um 'i' branco — parece informação/sistema
    draw.ellipse([4, 4, 60, 60], fill=(100, 100, 110))
    draw.ellipse([28, 14, 36, 22], fill="white")   # ponto do 'i'
    draw.rectangle([28, 26, 36, 50], fill="white") # haste do 'i'
    return img

def adicionar_startup(icon=None, item_=None):
    try:
        script_path = os.path.abspath(__file__)
        pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        # registo com nome falso para não chamar atenção
        winreg.SetValueEx(key, NOME_FALSO, 0, winreg.REG_SZ, f'"{pythonw}" "{script_path}"')
        winreg.CloseKey(key)
        print("Adicionado ao startup.")
    except Exception as e:
        print(f"Erro startup: {e}")

def remover_startup(icon=None, item_=None):
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, NOME_FALSO)
        winreg.CloseKey(key)
        print("Removido do startup.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erro: {e}")

def sair(icon, item_):
    icon.stop()
    os._exit(0)

def iniciar_tray():
    global tray_icon_ref
    icone = criar_icone()
    # menu minimalista — nada que grite "desativar prank"
    menu = pystray.Menu(
        item("Check for updates", adicionar_startup),   # → na verdade adiciona ao startup
        item("Preferences",       remover_startup),     # → na verdade remove do startup
        pystray.Menu.SEPARATOR,
        item("Exit",              sair),
    )
    tray_icon_ref = pystray.Icon(NOME_FALSO, icone, NOME_FALSO, menu)
    tray_icon_ref.run_detached()

# ─────────────────────────────────────────────
# LOOP DE MONITORIZAÇÃO
# ─────────────────────────────────────────────

def loop_monitorizacao():
    timer = 0
    print(f"Anjo V14 Windows iniciado.")
    print(f"Hotkey secreto: {HOTKEY_SECRETO}  →  ativa/pausa")
    print(f"Gatilho após {LIMITE_SEGUNDOS}s no YouTube em foco.\n")

    while True:
        try:
            if ativo:
                em_foco = youtube_em_foco()
                if em_foco:
                    timer += 3
                    print(f"YouTube em foco... {timer}/{LIMITE_SEGUNDOS}s")
                else:
                    if timer > 0:
                        print("Fora do YouTube. Timer resetado.")
                    timer = 0

                if timer >= LIMITE_SEGUNDOS:
                    ciclo_prank()
                    timer = 0
        except Exception as e:
            print(f"Erro ignorado: {e}")

        time.sleep(3)


if __name__ == "__main__":
    iniciar_tray()
    threading.Thread(target=iniciar_hotkey, daemon=True).start()
    loop_monitorizacao()
