import socket

# Definição dos produtos (código, nome e preço )
produtos = [
    {'codigo': 1,    'nome': 'Geladeira',        'preco': 2000.0},
    {'codigo': 2,    'nome': 'Micro ondas',      'preco': 500.0},
    {'codigo': 3,    'nome': 'Air Fryer',        'preco': 300.0},
    {'codigo': 4,    'nome': 'Fogão 4 B.',       'preco': 700.0},
    {'codigo': 5,    'nome': 'Misteira',         'preco': 80.0}
]

# Testa se o código informado faz parte da lista de produtos.
def testa_codigo(codigo):
    for p in produtos:
            if p['codigo'] == codigo:
                return True
    return False         

# Remove da lista o produto que foi comprado.
def remover_produto(codigo):
    global produtos  
    produtos = [p for p in produtos if p['codigo'] != codigo]

# Função onde ocorre a interação entre servidor e cliente.
def handle_client(client_socket):
    try:
        # Envia a lista de produtos para o cliente.
        produto_list = "\n".join([f"{p['codigo']}: {p['nome']}\t-\tR${p['preco']:.2f}" for p in produtos])
        client_socket.sendall(produto_list.encode('utf-8'))
        while True:
            # Receber código do produto escolhido
            codigo_produto = client_socket.recv(1024).decode('utf-8')
            
            if codigo_produto == "Sair": # Finalizar o processamento.
                break
            elif codigo_produto == "Lista": # Reenviar a lista para o cliente.
                produto_list = "\n".join([f"{p['codigo']}: {p['nome']}\t-\tR${p['preco']:.2f}" for p in produtos])
                client_socket.sendall(produto_list.encode('utf-8'))
                continue
            
            codigo_produto = int(codigo_produto)
            
            existe = testa_codigo(codigo_produto) 
            if existe: # Código existe na lista == Válido.
                resposta = "Válido"
                client_socket.sendall(resposta.encode('utf-8'))
            else:
                resposta = "Produto não encontrado! Insira um código válido." # Produto não existe na lista. Solicita um novo código.
                client_socket.sendall(resposta.encode('utf-8'))
                continue

            # Recebe a oferta do cliente
            oferta = client_socket.recv(1024).decode('utf-8')

            oferta = float (oferta)

            for p in produtos: # Seleciona o produto referente ao código digitado
                if p['codigo'] == codigo_produto:
                    produto = p

            # Negociação de preço
            if oferta >= produto['preco'] * 0.9:  # Aceita oferta se estiver dentro de 10% do preço inicial
                resposta = "Oferta aceita! Compra realizada no valor de: "
                resposta += str (oferta)
                client_socket.sendall(resposta.encode('utf-8')) # Manda a resposta que o item foi comprado.
                remover_produto(codigo_produto) # Deleta o item da lista.
                continue
            else:
                resposta = "Oferta rejeitada. Você terá 3 tentativas para realizar a compra.\nFaça uma nova oferta."
                Sugestao = produto['preco'] - (produto['preco'] * 0.03)
                resposta += "\nValor sugerido: "
                resposta += str (Sugestao)
                client_socket.sendall(resposta.encode('utf-8')) # Envia a resposta dizendo que a oferta foi rejeitada e sugerindo um novo valor.    
                          
                for i in range(3): # Limite de tentativas para a negociação.
                    oferta = client_socket.recv(1024).decode('utf-8')
                    oferta = float(oferta)
                    
                    if oferta >= produto['preco'] * 0.9: # Aceita ofertas se estiver dentro de 10% do preço inicial (As sugestões não passam de 10%).
                        resposta = "Oferta aceita! Compra realizada no valor de: "
                        resposta += str (oferta)
                        client_socket.sendall(resposta.encode('utf-8')) # Manda a resposta que o item foi comprado.
                        remover_produto(codigo_produto) # Remove o produto da lista.
                        break
                    else:
                        if i == 2:
                            continue
                        resposta = "Oferta ainda rejeitada. Tente novamente."
                        Sugestao = produto['preco'] - (produto['preco'] * 0.03 * (i+2))
                        resposta += "\nValor sugerido: "
                        resposta += str (Sugestao)
                        client_socket.sendall(resposta.encode('utf-8')) # Envia a resposta dizendo que a oferta foi recusada e sugere um novo valor.

                else:
                    resposta = "Negociação falhou. Limite de tentativas alcançado." # Envia a resposta dizendo que a negociação falhou.
                    client_socket.sendall(resposta.encode('utf-8'))
    
    finally:
        client_socket.close() # Fecha a conexão
        return 0 # Sinaliza que a conexão foi finalizada.

# Função para iniciar o servidor.
def start_server():
    serverPort = 12000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', serverPort))
    server_socket.listen(1)
    conexao = 1 
    print("Servidor iniciado e aguardando conexões...")

    while conexao == 1: # Mantém a conexão até o cliente escolher sair.
        client_socket, addr = server_socket.accept()
        print(f"Cliente conectado de {addr}")
        conexao = handle_client(client_socket,)

# Iniciando o processamento do servidor.
start_server()
