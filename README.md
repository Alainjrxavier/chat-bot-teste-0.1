Versão 1.0 do chatbot em python. O código foi feito no visual studio code.
PRÉ-REQUISITOS PARA O CÓDIGO FUNCIONAR:
1 - API DA OPENAI
2 - API DO BOTFATHER NO TELEGRAM
3 - UM BANCO DE DADOS .db feito em SQLITE (no código o arquivo consta com o nome empresa.db)
4 - DADOS PARA TREINAMENTO DO CHATBOT EM .jsonl (no código o arquivo consta com o nome meus_dados.jsonl)
* PREENCHER OS CAMINHOS CORRETOS PARA CADA ARQUIVO ONDE É PEDIDO NO CODIGO ( exemplo: r"E:\chatbot\meus_dados.jsonl")

Para executar o código, siga os seguintes passos:

1 - no terminal, executar o comando pip install python-telegram-bot
2 - no terminal, executar o comando pip install openai

*a API da openai é paga e deve ser gerada da seguinte forma:
1 - Crie uma conta e logue na OpenAI Platform: https://platform.openai.com
2 - Após logar, vá ao canto superior direito, no ícone perfil do usuário e selecione "Your profile"
3 - Nesta página, ao lado esquerdo, clique em "Billing"
4 - Insira suas informações e realize o pagamento em "add to credit balance", no mínimo 5 dólares.
5 - Na mesma página, ao lado esquerdo, clique em "API keys", ali será gerada a chave
6 - Clique em "Create new secret key", insira um nome e selecione um projeto, "Permissions all"
7 - A chave será gerada, então é só preencher na linha 10 do código, onde tem "client = OpenAI(api_key="
8 - Após execução do código, no terminal aparecerá o link do site que o Gradio gerou

Agora, é necessário um código de API para funcionar no telegram, que é grátis e bem simples de se fazer
1 - Cria uma conta no Telegram
2 - Procure pelo @BotFather no telegram
3 - Digite "/newbot"
4 - Ele vai perguntar o nome e o username do seu bot
5 - Após isso, ele vai gerar uma chave API para ser preenchida no código
6 - Use esta chave API na linha 13 do código, onde tem "TELEGRAM_TOKEN"


* Qualquer erro que possa ocorrer pode ser relacionado á API gerada, checar corretamente*
