import sys

REGISTROS = {
    "x0": "00000",
    "x1": "00001",
    "x2": "00010",
    "x3": "00011",
    "x4": "00100",
    "x5": "00101",
    "x6": "00110",
    "x7": "00111",
    "x8": "01000",
    "x9": "01001",
    "x10": "01010",
    "x11": "01011",
    "x12": "01100",
    "x13": "01101",
    "x14": "01110",
    "x15": "01111",
    "x16": "10000",
    "x17": "10001",
    "x18": "10010",
    "x19": "10011",
    "x20": "10100",
    "x21": "10101",
    "x22": "10110",
    "x23": "10111",
    "x24": "11000",
    "x25": "11001",
    "x26": "11010",
    "x27": "11011",
    "x28": "11100",
    "x29": "11101",
    "x30": "11110",
    "x31": "11111",

    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
    "fp": "01000"
}

INST = {
    # (Tipo, Opcode, funct3, funct7)
    "add":  ("R", "0110011", "000", "0000000"),
    "sub":  ("R", "0110011", "000", "0100000"),
    "xor":  ("R", "0110011", "100", "0000000"),
    "or":   ("R", "0110011", "110", "0000000"),
    "and":  ("R", "0110011", "111", "0000000"),
    "sll":  ("R", "0110011", "001", "0000000"),
    "srl":  ("R", "0110011", "101", "0000000"),
    "sra":  ("R", "0110011", "101", "0100000"),
    "slt":  ("R", "0110011", "010", "0000000"),
    "sltu": ("R", "0110011", "011", "0000000"),
    # I aritmeticas
    "addi":  ("I", "0010011", "000", None),
    "xori":  ("I", "0010011", "100", None),
    "ori":   ("I", "0010011", "110", None),
    "andi":  ("I", "0010011", "111", None),
    "slti":  ("I", "0010011", "010", None),
    "sltiu": ("I", "0010011", "011", None),
    "slli":  ("I", "0010011", "001", "0000000"),
    "srli":  ("I", "0010011", "101", "0000000"),
    "srai":  ("I", "0010011", "101", "0100000"),
    # I loads
    "lb":  ("I", "0000011", "000", None),
    "lh":  ("I", "0000011", "001", None),
    "lw":  ("I", "0000011", "010", None),
    "lbu": ("I", "0000011", "100", None),
    "lhu": ("I", "0000011", "101", None),
    # I otras
    "jalr":   ("I", "1100111", "000", None),
    "ecall":  ("I", "1110011", "000", None),
    "ebreak": ("I", "1110011", "000", None),
    # S
    "sb": ("S", "0100011", "000", None),
    "sh": ("S", "0100011", "001", None),
    "sw": ("S", "0100011", "010", None),
    # B
    "beq":  ("B", "1100011", "000", None),
    "bne":  ("B", "1100011", "001", None),
    "blt":  ("B", "1100011", "100", None),
    "bge":  ("B", "1100011", "101", None),
    "bltu": ("B", "1100011", "110", None),
    "bgeu": ("B", "1100011", "111", None),
    # U
    "lui":   ("U", "0110111", None, None),
    "auipc": ("U", "0010111", None, None),
    # J
    "jal": ("J", "1101111", None, None),
}


def manager_ARCH(entrada):

    etiquetas = {}

    # PASADA 1: guardar donde esta cada etiqueta
    PC = 0

    with open(entrada, "r") as archivo:

        for linea in archivo:

            linea = linea.split("#")[0].strip()

            if linea == "":
                continue

            if ":" in linea:

                etiqueta, resto = linea.split(":", 1)

                etiquetas[etiqueta.strip()] = PC

                linea = resto.strip()

                if linea == "":
                    continue

            PC += 4

    # PASADA 2: convertir cada instruccion
    PC = 0

    # el archivo de salida se llama igual que la entrada pero con .hex
    # (se quita la extension solo si el archivo tiene una)
    nombre_hex = entrada
    ultimo = entrada.split("/")[-1].split("\\")[-1]   # nombre sin carpetas

    if "." in ultimo:
        nombre_hex = entrada.rsplit(".", 1)[0]

    nombre_hex = nombre_hex + ".hex"
    archivo_hex = open(nombre_hex, "w")

    with open(entrada, "r") as archivo:

        for linea in archivo:

            linea = linea.split("#")[0].strip()

            if linea == "":
                continue

            if ":" in linea:

                _, linea = linea.split(":", 1)

                linea = linea.strip()

                if linea == "":
                    continue

            partes = linea.replace(",", " ").split()

            nombre = partes[0]

            if nombre not in INST:
                print("Instrucción inválida:", nombre)
                archivo_hex.close()
                return

            tipo = INST[nombre][0]

            if tipo == "R":

                bits = manager(nombre, partes[1], partes[2], partes[3])

            elif tipo == "I":

                if nombre == "ecall" or nombre == "ebreak":

                    bits = manager(nombre)

                elif nombre in ["lb", "lh", "lw", "lbu", "lhu", "jalr"]:

                    # lw x5, 8(sp)
                    rd = partes[1]

                    operando = partes[2]

                    if "(" in operando:

                        imm = operando.split("(")[0]

                        rs1 = operando.split("(")[1].replace(")", "")

                    else:

                        imm = "0"
                        rs1 = operando

                    if imm == "":
                        imm = "0"

                    bits = manager(nombre, rd, rs1, None, int(imm, 0))

                else:

                    bits = manager(nombre, partes[1], partes[2], None, int(partes[3], 0))

            elif tipo == "S":

                # sw x5, 8(sp)
                rs2 = partes[1]

                operando = partes[2]

                imm = operando.split("(")[0]

                rs1 = operando.split("(")[1].replace(")", "")

                if imm == "":
                    imm = "0"

                bits = manager(nombre, None, rs1, rs2, int(imm, 0))

            elif tipo == "B":

                rs1 = partes[1]
                rs2 = partes[2]
                destino = partes[3]

                if destino in etiquetas:
                    offset = etiquetas[destino] - PC
                else:
                    offset = int(destino, 0)

                bits = manager(nombre, None, rs1, rs2, offset)

            elif tipo == "U":

                bits = manager(nombre, partes[1], None, None, int(partes[2], 0))

            elif tipo == "J":

                rd = partes[1]
                destino = partes[2]

                if destino in etiquetas:
                    offset = etiquetas[destino] - PC
                else:
                    offset = int(destino, 0)

                bits = manager(nombre, rd, None, None, offset)

            # si hubo error en manager, no sigue
            if bits == "":
                archivo_hex.close()
                return

            # pasar los 32 bits a hexadecimal (8 digitos) y escribirlos
            hexa = format(int(bits, 2), "08x")
            archivo_hex.write(hexa + "\n")

            PC += 4

    archivo_hex.close()
    print("Archivo creado:", nombre_hex)


def manager(nombre, rd=None, rs1=None, rs2=None, imm=None):

    # verificar si la instruccion existe
    if nombre not in INST:
        print("La instruccion no existe")
        return ""

    # verificar que los registros existan
    if rd != None and rd not in REGISTROS:
        print("Registro inválido:", rd)
        return ""
    if rs1 != None and rs1 not in REGISTROS:
        print("Registro inválido:", rs1)
        return ""
    if rs2 != None and rs2 not in REGISTROS:
        print("Registro inválido:", rs2)
        return ""

    # tomar los valores de la instruccion
    datos = INST[nombre]
    tipo = datos[0]
    opcode = datos[1]
    funct3 = datos[2]
    funct7 = datos[3]

    bit_line = ""

    if tipo == "R":
        bit_line = assembler_R(funct7, rs2, rs1, funct3, rd, opcode)

    elif tipo == "I":
        if nombre == "ecall":
            bit_line = "000000000000" + "00000" + funct3 + "00000" + opcode
        elif nombre == "ebreak":
            bit_line = "000000000001" + "00000" + funct3 + "00000" + opcode
        else:
            bit_line = assembler_I(imm, REGISTROS[rs1], funct3, REGISTROS[rd], opcode, funct7)

    elif tipo == "S":
        bit_line = assembler_S(imm, REGISTROS[rs2], REGISTROS[rs1], funct3, opcode)

    elif tipo == "B":
        bit_line = assembler_B(imm, REGISTROS[rs2], REGISTROS[rs1], funct3, opcode)

    elif tipo == "U":
        bit_line = assembler_U(imm, REGISTROS[rd], opcode)

    elif tipo == "J":
        bit_line = assembler_J(imm, REGISTROS[rd], opcode)

    print(bit_line)
    return bit_line


def assembler_R(funct7, rs2, rs1, funct3, rd, opcode):
    return funct7 + REGISTROS[rs2] + REGISTROS[rs1] + funct3 + REGISTROS[rd] + opcode


def assembler_I(imm, rs1, funct3, rd, opcode, funct7=None):

    if funct7 is None:
        imm = format(imm & 0xFFF, "012b")
    else:
        imm = funct7 + format(imm & 0x1F, "05b")

    return imm + rs1 + funct3 + rd + opcode


def assembler_S(imm, rs2, rs1, funct3, opcode):
    imm = format(imm & 0xFFF, "012b")
    imm_high = imm[:7]
    imm_low = imm[7:]
    return imm_high + rs2 + rs1 + funct3 + imm_low + opcode


def assembler_B(imm, rs2, rs1, funct3, opcode):
    imm = format(imm & 0x1FFF, "013b")
    imm12 = imm[0]
    imm11 = imm[1]
    imm10_5 = imm[2:8]
    imm4_1 = imm[8:12]
    return imm12 + imm10_5 + rs2 + rs1 + funct3 + imm4_1 + imm11 + opcode


def assembler_U(imm, rd, opcode):
    return format(imm & 0xFFFFF, "020b") + rd + opcode


def assembler_J(imm, rd, opcode):
    imm = format(imm & 0x1FFFFF, "021b")
    imm20 = imm[0]
    imm19_12 = imm[1:9]
    imm11 = imm[9]
    imm10_1 = imm[10:20]
    return imm20 + imm10_1 + imm11 + imm19_12 + rd + opcode

manager_ARCH(sys.argv[1])