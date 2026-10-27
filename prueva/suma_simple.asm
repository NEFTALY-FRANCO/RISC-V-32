# suma_simple.asm
# Suma dos numeros, los guarda en memoria y los vuelve a leer
# input: ninguno
# output: a2 = 7, a3 = 7 (leido desde memoria)
    addi a1, zero, 2      # a1 = 2   (en vez de: li a1, 2)
    addi a0, zero, 5      # a0 = 5   (en vez de: li a0, 5)
    add a2, a1, a0        # a2 = a1 + a0 = 7
    sw a2, 0x18(zero)     # guarda a2 en la direccion 0x18
    lw a3, 0x18(zero)     # lee la direccion 0x18 en a3
    ebreak                # el resultado esta en a2 y a3
