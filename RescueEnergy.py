import cx_Oracle
import json

# Configuração de conexão com o Oracle
USERNAME = 'rm557509'
PASSWORD = '280905'
DSN = cx_Oracle.makedsn('oracle.fiap.com.br', 1521, service_name='orcl')

try:
    connection = cx_Oracle.connect(USERNAME, PASSWORD, DSN)
    print("Conexão bem-sucedida com o Oracle Database")
except cx_Oracle.Error as e:
    print("Erro ao conectar no Oracle Database:", e)
    exit()


def validar_entrada(entrada, tipo):
    if tipo == "string" and not entrada.strip():
        return False
    if tipo == "numero" and not entrada.isdigit():
        return False
    return True


def criar_cliente():
    nome = input("Digite o nome do cliente: ").strip()
    if not validar_entrada(nome, "string"):
        print("Erro: Nome inválido.")
        return

    endereco = input("Digite o endereço do cliente: ").strip()
    if not validar_entrada(endereco, "string"):
        print("Erro: Endereço inválido.")
        return

    telefone = input("Digite o telefone do cliente: ").strip()
    if not validar_entrada(telefone, "numero"):
        print("Erro: Telefone inválido. Deve conter apenas números.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO CLIENTES (ID, NOME, ENDERECO, TELEFONE) VALUES (SEQ_CLIENTES.NEXTVAL, :nome, :endereco, :telefone)",
            nome=nome, endereco=endereco, telefone=telefone
        )
        connection.commit()
        print("Cliente cadastrado com sucesso!")
    except cx_Oracle.Error as e:
        print("Erro ao cadastrar o cliente:", e)


def ler_clientes():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTES")
        clientes = cursor.fetchall()
        for cliente in clientes:
            print(cliente)
        return clientes
    except cx_Oracle.Error as e:
        print("Erro ao buscar os clientes:", e)
        return []


def buscar_cliente_por_nome():
    nome = input("Digite o nome do cliente para buscar: ").strip()
    if not validar_entrada(nome, "string"):
        print("Erro: Nome inválido.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTES WHERE NOME LIKE :nome", nome=f"%{nome}%")
        clientes = cursor.fetchall()
        for cliente in clientes:
            print(cliente)
        if not clientes:
            print("Nenhum cliente encontrado com esse nome.")
    except cx_Oracle.Error as e:
        print("Erro ao buscar clientes por nome:", e)


def atualizar_cliente():
    cliente_id = input("Digite o ID do cliente que deseja atualizar: ").strip()
    if not validar_entrada(cliente_id, "numero"):
        print("Erro: ID inválido.")
        return

    novo_nome = input("Digite o novo nome do cliente: ").strip()
    novo_endereco = input("Digite o novo endereço do cliente: ").strip()
    novo_telefone = input("Digite o novo telefone do cliente: ").strip()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE CLIENTES SET NOME = :nome, ENDERECO = :endereco, TELEFONE = :telefone WHERE ID = :id",
            nome=novo_nome, endereco=novo_endereco, telefone=novo_telefone, id=int(cliente_id)
        )
        connection.commit()
        print("Cliente atualizado com sucesso!")
    except cx_Oracle.Error as e:
        print("Erro ao atualizar o cliente:", e)


def deletar_cliente():
    cliente_id = input("Digite o ID do cliente que deseja deletar: ").strip()
    if not validar_entrada(cliente_id, "numero"):
        print("Erro: ID inválido.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM CLIENTES WHERE ID = :id", id=int(cliente_id))
        connection.commit()
        print("Cliente deletado com sucesso!")
    except cx_Oracle.Error as e:
        print("Erro ao deletar o cliente:", e)


def exportar_para_json():
    clientes = ler_clientes()
    if not clientes:
        print("Nenhum cliente para exportar.")
        return

    dados = [{"id": cliente[0], "nome": cliente[1], "endereco": cliente[2], "telefone": cliente[3]} for cliente in clientes]

    with open("clientes.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print("Clientes exportados para 'clientes.json' com sucesso!")


def menu():
    while True:
        print("\n=== MENU DE CLIENTES ===")
        print("1. Criar cliente")
        print("2. Ler clientes")
        print("3. Buscar cliente por nome")
        print("4. Atualizar cliente")
        print("5. Deletar cliente")
        print("6. Exportar clientes para JSON")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_cliente()
        elif opcao == '2':
            ler_clientes()
        elif opcao == '3':
            buscar_cliente_por_nome()
        elif opcao == '4':
            atualizar_cliente()
        elif opcao == '5':
            deletar_cliente()
        elif opcao == '6':
            exportar_para_json()
        elif opcao == '7':
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")


if __name__ == "__main__":
    menu()
    connection.close()
