"""
Script para testar a API de Perfumes
"""
import requests
import json

# URL base da API (ajuste conforme necessário)
BASE_URL = "http://localhost:8000/api/v1"

def test_health():
    """Testa o endpoint de health check"""
    response = requests.get("http://localhost:8000/health")
    print(f"Health Check: {response.status_code}")
    print(response.json())
    print("-" * 50)

def test_categorias():
    """Testa os endpoints de categorias"""
    print("Testando endpoints de categorias...")
    
    # Listar categorias
    response = requests.get(f"{BASE_URL}/categorias/")
    print(f"GET /categorias/: {response.status_code}")
    if response.status_code == 200:
        categorias = response.json()
        print(f"Número de categorias: {len(categorias)}")
        if categorias:
            categoria_id = categorias[0]["id"]
            
            # Obter categoria por ID
            response = requests.get(f"{BASE_URL}/categorias/{categoria_id}")
            print(f"GET /categorias/{categoria_id}: {response.status_code}")
            print(response.json())
    
    # Criar nova categoria
    nova_categoria = {
        "nome": "Categoria de Teste",
        "descricao": "Descrição da categoria de teste",
        "imagem_url": "/images/test.webp",
        "slug": "categoria-teste"
    }
    response = requests.post(f"{BASE_URL}/categorias/", json=nova_categoria)
    print(f"POST /categorias/: {response.status_code}")
    if response.status_code == 201:
        categoria_criada = response.json()
        categoria_id = categoria_criada["id"]
        print(f"Categoria criada: {categoria_criada}")
        
        # Atualizar categoria
        update_data = {
            "descricao": "Descrição atualizada"
        }
        response = requests.put(f"{BASE_URL}/categorias/{categoria_id}", json=update_data)
        print(f"PUT /categorias/{categoria_id}: {response.status_code}")
        if response.status_code == 200:
            print(response.json())
        
        # Excluir categoria
        response = requests.delete(f"{BASE_URL}/categorias/{categoria_id}")
        print(f"DELETE /categorias/{categoria_id}: {response.status_code}")
    
    print("-" * 50)

def test_produtos():
    """Testa os endpoints de produtos"""
    print("Testando endpoints de produtos...")
    
    # Listar produtos
    response = requests.get(f"{BASE_URL}/produtos/")
    print(f"GET /produtos/: {response.status_code}")
    if response.status_code == 200:
        produtos = response.json()
        print(f"Número de produtos: {len(produtos)}")
        if produtos:
            produto_id = produtos[0]["id"]
            categoria_id = produtos[0]["categoria_id"]
            
            # Obter produto por ID
            response = requests.get(f"{BASE_URL}/produtos/{produto_id}")
            print(f"GET /produtos/{produto_id}: {response.status_code}")
            print(response.json())
            
            # Obter produtos por categoria
            response = requests.get(f"{BASE_URL}/produtos/categoria/{categoria_id}")
            print(f"GET /produtos/categoria/{categoria_id}: {response.status_code}")
            print(f"Produtos na categoria {categoria_id}: {len(response.json())}")
    
    # Listar produtos em destaque
    response = requests.get(f"{BASE_URL}/produtos/destaques")
    print(f"GET /produtos/destaques: {response.status_code}")
    if response.status_code == 200:
        destaques = response.json()
        print(f"Número de produtos em destaque: {len(destaques)}")
    
    # Criar novo produto (precisa de uma categoria existente)
    response = requests.get(f"{BASE_URL}/categorias/")
    if response.status_code == 200 and response.json():
        categoria_id = response.json()[0]["id"]
        
        novo_produto = {
            "nome": "Produto de Teste",
            "descricao": "Descrição do produto de teste",
            "preco": 99.90,
            "imagem_url": "/images/test_product.webp",
            "categoria_id": categoria_id,
            "destaque": True,
            "estoque": 10
        }
        response = requests.post(f"{BASE_URL}/produtos/", json=novo_produto)
        print(f"POST /produtos/: {response.status_code}")
        if response.status_code == 201:
            produto_criado = response.json()
            produto_id = produto_criado["id"]
            print(f"Produto criado: {produto_criado}")
            
            # Atualizar produto
            update_data = {
                "preco": 89.90,
                "estoque": 15
            }
            response = requests.put(f"{BASE_URL}/produtos/{produto_id}", json=update_data)
            print(f"PUT /produtos/{produto_id}: {response.status_code}")
            if response.status_code == 200:
                print(response.json())
            
            # Excluir produto
            response = requests.delete(f"{BASE_URL}/produtos/{produto_id}")
            print(f"DELETE /produtos/{produto_id}: {response.status_code}")
    
    print("-" * 50)

def test_quiz():
    """Testa os endpoints do quiz"""
    print("Testando endpoints do quiz...")
    
    # Listar perguntas
    response = requests.get(f"{BASE_URL}/quiz/perguntas/")
    print(f"GET /quiz/perguntas/: {response.status_code}")
    if response.status_code == 200:
        perguntas = response.json()
        print(f"Número de perguntas: {len(perguntas)}")
        
        if perguntas:
            pergunta_id = perguntas[0]["id"]
            
            # Obter pergunta por ID
            response = requests.get(f"{BASE_URL}/quiz/perguntas/{pergunta_id}")
            print(f"GET /quiz/perguntas/{pergunta_id}: {response.status_code}")
            print(response.json())
            
            # Obter opções da pergunta
            response = requests.get(f"{BASE_URL}/quiz/opcoes/pergunta/{pergunta_id}")
            print(f"GET /quiz/opcoes/pergunta/{pergunta_id}: {response.status_code}")
            if response.status_code == 200:
                opcoes = response.json()
                print(f"Número de opções: {len(opcoes)}")
    
    # Listar resultados
    response = requests.get(f"{BASE_URL}/quiz/resultados/")
    print(f"GET /quiz/resultados/: {response.status_code}")
    if response.status_code == 200:
        resultados = response.json()
        print(f"Número de resultados: {len(resultados)}")
    
    # Testar processamento do quiz
    # Simular respostas do usuário
    respostas = {
        "4": "floral",
        "2": "suave"
    }
    response = requests.post(f"{BASE_URL}/quiz/processar", json=respostas)
    print(f"POST /quiz/processar: {response.status_code}")
    if response.status_code == 200:
        print(f"Resultado do quiz: {response.json()}")
    
    print("-" * 50)

def test_contatos():
    """Testa os endpoints de contatos"""
    print("Testando endpoints de contatos...")
    
    # Criar novo contato
    novo_contato = {
        "nome": "Usuário Teste",
        "email": "teste@exemplo.com",
        "telefone": "(11) 99999-9999",
        "assunto": "Teste da API",
        "mensagem": "Esta é uma mensagem de teste para verificar o funcionamento da API."
    }
    response = requests.post(f"{BASE_URL}/contatos/", json=novo_contato)
    print(f"POST /contatos/: {response.status_code}")
    if response.status_code == 201:
        contato_criado = response.json()
        contato_id = contato_criado["id"]
        print(f"Contato criado: {contato_criado}")
        
        # Listar contatos
        response = requests.get(f"{BASE_URL}/contatos/")
        print(f"GET /contatos/: {response.status_code}")
        if response.status_code == 200:
            contatos = response.json()
            print(f"Número de contatos: {len(contatos)}")
        
        # Obter contato por ID
        response = requests.get(f"{BASE_URL}/contatos/{contato_id}")
        print(f"GET /contatos/{contato_id}: {response.status_code}")
        print(response.json())
        
        # Marcar contato como respondido
        response = requests.put(f"{BASE_URL}/contatos/{contato_id}/marcar-respondido")
        print(f"PUT /contatos/{contato_id}/marcar-respondido: {response.status_code}")
        if response.status_code == 200:
            print(response.json())
        
        # Listar contatos não respondidos
        response = requests.get(f"{BASE_URL}/contatos/nao-respondidos")
        print(f"GET /contatos/nao-respondidos: {response.status_code}")
        if response.status_code == 200:
            nao_respondidos = response.json()
            print(f"Número de contatos não respondidos: {len(nao_respondidos)}")
    
    print("-" * 50)

def test_usuarios():
    """Testa os endpoints de usuários"""
    print("Testando endpoints de usuários...")
    
    # Criar novo usuário
    novo_usuario = {
        "nome": "Usuário Teste",
        "email": "usuario.teste@exemplo.com",
        "senha": "senha123",
        "ativo": True
    }
    response = requests.post(f"{BASE_URL}/usuarios/", json=novo_usuario)
    print(f"POST /usuarios/: {response.status_code}")
    if response.status_code == 201:
        usuario_criado = response.json()
        print(f"Usuário criado: {usuario_criado}")
        
        # Obter token de acesso
        login_data = {
            "username": "usuario.teste@exemplo.com",
            "password": "senha123"
        }
        response = requests.post(f"{BASE_URL}/usuarios/token", data=login_data)
        print(f"POST /usuarios/token: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print(f"Token obtido: {token}")
            
            # Configurar headers com token
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # Obter informações do usuário atual
            response = requests.get(f"{BASE_URL}/usuarios/me", headers=headers)
            print(f"GET /usuarios/me: {response.status_code}")
            if response.status_code == 200:
                print(response.json())
            
            # Listar usuários
            response = requests.get(f"{BASE_URL}/usuarios/", headers=headers)
            print(f"GET /usuarios/: {response.status_code}")
            if response.status_code == 200:
                usuarios = response.json()
                print(f"Número de usuários: {len(usuarios)}")
    
    print("-" * 50)

def main():
    """Função principal para executar todos os testes"""
    print("Iniciando testes da API de Perfumes...")
    print("=" * 50)
    
    try:
        # Inicializar banco de dados
        response = requests.post("http://localhost:8000/init-db")
        print(f"Inicialização do banco de dados: {response.status_code}")
        print(response.json())
        print("=" * 50)
        
        # Executar testes
        test_health()
        test_categorias()
        test_produtos()
        test_quiz()
        test_contatos()
        test_usuarios()
        
        print("Testes concluídos com sucesso!")
    except requests.exceptions.ConnectionError:
        print("Erro de conexão. Verifique se a API está em execução.")
    except Exception as e:
        print(f"Erro durante os testes: {str(e)}")

if __name__ == "__main__":
    main()
