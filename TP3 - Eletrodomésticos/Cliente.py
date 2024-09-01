import socket

# Testa se a oferta digitada pelo cliente é realmente um número.
def testa_Oferta(oferta, validade):
    while validade == False:
        try:
            oferta = float (oferta)
        except ValueError:
            print('Oferta inválida!')
            oferta = input("Digite uma oferta válida: ")
            continue
        oferta = str (oferta)
        return oferta

# Testa se o código digitado pelo cliente é realmente um número.
def testa_Codigo(codigo, validade): 
    if codigo == "Sair" or codigo == "Lista": # Caso seja alguma das palavras chaves a função já retorna antes da verificação.
        return codigo
    while validade == False:
        try:
            codigo = int (codigo)
        except ValueError:
            print('Código inválido!')
            codigo = input("Digite um código válido: ")
            continue
        codigo = str (codigo)
        return codigo

# Função onde ocorre a interação entre cliente e servidor.
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverName = 'localhost'
    serverPort = 12000
    client_socket.connect((serverName, serverPort))

    try:
        # Recebendo a lista de produtos do servidor e mostrando em tela
        produto_list = client_socket.recv(1024).decode('utf-8')
        print("Bem vindo ao Souza e Silva Eletrodomésticos!")
        print("Produtos disponíveis:") 
        print(produto_list)
        while True:
            # Cliente escolhe o produto
            codigo_produto = input("Digite o código do produto que deseja comprar, \"Lista\" para ver a lista novamente ou \"Sair\" para encerrar: ")
            
            codigo_produto = testa_Codigo(codigo_produto,False) # Validação.
                                
            client_socket.sendall(codigo_produto.encode('utf-8')) # Código enviada ao servidor.
            
            if codigo_produto == "Sair": # Forma de finalizar o processo.
                break
            
            resposta = client_socket.recv(1024).decode('utf-8') # Recebendo a resposta ao código enviado.
            
            if resposta.startswith("P") or resposta.endswith("0"): # Mostrando a resposta do servidor caso houver.
                print(resposta)
                print("")
                continue
            
            # Cliente faz a primeira oferta.
            oferta = input("Digite sua oferta: ")
            
            oferta = testa_Oferta(oferta, False) # Validação.
                 
            client_socket.sendall(oferta.encode('utf-8')) # Oferta enviada ao servidor.

            resposta = client_socket.recv(1024).decode('utf-8') # Recebendo a reposta do servidor.
            print("Resposta do servidor:", resposta) # Mostrando a resposta em tela.
            print("")
            
            if "Compra realizada" in resposta: # Caso tenha sido efetuada a compra o código volta ao início.
                continue

            # Se a oferta for rejeitada, o cliente tem 3 tentativas para conseguir comprar.
            for i in range(3):
                oferta = input("Nova oferta: ")
                oferta = testa_Oferta(oferta, False) # Testa a nova oferta.
                
                client_socket.sendall(oferta.encode('utf-8')) # Envia a nova oferta.

                resposta = client_socket.recv(1024).decode('utf-8') # Recebe a resposta a nova oferta.
                print("Resposta do servidor:", resposta) # Mostra em tela a resposta.
                print("")
                if "Compra realizada" in resposta: # Caso tenha realizado a compra é mostrado em tela e o código continua.
                    break
                elif "Negociação" in resposta: # Caso a negociação tenha sido encerrada sem comprar o produto é mostrado em tela e o código continua.
                    break

    finally:
        print('Volte sempre!')
        client_socket.close() # Fechando a conexão.

# Inicia o processamento do cliente.
start_client()
