"""
Calcula los primeros N números de Fibonacci en versiones serial y paralela
para comparar rendimiento entre estrategias de ejecución.
 
Curso: Infraestructuras Paralelas y Distribuidas (750023C)
Autor: Brandon Franco
"""
import time
import concurrent.futures

N = 20  # Número de Fibonacci a calcular

#Algortimo recursivo para calcular Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


#VERSIÓN SERIAL
#Puse esta opción para poder comparar tiempos de ejcución al final.
def calcular_fibonacci_serial(n_elementos):
    inicio = time.time()
    resultados = [fibonacci(i) for i in range(n_elementos)]
    
    fin = time.time()
    print(f"Fibonacci ({n_elementos}): {resultados}")
    print(f"Tiempo serial: {fin - inicio:.4f} segundos")

#VERSIÓN PARALELA
"""
Aquí entra la paralelización.

Cambié en donde se guardan los future de listas a diccionarios para poder asociar el índice de cada elemento con su resultado
y que a la hora de hacer el print no se pierda el orden de los elementos. Esto es importante porque el orden de ejecución de 
los futuros no es garantizado, y si se usara una lista, los resultados podrían aparecer desordenados.
"""
def calcular_fibonacci_paralelo(n_elementos, executor_type):
    inicio = time.time()  
    resultados = [0] * n_elementos

    with executor_type() as executor:
        futures = {executor.submit(fibonacci, i): i for i in range(n_elementos)}

        for future, i in futures.items():
            resultados[i] = future.result()

    fin = time.time()
    tiempo_ejecucion = fin - inicio

    print(f"Fibonacci ({n_elementos}): {resultados}")
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")

if __name__ == "__main__":

    #Se ejecuta el cálculo de Fibonacci en versiones serial y paralela, mostrando los resultados y tiempos de ejecución.

    print("=== Serial ===")
    calcular_fibonacci_serial(N)

    print("=== Con ThreadPoolExecutor ===")
    calcular_fibonacci_paralelo(N, concurrent.futures.ThreadPoolExecutor)

    print("\n=== Con ProcessPoolExecutor ===")
    calcular_fibonacci_paralelo(N, concurrent.futures.ProcessPoolExecutor)