from flask import Flask, request, jsonify
import cx_Oracle

# Configuração de conexão com o Oracle
USERNAME = 'rm557509'
PASSWORD = '280905'
DSN = cx_Oracle.makedsn('oracle.fiap.com.br', 1521, service_name='orcl')

app = Flask(__name__)

# Conectar ao banco
try:
    connection = cx_Oracle.connect(USERNAME, PASSWORD, DSN)
    print("Conexão bem-sucedida com o Oracle Database")
except cx_Oracle.Error as e:
    print("Erro ao conectar no Oracle Database", e)
    exit()

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.json
    nome = data.get('nome')
    endereco = data.get('endereco')
    telefone = data.get('telefone')

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO CLIENTES (ID, NOME, ENDERECO, TELEFONE) VALUES (SEQ_CLIENTES.NEXTVAL, :nome, :endereco, :telefone)",
            nome=nome, endereco=endereco, telefone=telefone
        )
        connection.commit()
        return jsonify({"message": "Cliente cadastrado com sucesso!"}), 201
    except cx_Oracle.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clientes', methods=['GET'])
def ler_clientes():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CLIENTES")
        clientes = cursor.fetchall()
        clientes_formatados = [{"id": c[0], "nome": c[1], "endereco": c[2], "telefone": c[3]} for c in clientes]
        return jsonify(clientes_formatados), 200
    except cx_Oracle.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    data = request.json
    nome = data.get('nome')
    endereco = data.get('endereco')
    telefone = data.get('telefone')

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE CLIENTES SET NOME = :nome, ENDERECO = :endereco, TELEFONE = :telefone WHERE ID = :id",
            nome=nome, endereco=endereco, telefone=telefone, id=id
        )
        connection.commit()
        return jsonify({"message": "Cliente atualizado com sucesso!"}), 200
    except cx_Oracle.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM CLIENTES WHERE ID = :id", id=id)
        connection.commit()
        return jsonify({"message": "Cliente deletado com sucesso!"}), 200
    except cx_Oracle.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
