
INST = {
    # (Type, Opcode, funct3, funct7)
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
    # I aritméticas
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


def manager(nombre, rd, rs1, rs2):

    # verificar si la instruccion existe
    if nombre not in INST:
        print("La instruccion no existe")
        return ""

    # tomar los valores de la instruccion
    datos = INST[nombre]
    tipo = datos[0]
    opcode = datos[1]
    funct3 = datos[2]
    funct7 = datos[3]

    bit_line = ""

    if tipo == "R":
        bit_line = assambler_R(funct7, rs2, rs1, funct3, rd, opcode)
        print(bit_line)
        return bit_line
    elif tipo == "I":
        if opcode == "1110111":
            if nombre == "ecall":
                imm = "000000000000"
                rs1 = "00000"
                rd = "00000"
                return bit_line = imm + format(rs1, "05b") + funct3 + format(rd, "05b") + opcode
            else:
                imm = "000000000001"
                rs1 = "00000"
                rd = "00000"
                return bit_line = imm + format(rs1, "05b") + funct3 + format(rd, "05b") + opcode
    else:
        bit_line = assambler_I(rs2, rs1, funct3, rd, opcode, funct7)



def assambler_R(funct7, rs2, rs1, funct3, rd, opcode):
    return funct7 + format(rs2, "05b") + format(rs1, "05b") + funct3 + format(rd, "05b")  + opcode

def assambler_I(rs2, rs1, funct3, rd, opcode, funct7 = None):
    
    if funct7 is None:
        imm = format(rs2, "012b")
        return imm + format(rs1, "05b") + funct3 + format(rd, "05b") + opcode
    else:
        imm = funct7 + format(rs2, "05b")
        return imm + format(rs1, "05b") + funct3 + format(rd, "05b") + opcode





