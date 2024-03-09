
from fastapi import FastAPI, HTTPException, Response

from ..controllers.Transferencia_entre_bancos_controller import Transferencia_entre_bancos_controller
import json
from requests import request

def init_routes(app: FastAPI, db_name: str) -> None:
    """
    Function that creates the CRUD routes for Transferencias_entre_bancos
    """
    transferencia_bancos_controller = Transferencia_entre_bancos_controller(db_name)

    @app.get("/transferencias_entre_bancos")
    def get_transferencias():
        
        return Response(
            content=json.dumps(transferencia_bancos_controller.mostrar()),
            media_type="application/json"
        )

    @app.get("/transferencias_entre_bancos/{id_transf}")
    def get_transferencia_by_id(id_transf: int):
        """
        Returns a transferencia_entre_bancos based on its id
        """
        return Response(
            content=json.dumps(transferencia_bancos_controller.get_dados(id_transf)),
        )

    @app.post("/transferencias_entre_bancos")
    def insere_transferencia(req: dict):
        if not transferencia_bancos_controller.adicionar(**req):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao criar a transferência entre bancos")
        
        try:
            request(
                "PATCH",
                f"http://localhost:8000/bancos/{req['id_banco_origem']}",
            )

            request(
                "PATCH",
                f"http://localhost:8000/bancos/{req['id_banco_destino']}",
            )
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo dos bancos: {e}")

        return Response(
            content=json.dumps({"message": "Transferência entre bancos adicionada com sucesso"}),
            media_type="application/json",
            status_code=201
        )

    @app.put("/transferencias_entre_bancos/{id_transf}")
    def edita_transferencia(id_transf: int, req: dict):
        """
        Updates a transferencia_entre_bancos based on its id
        """

        dados_transf = transferencia_bancos_controller.get_dados(id_transf)

        if not dados_transf:
            raise HTTPException(status_code=404, detail="Transferência entre bancos não encontrada")
        
        if not transferencia_bancos_controller.editar(id_transf, **req):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao editar a transferência entre bancos")
        
        try:
            request(
                "PATCH",
                f"http://localhost:8000/bancos/{dados_transf['id_banco_origem']}",
            )

            request(
                "PATCH",
                f"http://localhost:8000/bancos/{dados_transf['id_banco_destino']}",
            )
        
        except Exception as e:
            return HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo dos bancos: {e}")


        
        return Response(
            content=json.dumps({"message": "Transferência entre bancos editada com sucesso"}),
            media_type="application/json",
        )

    @app.delete("/transferencias_entre_bancos/{id_transf}")
    def delete_transferencia(id_transf: int) -> None:
        """
        Deletes a transferencia_entre_bancos based on its id
        """
        dados_transf = transferencia_bancos_controller.get_dados(id_transf)

        if not dados_transf:
            raise HTTPException(status_code=404, detail="Transferência entre bancos não encontrada")

        if not transferencia_bancos_controller.deletar(id_transf):
            raise HTTPException(status_code=500, detail="Ocorreu um erro ao deletar a transferência entre bancos")
        
        try:
            request(
                "PATCH",
                f"http://localhost:8000/bancos/{dados_transf['id_banco_origem']}",
            )

            request(
                "PATCH",
                f"http://localhost:8000/bancos/{dados_transf['id_banco_destino']}",
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ocorreu um erro ao atualizar o saldo dos bancos: {e}")
        
        return Response(
            content=json.dumps({"message": "Transferência entre bancos excluída com sucesso"}),
            media_type="application/json",
        )
