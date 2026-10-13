"""Conversación con el agente en la consola: python -m cotizador_agente"""

from .agente import AgenteCotizador


def main() -> None:
    agente = AgenteCotizador()
    print("Agente Cotizador de La Ventanería. Escriba 'salir' para terminar.\n")
    while True:
        try:
            texto = input("Cliente: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if texto.lower() in ("salir", "exit"):
            break
        if texto:
            print(f"\nAgente: {agente.responder(texto)}\n")


if __name__ == "__main__":
    main()
