# sum_n.asm
# Calcula la suma de los primeros n numeros
# input: a0 = n
# output: t0 = suma(1..n)
    addi a0, zero, 5      # n = 5
    addi t0, zero, 0      # suma = 0
loop:
    beq a0, zero, fin     # si n == 0, terminar
    add t0, t0, a0        # suma = suma + n
    addi a0, a0, -1       # n = n - 1
    jal zero, loop        # volver a loop
fin:
    ebreak                # el resultado esta en t0 (15)
