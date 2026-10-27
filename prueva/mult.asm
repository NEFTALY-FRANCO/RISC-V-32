# mult.asm
# Multiplica dos numeros usando sumas repetidas
# input: a0 = 6, a1 = 7
# output: a2 = a0 * a1
    addi a0, zero, 6      # a0 = 6
    addi a1, zero, 7      # a1 = 7 (cuantas veces sumar)
    addi a2, zero, 0      # resultado = 0
mult:
    beq a1, zero, fin     # si a1 == 0, terminar
    add a2, a2, a0        # resultado = resultado + a0
    addi a1, a1, -1       # a1 = a1 - 1
    jal zero, mult        # repetir
fin:
    ebreak                # el resultado esta en a2 (42)
