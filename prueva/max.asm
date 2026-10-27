# max.asm
# Encuentra el mayor de dos numeros
# input: a0 = 15, a1 = 27
# output: t0 = mayor
    addi a0, zero, 15     # a0 = 15
    addi a1, zero, 27     # a1 = 27
    bge a0, a1, mayor_a0  # si a0 >= a1, el mayor es a0
    add t0, a1, zero      # t0 = a1
    jal zero, fin         # saltar al final
mayor_a0:
    add t0, a0, zero      # t0 = a0
fin:
    ebreak                # el resultado esta en t0 (27)
