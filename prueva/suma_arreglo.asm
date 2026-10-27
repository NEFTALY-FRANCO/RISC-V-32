# suma_arreglo.asm
# Guarda 3 numeros en memoria y los suma leyendolos uno por uno
# input: arreglo en memoria = 10, 20, 30
# output: t2 = suma del arreglo
    addi t0, zero, 10     # primer numero
    sw t0, 0(zero)        # memoria[0] = 10
    addi t0, zero, 20     # segundo numero
    sw t0, 4(zero)        # memoria[4] = 20
    addi t0, zero, 30     # tercer numero
    sw t0, 8(zero)        # memoria[8] = 30
    addi t1, zero, 0      # t1 = direccion actual
    addi t2, zero, 0      # t2 = suma
    addi t3, zero, 12     # t3 = direccion final
sumar:
    bge t1, t3, fin       # si ya llego al final, terminar
    lw t4, 0(t1)          # t4 = memoria[t1]
    add t2, t2, t4        # suma = suma + t4
    addi t1, t1, 4        # siguiente direccion
    jal zero, sumar       # repetir
fin:
    ebreak                # el resultado esta en t2 (60)
