import mysql.connector
import re
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Carregar as variáveis de ambiente do arquivo .env
env_path = r"C:\Users\User\OneDrive\Documentos\apis.env"
load_dotenv(dotenv_path=env_path)

# Configuração do cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Token do bot do Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configuração do banco de dados MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "Alain",
    "password": "Alain123@@",
    "database": "chatbot_db"
}

# Função para conectar ao banco de dados
def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Função para criar a tabela (caso não exista)
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cliente (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        telefone VARCHAR(20) NOT NULL,
        equipamento VARCHAR(255) NOT NULL,
        modelo_equipamento VARCHAR(255) NOT NULL,
        problema_apresentado VARCHAR(1000) NOT NULL,
        UNIQUE (nome(100), telefone, equipamento(100), modelo_equipamento(100))

    )
    """)
    conn.commit()
    conn.close()

# Caminho do arquivo de treinamento
training_data_path = r"C:\Users\User\OneDrive\Documentos\meus_dados.jsonl"

# Função para carregar os dados do arquivo JSONL
def load_training_data():
    if not os.path.exists(training_data_path):
        return []
    with open(training_data_path, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
            return data.get("messages", [])
        except json.JSONDecodeError:
            return []

# Carregar os dados para o chatbot
training_messages = load_training_data()

# Função para validar telefone
def is_valid_phone(telefone):
    return bool(re.fullmatch(r"\d+", telefone))

# Função para verificar se os dados já existem na tabela 'Cliente'
def is_duplicate_entry(nome, telefone, equipamento, modelo_equipamento, problema_apresentado):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*) FROM Cliente WHERE nome = %s AND telefone = %s 
    AND equipamento = %s AND modelo_equipamento = %s AND problema_apresentado = %s
    """, (nome, telefone, equipamento, modelo_equipamento, problema_apresentado))
    
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# Função para inserir dados na tabela 'Cliente'
def insert_client_data(nome, telefone, equipamento, modelo_equipamento, problema_apresentado):
    if not is_valid_phone(telefone):
        return "Erro: O telefone deve conter apenas números."
    
    if is_duplicate_entry(nome, telefone, equipamento, modelo_equipamento, problema_apresentado):
        return "Erro: Este atendimento já foi registrado anteriormente."
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO Cliente (nome, telefone, equipamento, modelo_equipamento, problema_apresentado)
    VALUES (%s, %s, %s, %s, %s)
    """, (nome, telefone, equipamento, modelo_equipamento, problema_apresentado))
    
    conn.commit()
    conn.close()
    return "Atendimento registrado com sucesso. Nosso suporte entrará em contato para finalizar seu atendimento!"

# Função para processar perguntas gerais sobre TI
def CustomChatGPT(user_input):
    messages = training_messages + [{"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

# Função para lidar com mensagens no Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()
    state = context.user_data.get('state', None)

    if state is None:
        if user_text == "1":
            context.user_data['state'] = 'nome'
            await update.message.reply_text("Ótimo! Vamos começar seu atendimento.\nQual é o seu nome?")
        else:
            bot_reply = CustomChatGPT(update.message.text)
            await update.message.reply_text(bot_reply)
    
    elif state == 'nome':
        context.user_data['nome'] = update.message.text
        await update.message.reply_text("Qual é o seu telefone? (Apenas números)")
        context.user_data['state'] = 'telefone'
    
    elif state == 'telefone':
        telefone = update.message.text.strip()
        if not is_valid_phone(telefone):
            await update.message.reply_text("Erro: O telefone deve conter apenas números. Digite novamente.")
            return
        context.user_data['telefone'] = telefone
        await update.message.reply_text("Qual equipamento você está utilizando?")
        context.user_data['state'] = 'equipamento'
    
    elif state == 'equipamento':
        context.user_data['equipamento'] = update.message.text
        await update.message.reply_text("Qual o modelo do seu equipamento?")
        context.user_data['state'] = 'modelo_equipamento'
    
    elif state == 'modelo_equipamento':
        context.user_data['modelo_equipamento'] = update.message.text
        await update.message.reply_text("Qual é o problema apresentado?")
        context.user_data['state'] = 'problema_apresentado'
    
    elif state == 'problema_apresentado':
        context.user_data['problema_apresentado'] = update.message.text
        result = insert_client_data(
            context.user_data['nome'],
            context.user_data['telefone'],
            context.user_data['equipamento'],
            context.user_data['modelo_equipamento'],
            context.user_data['problema_apresentado']
        )
        await update.message.reply_text(result)
        if "Atendimento registrado com sucesso" in result:
            await update.message.reply_text("Agora o chatbot voltará a responder perguntas gerais sobre TI.")
            context.user_data.clear()

# Configuração do bot do Telegram
def start_telegram_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot do Telegram iniciado...")
    app.run_polling()

if __name__ == "__main__":
    create_table()
    start_telegram_bot()
