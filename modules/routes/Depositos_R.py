import json

from fastapi import FastAPI, HTTPException, Response

from modules.controllers.Deposito_controller import Deposito_controller
from requests import request

def init_routes(app: FastAPI, db_name: str) -> None:
    Deposito_C = Deposito_controller(db_name)

    @app.get("/depositos")
    def mostrar_depositos():
        return Response(
            content=json.dumps(Deposito_C.mostrar()),
            media_type="application/json"
        )

    @app.post("/depositos")
    def criar_deposito(req: dict):
        adicionou = Deposito_C.adicionar(
            **req
        )

        if not adicionou:
            raise HTTPException(status_code=400, detail="Depósito já existe")

        try:

            request(
                "PATCH",
                f"http://localhost:8000/bancos/{req['id_banco']}",
            )

            request(
                "PATCH",
                f"http://localhost:8000/direcionamentos/{req['id_direcionamento']}",
            )

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

            request(
                "PATCH",
                f"http://localhost:8000/bancos/{dados_deposito['id_banco']}",
            )

            request(
                "PATCH",
                f"http://localhost:8000/direcionamentos/{dados_deposito['id_direcionamento']}",
            )

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
            request(
                "PATCH",
                f"http://localhost:8000/bancos/{dados_deposito['id_banco']}",
            )

            request(
                "PATCH",
                f"http://localhost:8000/direcionamentos/{dados_deposito['id_direcionamento']}",
            )

            if req.get('novo_id_banco'):
                request(
                    "PATCH",
                    f"http://localhost:8000/bancos/{req['novo_id_banco']}",
                )

            if req.get('novo_id_direcionamento'):
                request(
                    "PATCH",
                    f"http://localhost:8000/direcionamentos/{req['novo_id_direcionamento']}",
                )
                
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")

        return Response(
            content=json.dumps({"message": "Depósito editado com sucesso"}),
            media_type="application/json"
        )
