from ..controllers.Banco_controller import Banco_controller
import json
from fastapi import HTTPException, Response



def init_routes (app, db_name: str) -> None:
    Banco_C = Banco_controller(db_name)
    @app.get("/bancos")
    def mostrar_bancos():
        return Response(content=json.dumps(Banco_C.mostrar()), media_type="application/json")
    
    @app.get("/bancos/{id_banco}")
    def mostrar_banco(id_banco: int):
        dados = Banco_C.get_dados_banco(id_banco)

        if not dados:
            raise HTTPException(status_code=404, detail="Banco não encontrado")
        
        return Response(content=json.dumps(dados), media_type="application/json")
    
    @app.get("/bancos/get-id/{nome_banco}")
    def id_banco_por_nome(nome_banco: str):
        id_banco = Banco_C.get_id_banco(nome_banco)

        if not id_banco:
            raise HTTPException(status_code=404, detail="Banco não encontrado")
        
        return Response(content=json.dumps({"id_banco": id_banco}), media_type="application/json")
    
    @app.post("/bancos")
    def criar_banco(banco: dict):
        adicionou = Banco_C.adiciona_banco(banco["nome_banco"])
        
        if not adicionou:
            raise HTTPException(status_code=400, detail="Banco já existe")
        
        return Response(content=json.dumps({"message": "Banco adicionado com sucesso"}), media_type="application/json", status_code=201)


    @app.put("/bancos/{id_banco}")
    def editar_banco(id_banco: int, banco: dict):
        if not Banco_C.get_dados_banco(id_banco):
            raise HTTPException(status_code=404, detail="Banco não encontrado")
        
        novo_nome = banco["novo_nome"]
        if not isinstance(novo_nome, str):
            raise HTTPException(status_code=400, detail="Nome não é uma string")
        
        if not Banco_C.edita_nome_banco(id_banco, novo_nome):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar o nome do banco")
            
        return Response(content=json.dumps({"message": "Banco editado com sucesso"}), media_type="application/json")

    @app.delete("/bancos/{id_banco}")
    def deletar_banco(id_banco: int):
        if not Banco_C.get_dados_banco(id_banco):
            raise HTTPException(status_code=404, detail="Banco não encontrado")
        
        if not Banco_C.deleta_banco(id_banco):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao excluir o banco")

        return Response(content=json.dumps({"message": "Banco excluído com sucesso"}), media_type="application/json")

    @app.patch("/bancos/{id_banco}")
    def atualiza_saldo_banco(id_banco: int):

        dados_banco = Banco_C.get_dados_banco(id_banco)

        if not dados_banco:
            raise HTTPException(status_code=404, detail="Banco não encontrado")
        
        if not Banco_C.atualiza_saldo(id_banco):
            return Response(
                status_code= 208,
                content=json.dumps({"message": f"O Banco {dados_banco['nome']} não precisa ter seu saldo atualizado."}),
            )
        
        return Response(content=json.dumps({"message": "Saldo atualizado com sucesso"}), media_type="application/json")

