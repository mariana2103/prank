import os
import time
import subprocess
import threading

# ╔══════════════════════════════════════════════╗
# ║         ANJO V14 - MAC EDITION 💀            ║
# ╚══════════════════════════════════════════════╝

LINK_VOVO  = "https://www.youtube.com/watch?v=bDCBj15vKTE"
LINK_RELAX = "https://www.youtube.com/watch?v=92xTPH7OtLs"
LINK_FOCO  = "https://www.youtube.com/watch?v=Xdn0-lnDecw"

LIMITE_SEGUNDOS  = 10   # segundos no YouTube antes de disparar
VIDEO_DURACAO    = 15   # segundos que ele tem de ver cada vídeo
NAVEGADOR        = "Google Chrome"

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def popup(mensagem, titulo):
    try:
        subprocess.run([
            "osascript", "-e",
            f'display dialog "{mensagem}" with title "{titulo}" '
            f'buttons {{"OK"}} default button "OK" with icon stop'
        ], capture_output=True)
    except Exception:
        pass

def fechar_tabs_youtube():
    try:
        subprocess.run(["osascript", "-e", f'''
tell application "{NAVEGADOR}"
    try
        repeat with w in windows
            set tabsToClose to {{}}
            repeat with t in tabs of w
                try
                    if URL of t contains "youtube.com" then
                        set end of tabsToClose to t
                    end if
                end try
            end repeat
            repeat with t in tabsToClose
                try
                    close t
                end try
            end repeat
        end repeat
    end try
end tell
'''], capture_output=True)
    except Exception:
        pass

def abrir_video(link):
    try:
        subprocess.run(["osascript", "-e", f'''
tell application "Google Chrome"
    make new window
    set URL of active tab of front window to "{link}"
    activate
end tell
'''], capture_output=True)
        time.sleep(4)
    except Exception as e:
        print(f"Erro ao abrir vídeo: {e}")

def youtube_esta_aberto():
    try:
        result = subprocess.run(["osascript", "-e", f'''
tell application "{NAVEGADOR}"
    try
        repeat with w in windows
            repeat with t in tabs of w
                if URL of t contains "youtube.com" then
                    return "sim"
                end if
            end repeat
        end repeat
    end try
    return "nao"
end tell
'''], capture_output=True, text=True)
        return "sim" in result.stdout
    except Exception:
        return False

def get_frontmost():
    try:
        result = subprocess.run(
            ["osascript", "-e",
             'tell application "System Events" to get name of first process whose frontmost is true'],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return ""

def youtube_em_foco():
    app = get_frontmost()
    return NAVEGADOR in app and youtube_esta_aberto()

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

    # ══ BLOCO 1 → VIDEO VOVO ══════════════════
    fechar_tabs_youtube()
    popup("A TRABALHAR MUITO NÃO É ?",                                                                   "PRODUTIVIDADE ZERO")
    popup("PRODUTIVIDADE ZERO",                                                                          "PRODUTIVIDADE ZERO")
    popup("E depois ainda diz que trabalha? Sim confia",                                                 "PRODUTIVIDADE ZERO")
    reproduzir_video_com_vigilancia(
        LINK_VOVO,
        msg_fecho="Não estás a gostar do banger? Infelizmente vais ter de ouvir até ao fim. Upsi!",
    )
    print("Video 1 terminado.")

    # ══ BLOCO 2 → VIDEO RELAX ═════════════════
    fechar_tabs_youtube()
    popup("A tua namorada é um anjo na terra, linda e perfeita.",                                        "MENSAGEM DO ANJO")
    popup("Respira um pouco, relaxa, não me mates",                                                      "MENSAGEM DO ANJO")
    popup("Sabes que te amo muito certo? Reflete nisso enquanto respiras antes de vires falar comigo!", "MENSAGEM DO ANJO")
    reproduzir_video_com_vigilancia(
        LINK_RELAX,
        msg_fecho="Eu acho mesmo que tu queres relaxar! Essa tensão é provavelmente irritação não te fazem bem!",
    )
    print("Video 2 terminado.")

    # ══ BLOCO 3 → VIDEO FOCO ══════════════════
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
# LOOP DE MONITORIZAÇÃO
# ─────────────────────────────────────────────

timer = 0
print(f"Anjo V14 Mac iniciado — monitorizando '{NAVEGADOR}'...")
print(f"Gatilho apos {LIMITE_SEGUNDOS}s no YouTube em foco. Video: {VIDEO_DURACAO}s obrigatorios.\n")

while True:
    try:
        app_atual = get_frontmost()
        yt_aberto = youtube_esta_aberto()
        chrome_em_foco = NAVEGADOR in app_atual

        # so conta se o Chrome esta em foco E tem youtube aberto
        if chrome_em_foco and yt_aberto:
            timer += 3
            print(f"YouTube em foco... {timer}/{LIMITE_SEGUNDOS}s")
        else:
            if timer > 0:
                print("Fora do YouTube. Timer pausado e resetado.")
            timer = 0

        if timer >= LIMITE_SEGUNDOS:
            ciclo_prank()
            timer = 0

    except Exception as e:
        print(f"Erro ignorado: {e}")

    time.sleep(3)