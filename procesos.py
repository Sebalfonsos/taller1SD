import multiprocessing as mp
import time
import os

def worker(label, seconds=180):
    pid = os.getpid()
    print(f"[{label}] PID={pid} iniciado; durará {seconds} s")
    time.sleep(seconds)  # se mantiene "vivo" 3 minutos
    print(f"[{label}] PID={pid} finalizado")

if __name__ == "__main__":
    procesos = []
    for i in range(1, 6):
        p = mp.Process(target=worker, args=(f"proc-{i}",))
        p.start()
        procesos.append(p)

    # Espera a que terminen (opcional para mantener el main vivo)
    for p in procesos:
        p.join()