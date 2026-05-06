import serial
import subprocess
import os
import sys

# --- CONFIGURAÇÕES ---
# No Raspberry Pi 5, geralmente é /dev/ttyUSB0 ou /dev/ttyACM0
PORTA_SERIAL = '/dev/ttyACM0' 
BAUD_RATE = 115200

# Caminhos Absolutos (Substitua 'usuario' pelo seu nome de usuário no Pi)
USER_HOME = os.path.expanduser("~")
PASTA_ROBO = os.path.join(USER_HOME, "Documents/New-Omega-Robot")
PYTHON_VENV = os.path.join(PASTA_ROBO, "venv/bin/python")
SCRIPT_BOT = os.path.join(PASTA_ROBO, "professor_bot.py")

def executar_bot():
    print(f"Executando: {PYTHON_VENV} {SCRIPT_BOT}")
    try:
        # Usamos Popen para que o bot rode em paralelo e não trave o listener
        subprocess.Popen([PYTHON_VENV, SCRIPT_BOT], cwd=PASTA_ROBO)
    except Exception as e:
        print(f"Erro ao disparar o bot: {e}")

def main():
    print(f"Iniciando Listener na porta {PORTA_SERIAL}...")
    
    try:
        # Inicializa a conexão serial
        ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
        ser.flush() # Limpa o buffer
        
        while True:
            if ser.in_waiting > 0:
                linha = ser.readline().decode('utf-8').strip()
                
                if linha == "START_ROBOT_BOT":
                    print("Sinal recebido do ESP-32!")
                    executar_bot()
                    
    except serial.SerialException as e:
        print(f"Erro de conexão serial: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nEncerrando...")

if __name__ == "__main__":
    main()
