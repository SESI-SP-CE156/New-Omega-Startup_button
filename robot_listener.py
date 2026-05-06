import serial
import subprocess
import os
import sys
import time

# --- CONFIGURAÇÕES ---
PORTA_SERIAL = '/dev/ttyACM0' 
BAUD_RATE = 115200

# Caminhos Absolutos
USER_HOME = os.path.expanduser("~")
PASTA_ROBO = os.path.join(USER_HOME, "Documents/New-Omega-Robot")
PYTHON_VENV = os.path.join(PASTA_ROBO, "venv/bin/python")
SCRIPT_BOT = os.path.join(PASTA_ROBO, "professor_bot.py")

# Variável para rastrear o processo em execução
bot_process = None

def executar_bot():
    global bot_process
    
    # Verifica se o processo já existe e se ainda está rodando (poll() retorna None se estiver rodando)
    if bot_process is not None and bot_process.poll() is None:
        print("Aviso: O bot já está em execução! Ignorando comando de START.")
        return

    print(f"Executando: {PYTHON_VENV} {SCRIPT_BOT}")
    try:
        # Atribui a referência do subprocesso à variável global
        bot_process = subprocess.Popen([PYTHON_VENV, SCRIPT_BOT], cwd=PASTA_ROBO)
        print(f"Bot iniciado com PID: {bot_process.pid}")
    except Exception as e:
        print(f"Erro ao disparar o bot: {e}")

def parar_bot():
    global bot_process
    
    if bot_process is not None and bot_process.poll() is None:
        print(f"Encerrando o bot (PID: {bot_process.pid})...")
        try:
            # Envia o sinal SIGTERM para o processo
            bot_process.terminate()
            # Aguarda até 3 segundos para o processo fechar de forma limpa
            bot_process.wait(timeout=3)
            print("Bot encerrado com sucesso.")
        except subprocess.TimeoutExpired:
            print("O bot demorou a responder. Forçando o encerramento (SIGKILL)...")
            bot_process.kill() # Mata na força bruta se travar
        except Exception as e:
            print(f"Erro ao tentar encerrar o bot: {e}")
    else:
        print("Comando ignorado: Nenhum bot em execução no momento.")

def main():
    print(f"Iniciando Listener na porta {PORTA_SERIAL}...")
    
    try:
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
        ser.flush()
        
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if linha == "START_ROBOT_BOT":
                    print("--> Sinal de START recebido do ESP-32!")
                    executar_bot()
                
                elif linha == "STOP_ROBOT_BOT":
                    print("--> Sinal de STOP recebido do ESP-32!")
                    parar_bot()
                    
            time.sleep(0.05) # Pequeno delay para economizar processamento
                    
    except serial.SerialException as e:
        print(f"Erro de conexão serial: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nEncerrando listener...")
        parar_bot() # Garante que o bot também seja fechado se o listener cair

if __name__ == "__main__":
    main()