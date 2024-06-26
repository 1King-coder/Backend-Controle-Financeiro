from fastapi import FastAPI, HTTPException, Response
from requests import request
from ..controllers.Gasto_geral_controller import Gasto_geral_controller
from ..controllers.Banco_controller import Banco_controller
from ..controllers.Direcionamento_controller import Direcionamento_controller
import json

def init_routes (app: FastAPI, db_name: str) -> None:

    Gasto_geral_C = Gasto_geral_controller(db_name)
    Banco_C = Banco_controller(db_name)
    Direcionamento_C = Direcionamento_controller(db_name)

    @app.get("/gastos_gerais")
    def mostrar_gastos_gerais():
        return Response(
            content=json.dumps(Gasto_geral_C.mostrar()),
            media_type="application/json"
        )
    
    @app.get("/gastos_gerais/{id_gasto_geral}")
    def mostrar_gasto_geral(id_gasto_geral: int):
        dados = Gasto_geral_C.get_dados(id_gasto_geral)

        if not dados:
            raise HTTPException(status_code=404, detail="Gasto geral/imediato não encontrado")
        
        return Response(
            content=json.dumps(dados),
            media_type="application/json"
        )

    @app.post("/gastos_gerais")
    def criar_gasto_geral(req: dict):
    
        for gasto in req['gastos']:
            adicionou = Gasto_geral_C.adicionar(**gasto)
            if not adicionou:
                raise HTTPException(
                    status_code=400,
                    detail="Ocorreu um erro ao criar o gasto geral/ imediato"
                )
            
        ids = [
            [gasto['id_banco'], gasto['id_direcionamento']] for gasto in req['gastos']
        ]

        try:

            for id_banco, id_direcionamento in ids:
                Banco_C.atualiza_saldo(id_banco)
                Direcionamento_C.atualizar(id_direcionamento)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")

        return Response(
            content=json.dumps({"message": "Gasto geral/imediato adicionado com sucesso"}),
            media_type="application/json",
            status_code=201
        )
    

    @app.delete("/gastos_gerais/{id_gasto_geral}")
    def deletar_gasto_geral(id_gasto_geral: int):
        dados_gasto_geral = Gasto_geral_C.get_dados(id_gasto_geral)

        if not dados_gasto_geral:
            raise HTTPException(status_code=404, detail="Gasto geral/imediato não encontrado")

        if not Gasto_geral_C.deletar(id_gasto_geral):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao excluir o gasto geral/imediato")

        try:

            Banco_C.atualiza_saldo(dados_gasto_geral['id_banco'])
            Direcionamento_C.atualizar(dados_gasto_geral['id_direcionamento'])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")

        return Response(
            content=json.dumps({"message": "Gasto geral/imediato excluído com sucesso"}),
            media_type="application/json"
        )
    
    @app.put("/gastos_gerais/{id_gasto_geral}")
    def editar_gasto_geral(id_gasto_geral: int, req: dict):

        dados_gasto_geral = Gasto_geral_C.get_dados(id_gasto_geral)

        if not dados_gasto_geral:
            raise HTTPException(status_code=404, detail="Gasto geral/imediato não encontrado")
        
        if not Gasto_geral_C.editar(id_gasto_geral, **req):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar o gasto geral/imediato")
        
        try:
            Banco_C.atualiza_saldo(dados_gasto_geral['id_banco'])
            Direcionamento_C.atualizar(dados_gasto_geral['id_direcionamento'])

            if req.get('novo_id_banco'):
                Banco_C.atualiza_saldo(req['novo_id_banco'])

            if req.get('novo_id_direcionamento'):
                Direcionamento_C.atualizar(req['novo_id_direcionamento'])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")
        
        return Response(
            content=json.dumps({"message": "Gasto geral/imediato editado com sucesso"}),
            media_type="application/json"
        )





