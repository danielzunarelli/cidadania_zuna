import asyncio
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN não definido nas variáveis de ambiente.")

ARQUIVO_USUARIOS = "data/usuarios.json"
ARQUIVO_STATUS = "data/status_atual.json"

# ------------------------------
def carregar_usuarios():
    try:
        with open(ARQUIVO_USUARIOS, "r") as f:
            return json.load(f)
    except:
        return []

def salvar_usuarios(lista):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(lista, f)

def carregar_status_salvo():
    try:
        with open(ARQUIVO_STATUS, "r") as f:
            return json.load(f)
    except:
        return []

# ------------------------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    usuarios = carregar_usuarios()

    if chat_id not in usuarios:
        usuarios.append(chat_id)
        salvar_usuarios(usuarios)
        print(f"✅ Novo usuário registrado: {chat_id}")

    mensagem = (
        "👋 Olá! Seja bem-vindo ao bot da cidadania italiana da família Zunarelli 🇮🇹\n\n"
        "Envie /status para ver a situação atual do nosso processo."
    )
    await context.bot.send_message(chat_id=chat_id, text=mensagem)

# ------------------------------
async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = carregar_status_salvo()
    chat_id = update.effective_chat.id

    if status:
        mensagem = "📌 STATUS ATUAL DO PROCESSO:\n\n" + "\n".join(status)
    else:
        mensagem = "⚠️ Nenhum status salvo ainda. Tente mais tarde."

    await context.bot.send_message(chat_id=chat_id, text=mensagem)

# ------------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))

    print("🤖 Bot escutando... (/start e /status ativos)")
    asyncio.run(app.run_polling())