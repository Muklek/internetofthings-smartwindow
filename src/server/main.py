import os

if __name__ == "__main__":
    os.system('sudo ~/.local/bin/uvicorn server:app --host 0.0.0.0 --port 80')
