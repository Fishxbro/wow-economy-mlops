from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="wow_economy_verificacion",
    description="Verificacion inicial de Apache Airflow para WoW Economy MLOps",
    schedule=None,
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["wow", "mlops", "verificacion"],
)
def wow_economy_verificacion():

    @task
    def verificar_entorno():
        print("Iniciando verificacion de WoW Economy MLOps")
        return "Entorno Airflow funcionando"

    @task
    def verificar_proyecto(resultado):
        print(f"Resultado anterior: {resultado}")
        print("Proyecto: WoW Economy MLOps")
        print("Componente: Apache Airflow")
        return True

    @task
    def finalizar(resultado):
        if not resultado:
            raise RuntimeError("La verificacion no fue exitosa")

        print("Verificacion completada correctamente")
        print("Airflow esta listo para integrar los pipelines")

    estado = verificar_entorno()
    comprobacion = verificar_proyecto(estado)
    finalizar(comprobacion)


wow_economy_verificacion()

