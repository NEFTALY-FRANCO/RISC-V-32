
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


def manager(nombre, rd=None, rs1=None, rs2=None,imm=None):

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
        bit_line = assembler_R(funct7, rs2, rs1, funct3, rd, opcode)
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
        bit_line = assembler_I(rs2, rs1, funct3, rd, opcode, funct7)
    if tipo == "S":
        imm_bin = format(imm, "012b")
        bit_line = (imm_bin,rs2, rs1, funct3, opcode)
    elif tipo == "B":
        imm_bin = format(imm, "012b")
        bit_line = assembler_B(imm_bin,rs2, rs1, funct3, opcode)
    elif tipo == "U":
        bit_line = assembler_U(imm,rd,opcode)
    elif tipo == "J":
        bit_line = assembler_J(imm, rd, opcode)


def assembler_R(funct7, rs2, rs1, funct3, rd, opcode):
    return funct7 + format(rs2, "05b") + format(rs1, "05b") + funct3 + format(rd, "05b")  + opcode

def assembler_I(rs2, rs1, funct3, rd, opcode, funct7 = None):
    
    if funct7 is None:
        imm = format(rs2, "012b")
        return imm + format(rs1, "05b") + funct3 + format(rd, "05b") + opcode
    else:
        imm = funct7 + format(rs2, "05b")
        return imm + format(rs1, "05b") + funct3 + format(rd, "05b") + opcode

def assembler_S(imm,rs2, rs1, funct3, opcode):
    imm_high = imm[:7]
    imm_low = imm[7:]
    return (imm_high + format(rs2, "05b") + format(rs1, "05b") + funct3 + imm_low + opcode)

def assembler_B(imm,rs2, rs1, funct3, opcode):
    imm12   = imm[0]
    imm10_5 = imm[1:7]
    imm4_1  = imm[7:11]
    imm11   = imm[11]
    return (imm12 + imm10_5 + rs2 + rs1 + funct3 + imm4_1 + imm11)

def assembler_U(imm, rd, opcode):
    return (format(imm, "020b") +format(rd, "05b") + opcode)

def assembler_J(imm, rd, opcode):
    imm20 = imm[0]
    imm10_1 = imm[10:20]
    imm11 = imm[9]
    imm19_12 = imm[1:9]
    
    return (imm20 + imm10_1 + imm11 + imm19_12 + format(rd, "05b") + opcode )
    