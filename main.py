import os
import subprocess
from multiprocessing import Pool

import time
from telegram import Update
from telegram.ext import Application,ApplicationBuilder, CommandHandler, ContextTypes,CallbackContext
async def ping_server(update: Update, context: CallbackContext):

    await update.message.reply_text(f"Continuo rodando")
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Olá! Envie o comando /contar_arquivos seguido do caminho da pasta para contar os arquivos.")

# Lista os arquivos de uma pasta
async def list_files(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    folder_path = "./output"  # Substitua pelo caminho da pasta que deseja listar
    try:
        files = subprocess.run(["ls", folder_path], stdout=subprocess.PIPE, text=True)
        
        await update.message.reply_text(f"Arquivos em {folder_path} ({len(problemas)}):\n\n{files.stdout}")
    except FileNotFoundError:
        await update.message.reply_text(f"Pasta {folder_path} não encontrada.")

# Função para enviar notificação periódica





async def help_list(update: Update,contex:CallbackContext):
    await update.message.reply_text("""
ping - verificar o servidor se ele esta online
list - listar a pasta output
help - lista de comandos 
count - contar quantidade de arquivos na output
                                    """)


async def contar_arquivos(update: Update, context: CallbackContext):
    # Obtém o caminho da pasta do comando enviado pelo usuário
    folder_path = "./output"

    # Verifica se o caminho da pasta é válido
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # Lista os arquivos na pasta e conta-os
        files = os.listdir(folder_path)
        num_files = len(files)
        await update.message.reply_text(f"A pasta '{folder_path}' contém {num_files} arquivo(s), o total é {len(problemas)}")
    else:
        await update.message.reply_text("O caminho da pasta é inválido.")
def output_file_exists(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    output_filename = f"output/output_{filename}.txt"
    return os.path.exists(output_filename)

def execute_cpp(filepath):
    print(f"{filepath}")
    filename = os.path.splitext(os.path.basename(filepath))[0]
    if output_file_exists(filepath):
        print(f"Output file already exists for {filename}")
        return
    cmd = ["./build/mip-solve", filepath, "--verbose"]

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output

    output_filename = f"output/output_{filename}.txt"

    print(f"End process, writing file for {filename}")
    with open(output_filename, "w") as output_file:
        output_file.write(output)

    
if __name__ == "__main__":
    # subprocess.run(start_bot,stdout=subprocess.PIPE,)
    bot_token = "6698519042:AAGq-CFtKic24bIiepUd8emCLgbXlAMQ84I"  # Substitua pelo token do seu bot
    app = ApplicationBuilder().token(bot_token).build()

    # app.add_handler(CommandHandler("hello", hello))

    # app.run_polling()
  # Handlers para comandos
    app.add_handler(CommandHandler("ping", ping_server))
    app.add_handler(CommandHandler("list", list_files))
    app.add_handler(CommandHandler(["start","help"],help_list))
    app.add_handler(CommandHandler("count",contar_arquivos))

  



    PASTA_BASE = "./collection_2/"
    PASTA_BASE = "./mipdownloader/miplib2017-selected" # Comentar para debug
    global problemas
    problemas = os.listdir(PASTA_BASE)
    N = 10
    pool = Pool(processes=N)

    ignored_files = set()
    IGNORED_DIR = "ignore"

    for root, _, files in os.walk(IGNORED_DIR):
        for file in files:
            with open(os.path.join(root, file), "r") as ignore_file:
                ignored_files.update(ignore_file.read().splitlines())

    # Verifica se a pasta "output" existe, senão cria
    output_folder = "./output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)













    for problema in problemas:
        pasta_problema = os.path.join(PASTA_BASE, problema, "instances")
        pasta_problema = PASTA_BASE # comentar para debug
        arquivos = os.listdir(pasta_problema)
        files_to_process = []

        for arquivo in arquivos:
            if os.path.splitext(arquivo)[0] not in ignored_files:
                files_to_process.append(os.path.join(pasta_problema, arquivo))

        for file_to_process in files_to_process:
            pool.apply_async(execute_cpp, (file_to_process,))

    pool.close()
    # pool.join()

    app.run_polling()



    