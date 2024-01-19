import subprocess
import openai

from config import OpenAI_API_Key

# Command to be executed
command = "uvicorn bot:app --reload"


if __name__ == '__main__':
    # Execute the command
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print("Stopping the app by user request...")
        exit(0)