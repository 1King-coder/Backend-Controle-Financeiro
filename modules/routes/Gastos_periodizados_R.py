from ..controllers.Gasto_periodizado_controller import Gasto_periodizado_controller
from ..controllers.Banco_controller import Banco_controller
from ..controllers.Direcionamento_controller import Direcionamento_controller
from fastapi import FastAPI, HTTPException, Response
from requests import request
import json

def init_routes(app, db_name):
    Gasto_periodizado_C = Gasto_periodizado_controller(db_name)
    Banco_C = Banco_controller(db_name)
    Direcionamento_C = Direcionamento_controller(db_name)

    @app.post("/gastos_periodizados")
    def adiciona_gasto_periodizado(req: dict):
        adicionou = Gasto_periodizado_C.adicionar(
            **req
        )

        if not adicionou:
            raise HTTPException(status_code=400, detail="Ocorreu um erro ao criar o gasto periodizado")

        try:

            Banco_C.atualiza_saldo(req['id_banco'])
            Direcionamento_C.atualizar(req['id_direcionamento'])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")

        return Response(
            content=json.dumps({"message": "Gasto periodizado adicionado com sucesso"}),
            media_type="application/json",
            status_code=201
        )
    
    @app.get("/gastos_periodizados/{id_gasto_periodizado}")
    def mostra_gasto_periodizado(id_gasto_periodizado: int):

        dados = Gasto_periodizado_C.get_dados(id_gasto_periodizado)

        if not dados:
            raise HTTPException(status_code=404, detail="Gasto periodizado não encontrado")
        
        return Response(
            content=json.dumps(dados),
            media_type="application/json"
        )
    
    @app.get("/gastos_periodizados")
    def mostrar_gastos_periodizados():
        return Response(
            content=json.dumps(Gasto_periodizado_C.mostrar()),
            media_type="application/json"
        )
    
    @app.put("/gastos_periodizados/{id_gasto_periodizado}")
    def edita_gasto_periodizado(id_gasto_periodizado: int, req: dict):
        dados_gasto_periodizado = Gasto_periodizado_C.get_dados(id_gasto_periodizado)

        if not dados_gasto_periodizado:
            raise HTTPException(status_code=404, detail="Gasto periodizado não encontrado")
        
        editou = Gasto_periodizado_C.editar(id_gasto_periodizado, **req)
        
        if not editou:
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar o gasto periodizado")

        dados_gasto_geral = request(
            "GET",
            f"http://localhost:8000/gastos_gerais/{id_gasto_periodizado}",
        ).json()

        id_banco, id_direcionamento = dados_gasto_geral['id_banco'], dados_gasto_geral['id_direcionamento']

        
        try:
            if dados_gasto_periodizado.get('controle_parcelas'):
                Banco_C.atualiza_saldo(id_banco)
                Direcionamento_C.atualizar(id_direcionamento)

            if req.get('novo_id_banco'):
                Banco_C.atualiza_saldo(req['novo_id_banco'])

            if req.get('novo_id_direcionamento'):
                Direcionamento_C.atualizar(req['novo_id_direcionamento'])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")
        
        return Response(
            content=json.dumps({"message": "Gasto periodizado editado com sucesso"}),
            media_type="application/json"
        )
    
    @app.delete("/gastos_periodizados/{id_gasto_periodizado}")
    def deleta_gasto_periodizado(id_gasto_periodizado: int):
        dados_gasto_periodizado = Gasto_periodizado_C.get_dados(id_gasto_periodizado)

        if not dados_gasto_periodizado:
            raise HTTPException(status_code=404, detail="Gasto periodizado não encontrado")

        if not Gasto_periodizado_C.deletar(id_gasto_periodizado):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao excluir o gasto periodizado")

        try:

            Banco_C.atualiza_saldo(dados_gasto_periodizado['id_banco'])
            Direcionamento_C.atualizar(dados_gasto_periodizado['id_direcionamento'])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo do banco e/ou direcionamento: {e}")

        return Response(
            content=json.dumps({"message": "Gasto periodizado excluído com sucesso"}),
            media_type="application/json"
        )



    @app.patch("/gastos_periodizados")
    def atualiza_controle_parcelas():
        todos_id_gastos_periodizados = [
            gasto_periodizado['id_gasto'] for gasto_periodizado in Gasto_periodizado_C.mostrar()
        ]

        try:
            
            for id_gasto in todos_id_gastos_periodizados:
                atualizou = Gasto_periodizado_C.atualiza_controle_parcelas(id_gasto, 30)
                
                if atualizou and atualizou != 2:
                    dados_gasto = request(
                        "GET",
                        f"http://localhost:8000/gastos_gerais/{id_gasto}",
                    ).json()

                    Banco_C.atualiza_saldo(dados_gasto['id_banco'])
                    Direcionamento_C.atualizar(dados_gasto['id_direcionamento'])

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o controle de parcelas: {e}")

        return Response(
            content=json.dumps({"message": "Controle parcelas atualizado com sucesso"}),
            media_type="application/json"
        )


