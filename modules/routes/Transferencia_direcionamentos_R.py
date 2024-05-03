
from fastapi import FastAPI, HTTPException, Response

from ..controllers.Transferencia_entre_direcionamentos_controller import Transferencia_entre_direcionamentos_controller
from ..controllers.Direcionamento_controller import Direcionamento_controller
import json
from requests import request

def init_routes(app: FastAPI, db_name: str) -> None:
    """
    Function that creates the CRUD routes for Transferencias_entre_direcionamentos
    """
    transferencia_direcionamentos_controller = Transferencia_entre_direcionamentos_controller(db_name)
    Direcionamento_C = Direcionamento_controller(db_name)
    @app.get("/transferencias_entre_direcionamentos")
    def get_transferencias():
        
        return Response(
            content=json.dumps(transferencia_direcionamentos_controller.mostrar()),
            media_type="application/json"
        )

    @app.get("/transferencias_entre_direcionamentos/{id_transf}")
    def get_transferencia_by_id(id_transf: int):
        """
        Returns a transferencia_entre_direcionamentos based on its id
        """
        return Response(
            content=json.dumps(transferencia_direcionamentos_controller.get_dados(id_transf)),
        )

    @app.post("/transferencias_entre_direcionamentos")
    def insere_transferencia(req: dict):
        if not transferencia_direcionamentos_controller.adicionar(**req):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao criar a transferência entre direcionamentos")
        
        try:
            Direcionamento_C.atualizar(req['id_direcionamento_origem'])
            Direcionamento_C.atualizar(req['id_direcionamento_destino'])
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo dos direcionamentos: {e}")

        return Response(
            content=json.dumps({"message": "Transferência entre direcionamentos adicionada com sucesso"}),
            media_type="application/json",
            status_code=201
        )

    @app.put("/transferencias_entre_direcionamentos/{id_transf}")
    def edita_transferencia(id_transf: int, req: dict):
        """
        Updates a transferencia_entre_direcionamentos based on its id
        """

        dados_transf = transferencia_direcionamentos_controller.get_dados(id_transf)

        if not dados_transf:
            raise HTTPException(status_code=404, detail="Transferência entre direcionamentos não encontrada")
        
        if not transferencia_direcionamentos_controller.editar(id_transf, **req):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar a transferência entre direcionamentos")
        
        try:
            Direcionamento_C.atualizar(dados_transf['id_direcionamento_origem'])
            Direcionamento_C.atualizar(dados_transf['id_direcionamento_destino'])
        
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo dos direcionamentos: {e}")

        return Response(
            content=json.dumps({"message": "Transferência entre direcionamentos editada com sucesso"}),
            media_type="application/json",
        )
    
    @app.delete("/transferencias_entre_direcionamentos/{id_transf}")
    def deletar_transferencia(id_transf: int):
        dados_transf = transferencia_direcionamentos_controller.get_dados(id_transf)

        if not dados_transf:
            raise HTTPException(status_code=404, detail="Transferência entre direcionamentos não encontrada")
        
        if not transferencia_direcionamentos_controller.deletar(id_transf):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao excluir a transferência entre direcionamentos")
        
        try:
            Direcionamento_C.atualizar(dados_transf['id_direcionamento_origem'])
            Direcionamento_C.atualizar(dados_transf['id_direcionamento_destino'])
        
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo dos direcionamentos: {e}")

        return Response(content=json.dumps({"message": "Transferência entre direcionamentos excluída com sucesso"}), media_type="application/json")