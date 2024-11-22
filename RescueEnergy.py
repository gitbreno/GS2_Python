import cx_Oracle

# Configuração de conexão com o Oracle
USERNAME = 'rm557509'
PASSWORD = '280905'
DSN = cx_Oracle.makedsn('oracle.fiap.com.br', 1521, service_name='orcl')

try:
    connection = cx_Oracle.connect(USERNAME, PASSWORD, DSN)
    print("Conexão bem-sucedida com o Oracle Database")
except cx_Oracle.Error as e:
    print("Erro ao conectar no Oracle Database", e)
    exit()

def criar_cliente():
    nome = input("Digite o nome do cliente: ")
    endereco = input("Digite o endereço do cliente: ")
    telefone = input("Digite o telefone do cliente: ")

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO CLIENTES (ID, NOME, ENDERECO, TELEFONE) VALUES (SEQ_CLIENTES.NEXTVAL, :nome, :endereco, :telefone)",
                       nome=nome, endereco=endereco, telefone=telefone)
        connection.commit()
        print("Cliente cadastrado com sucesso!")
    except cx_Oracle.Error as e:
        print("Erro ao cadastrar o cliente", e)

def ler_clientes():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTES")
        clientes = cursor.fetchall()
        for cliente in clientes:
            print(cliente)
    except cx_Oracle.Error as e:
        print("Erro ao buscar os clientes", e)

def atualizar_cliente():
    cliente_id = int(input("Digite o ID do cliente que deseja atualizar: "))
    novo_nome = input("Digite o novo nome do cliente: ")
    novo_endereco = input("Digite o novo endereço do cliente: ")
    novo_telefone = input("Digite o novo telefone do cliente: ")

    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE CLIENTES SET NOME = :nome, ENDERECO = :endereco, TELEFONE = :telefone WHERE ID = :id",
                       nome=novo_nome, endereco=novo_endereco, telefone=novo_telefone, id=cliente_id)
        connection.commit()
        print("Cliente atualizado com sucesso!")
    except cx_Oracle.Error as e:
        print("Erro ao atualizar o cliente", e)

def deletar_cliente():
    cliente_id = int(input("Digite o ID do cliente que deseja deletar: "))

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM CLIENTES WHERE ID = :id", id=cliente_id)
        connection.commit()
        print("Cliente deletado com sucesso!")
    except cx_Oracle.Error as e:
        print("Erro ao deletar o cliente", e)

def menu():
    while True:
        print("\n=== MENU DE CLIENTES ===")
        print("1. Criar cliente")
        print("2. Ler clientes")
        print("3. Atualizar cliente")
        print("4. Deletar cliente")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_cliente()
        elif opcao == '2':
            ler_clientes()
        elif opcao == '3':
            atualizar_cliente()
        elif opcao == '4':
            deletar_cliente()
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    menu()
    connection.close()