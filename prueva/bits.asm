# bits.asm
# Operaciones con bits: lui, andi, srli, slli y xor
# input: ninguno
# output: a0 = 0x12345678, a1 = 0x78, a2 = 0x1234, a3 = 0x780, a4 = 0
    lui a0, 0x12345       # a0 = 0x12345000
    addi a0, a0, 0x678    # a0 = 0x12345678
    andi a1, a0, 0xFF     # a1 = ultimo byte = 0x78
    srli a2, a0, 16       # a2 = 16 bits de arriba = 0x1234
    slli a3, a1, 4        # a3 = a1 desplazado 4 bits = 0x780
    xor a4, a1, a1        # a4 = 0 (un numero xor si mismo)
    ebreak
