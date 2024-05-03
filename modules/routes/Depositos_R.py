import json

from fastapi import FastAPI, HTTPException, Response

from modules.controllers.Deposito_controller import Deposito_controller
from modules.controllers.Banco_controller import Banco_controller
from modules.controllers.Direcionamento_controller import Direcionamento_controller
from requests import request

def init_routes(app: FastAPI, db_name: str) -> None:
    Deposito_C = Deposito_controller(db_name)
    Banco_C = Banco_controller(db_name)
    Direcionamento_C = Direcionamento_controller(db_name)

    @app.get("/depositos")
    def mostrar_depositos():
        return Response(
            content=json.dumps(Deposito_C.mostrar()),
            media_type="application/json"
        )

    @app.post("/depositos")
    def criar_deposito(req: dict):
        
        for deposito in req['depositos']:
            adicionou = Deposito_C.adicionar(**deposito)
            if not adicionou:
                raise HTTPException(
                    status_code=400,
                    detail="Ocorreu um erro ao criar o deposito"
                )
            
        ids = [
            (deposito['id_banco'], deposito['id_direcionamento']) for deposito in req['depositos']
        ]
            
        try:
            for id_banco, id_direcionamento in ids:

                Banco_C.atualiza_saldo(id_banco)
                Direcionamento_C.atualizar(id_direcionamento)

        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")


        return Response(
            content=json.dumps({"message": "Depósito adicionado com sucesso"}),
            media_type="application/json",
            status_code=201
        )

    @app.delete("/depositos/{id_deposito}")
    def deletar_deposito(id_deposito: int):
        dados_deposito = Deposito_C.get_dados_deposito(id_deposito)

        if not dados_deposito:
            raise HTTPException(status_code=404, detail="Depósito não encontrado")

        if not Deposito_C.deletar(id_deposito):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao excluir o depósito")

        try:

            Banco_C.atualiza_saldo(dados_deposito['id_banco'])
            Direcionamento_C.atualizar(dados_deposito['id_direcionamento'])

        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")


        return Response(
            content=json.dumps({"message": "Depósito excluído com sucesso"}),
            media_type="application/json"
        )

    @app.put("/depositos/{id_deposito}")
    def editar_deposito(id_deposito: int, req: dict):
        dados_deposito = Deposito_C.get_dados_deposito(id_deposito)

        if not dados_deposito:
            raise HTTPException(status_code=404, detail="Depósito não encontrado")

        if not Deposito_C.editar(id_deposito, **req):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar o valor do depósito")

        try:
            Banco_C.atualiza_saldo(dados_deposito['id_banco'])
            Direcionamento_C.atualizar(dados_deposito['id_direcionamento'])

            if req.get('novo_id_banco'):
                Banco_C.atualiza_saldo(req['novo_id_banco'])
                

            if req.get('novo_id_direcionamento'):
                Direcionamento_C.atualizar(req['id_direcionamento'])
                
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")

        return Response(
            content=json.dumps({"message": "Depósito editado com sucesso"}),
            media_type="application/json"
        )
