# fibonacci.asm
# Guarda en memoria los primeros 8 numeros de Fibonacci
# input: t3 = cantidad de terminos
# output: memoria desde la direccion 0 = 0,1,1,2,3,5,8,13
    addi t0, zero, 0      # t0 = fib(n-2) = 0
    addi t1, zero, 1      # t1 = fib(n-1) = 1
    addi t2, zero, 0      # t2 = direccion actual de memoria
    addi t3, zero, 8      # t3 = contador de terminos
bucle:
    beq t3, zero, fin     # si el contador es 0, terminar
    sw t0, 0(t2)          # guardar t0 en memoria
    add t4, t0, t1        # t4 = t0 + t1 (siguiente termino)
    add t0, t1, zero      # t0 = t1
    add t1, t4, zero      # t1 = t4
    addi t2, t2, 4        # siguiente direccion (4 bytes)
    addi t3, t3, -1       # contador = contador - 1
    jal zero, bucle       # repetir
fin:
    ebreak
