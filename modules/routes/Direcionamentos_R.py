from ..controllers.Direcionamento_controller import Direcionamento_controller
from ..models.Direcionamento_model import Direcionamento_model
from fastapi import HTTPException, Response
import json


def init_routes(app, db_name: str):
    Direcionamento_C = Direcionamento_controller(db_name)

    @app.get("/direcionamentos")
    def mostrar_direcionamentos():
        return Response(
            content=json.dumps(Direcionamento_C.mostrar()),
            media_type="application/json"
        )
    
    @app.get("/direcionamentos/saldo-por-banco")
    def mostrar_direcionamentos_saldos_por_banco():
        return Response(
            content=json.dumps(Direcionamento_C.mostrar_saldos_por_banco()),
            media_type="application/json"
        )

    @app.get("/direcionamentos/{id_direcionamento}")
    def mostrar_direcionamento(id_direcionamento: int):
        dados = Direcionamento_C.get_dados_direcionamento(id_direcionamento)

        if not dados:
            raise HTTPException(status_code=404, detail="Direcionamento não encontrado")

        return Response(
            content=json.dumps(dados),
            media_type="application/json"
        )
    
    @app.get("/direcionamentos/saldo-por-banco/{id_direcionamento}")
    def mostrar_direcionamento(id_direcionamento: int):
        dados = Direcionamento_C.get_dados_direcionamento_por_banco(id_direcionamento)

        if not dados:
            raise HTTPException(status_code=404, detail="Direcionamento não encontrado")

        return Response(
            content=json.dumps(dados),
            media_type="application/json"
        )
    
    @app.get("/direcionamentos/get-id/{nome_direcionamento}")
    def id_direcionamento_por_nome(nome_direcionamento: str):
        id_direcionamento = Direcionamento_C.get_id_direcionamento(nome_direcionamento)

        if not id_direcionamento:
            raise HTTPException(status_code=404, detail="Direcionamento não encontrado")
        
        return Response(
            content=json.dumps({"id_direcionamento": id_direcionamento}),
            media_type="application/json"
        )

    @app.post("/direcionamentos")
    def criar_direcionamento(req: dict):
        adicionou = Direcionamento_C.adiciona_direcionamento(req['nome_direcionamento'])

        if not adicionou:
            raise HTTPException(status_code=400, detail="Direcionamento já existe")

        return Response(
            content=json.dumps({"message": "Direcionamento adicionado com sucesso"}),
            media_type="application/json",
            status_code=201 
        )

    @app.put("/direcionamentos/{id_direcionamento}")
    def editar_direcionamento(id_direcionamento: int, req: dict):

        if not Direcionamento_C.get_dados_direcionamento(id_direcionamento):
            raise HTTPException(status_code=404, detail="Direcionamento não encontrado")

        if not Direcionamento_C.edita_nome_direcionamentos(id_direcionamento, req['novo_nome']):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar o direcionamento")

        return Response(
            content=json.dumps({"message": "Direcionamento editado com sucesso"}),
            media_type="application/json"
        )        

    @app.delete("/direcionamentos/{id_direcionamento}", status_code=204)
    def deletar_direcionamento(id_direcionamento: int):
        if not Direcionamento_C.get_dados_direcionamento(id_direcionamento):
            raise HTTPException(status_code=404, detail="Direcionamento não encontrado")

        if not Direcionamento_C.deleta_direcionamento(id_direcionamento):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao excluir o direcionamento")
        
        return Response(
            content=json.dumps({"message": "Direcionamento excluído com sucesso"}),
            media_type="application/json"
        )
    
    @app.patch("/direcionamentos/{id_direcionamento}")
    def atualizar_saldo_direcionamento(id_direcionamento: int):

        dados_direcionamento = Direcionamento_C.get_dados_direcionamento(id_direcionamento)

        if not dados_direcionamento:
            raise HTTPException(status_code=404, detail="Direcionamento não encontrado")
        
        if not Direcionamento_C.atualizar(id_direcionamento):
            return Response(
                status_code= 208,
                content=json.dumps({"message": f"O Direcionamento {dados_direcionamento['nome']} não precisa ter seu saldo atualizado."}),
            )
        
        return Response(
            content=json.dumps({"message": "Direcionamento atualizado com sucesso"}),
            media_type="application/json"
        )



