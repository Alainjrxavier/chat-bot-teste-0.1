import gradio as gr
from openai import OpenAI

# Configuração do cliente OpenAI
client = OpenAI(api_key="A")  # Substitua pela sua chave da OpenAI

# Função para processar a entrada do usuário e retornar a resposta
def CustomChatGPT(user_input):
    # Mensagens iniciais para cada interação (evita acúmulo de mensagens)
    messages = [
        {"role": "system", "content": "Você é um chabot de uma empresa de TI, especializado em atender as ordens de serviços dos clientes, se limite á isso."},
        {"role": "user", "content": user_input}
    ]
    
    # Faz a chamada para a OpenAI para obter a resposta
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    # Acessa a resposta corretamente
    reply = response.choices[0].message.content
    
    return reply

# Criação da interface do Gradio
iface = gr.Interface(
    fn=CustomChatGPT,  # Função que será chamada quando o usuário enviar uma mensagem
    inputs=gr.Textbox(placeholder="Digite sua pergunta...", label="Sua mensagem"),  # Caixa de texto para entrada do usuário
    outputs=gr.Textbox(label="Resposta do chatbot"),  # Caixa de texto para mostrar a resposta
    title="versão 1.0 do chatbot de ordem de serviço de ti by alain",  # Título da interface
    description="Você é um chabot de uma empresa de TI, especializado em atender as ordens de serviços dos clientes, se limite á isso.",  # Descrição do chatbot
)

# Lança o site de chatbot
iface.launch(share=True)  # Adiciona share=True para permitir link público
