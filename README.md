# Ensamblador RISC-V (RV32I)

Programa en Python 3 que lee un archivo de ensamblador RV32I y escribe un archivo de texto con una palabra de 32 bits por línea, en hexadecimal de 8 dígitos. Ese archivo se puede cargar en una memoria de instrucciones descrita en Verilog con `$readmemh`.

No hace falta instalar librerías. Solo se usa la biblioteca estándar de Python. No hay `requirements.txt`.

## Cómo ejecutarlo desde la terminal

1. Comprueba que Python 3 está instalado:

```
python --version
```

En algunos equipos el comando es `python3`.

2. Abre PowerShell o CMD y entra a la carpeta del proyecto (ajusta la ruta si la tuya es distinta):

```
cd "C:\Users\nefta\Downloads\lading-page 5\RISC-V-32"
```

3. Ejecuta el programa con el archivo de entrada. El único argumento es ese archivo:

```
python enssambler.py prueva\sum_n.asm
```

El programa:

- imprime en la terminal los 32 bits de cada instrucción;
- crea un `.hex` con el mismo nombre y en la misma carpeta que la entrada.

| Entrada | Salida |
|---|---|
| `prueva\sum_n.asm` | `prueva\sum_n.hex` |
| `programa.asm` | `programa.hex` |
| `notas.txt` | `notas.hex` |

Si el archivo de salida ya existe, se sobrescribe.

Ejemplo con `prueva\sum_n.asm`. La terminal muestra el binario y al final `Archivo creado: prueva\sum_n.hex`. El archivo queda así:

```
00500513
00000293
00050863
00a282b3
fff50513
ff5ff06f
00100073
```

La primera línea es la dirección `0x00000000`, la segunda `0x00000004`, y así sucesivamente. No lleva prefijo `0x` ni espacios.

## Cómo está organizado el código

Todo vive en `enssambler.py`. Hay tres partes.

**Tablas.** `REGISTROS` traduce cada registro (`x0`–`x31` y los nombres ABI: `zero`, `ra`, `sp`, `gp`, `tp`, `fp`, `t0`–`t6`, `s0`–`s11`, `a0`–`a7`) a 5 bits. `INST` asocia cada mnemónico con su formato (`R`, `I`, `S`, `B`, `U` o `J`), el opcode, el funct3 y, cuando aplica, el funct7. Esas cadenas son las que después se concatenan para formar la instrucción.

**Dos pasadas, en `manager_ARCH`.** La primera recorre el archivo solo para anotar etiquetas. La segunda vuelve a leerlo, codifica cada instrucción y escribe el `.hex`.

**Codificación, en `manager` y `assembler_R`, `assembler_I`, `assembler_S`, `assembler_B`, `assembler_U`, `assembler_J`.** `manager` comprueba que el mnemónico y los registros existan y llama a la función del formato. Cada función arma una cadena de 32 caracteres `'0'` y `'1'` en el orden de campos de RV32I. Al final `format(..., "08x")` la pasa a hexadecimal.

## Cómo se representa una instrucción

Una instrucción es la concatenación de sus campos, del bit 31 al bit 0:

| Formato | Orden de los campos |
|---|---|
| R | funct7, rs2, rs1, funct3, rd, opcode |
| I | inmediato de 12 bits (o funct7 + shamt de 5 bits en `slli`, `srli` y `srai`), rs1, funct3, rd, opcode |
| S | imm[11:5], rs2, rs1, funct3, imm[4:0], opcode |
| B | imm[12], imm[10:5], rs2, rs1, funct3, imm[4:1], imm[11], opcode |
| U | inmediato de 20 bits, rd, opcode |
| J | imm[20], imm[10:1], imm[11], imm[19:12], rd, opcode |

`ecall` y `ebreak` no llevan operandos. Su inmediato es 0 y 1, respectivamente, y el resto de los campos de registro van en cero.

En `lui` y `auipc` el número que escribes ya son los 20 bits altos (`lui t0, 0x12345`), no un valor de 32 bits al que haya que desplazarlo.

En los saltos (`beq`, `jal`, etc.) el desplazamiento es la distancia en bytes desde la propia instrucción hasta el destino. El bit 0 de esa distancia no se guarda, porque el destino siempre es par.

## Cómo se resuelven las etiquetas

En la primera pasada el contador de programa empieza en 0. Se ignoran líneas vacías y todo lo que va después de `#`. Si la línea tiene `:`, el nombre de la izquierda se guarda con la dirección actual. Una etiqueta sola no avanza el contador. Cada instrucción real suma 4.

En la segunda pasada, si el destino de una instrucción B o J está en esa tabla, el inmediato es `dirección de la etiqueta − PC de la instrucción`. Si no está, el programa intenta leer el operando como número (`10`, `0x10`, `0b1010`).

Ejemplo: un `beq` en `0x08` hacia una etiqueta en `0x18` usa desplazamiento +16. Un `jal` en `0x14` hacia una etiqueta en `0x08` usa desplazamiento −12.

## Qué acepta el archivo de entrada

- Una instrucción por línea. Las líneas vacías se ignoran.
- Los comentarios empiezan con `#` y llegan hasta el final de la línea.
- Una etiqueta es un nombre seguido de `:`. Puede ir sola o delante de la instrucción en la misma línea.
- Los operandos se separan con comas. Los espacios de más no importan.
- Registros por número (`x0`–`x31`) o por nombre ABI.
- Inmediatos en decimal (`-12`, `42`), hexadecimal (`0xFF`) o binario (`0b1010`).
- Cargas y almacenamientos en la forma `desplazamiento(registro)`, por ejemplo `lw t0, 8(sp)`. Si en una carga se omite el desplazamiento, se usa 0.
- En bifurcaciones y en `jal`, el destino puede ser una etiqueta.

Ejemplo:

```
inicio: addi x5, x0, 10     # x5 = 10
        add  x6, x5, x5
        lw   t0, 8(sp)
        sw   t0, 12(sp)
loop:   beq  x5, x6, fin
        jal  x1, loop
fin:    lui  x7, 0x12345
        srai x5, x5, 3
        ecall
        ebreak
```

## Instrucciones que codifica

| Formato | Instrucciones |
|---|---|
| R | `add` `sub` `sll` `slt` `sltu` `xor` `srl` `sra` `or` `and` |
| I | `addi` `slti` `sltiu` `xori` `ori` `andi` `slli` `srli` `srai` `lb` `lh` `lw` `lbu` `lhu` `jalr` `ecall` `ebreak` |
| S | `sb` `sh` `sw` |
| B | `beq` `bne` `blt` `bge` `bltu` `bgeu` |
| U | `lui` `auipc` |
| J | `jal` |

`fence` no forma parte del conjunto pedido y no está incluida.

## Por qué `li`, `la` y `call` ocupan dos instrucciones

Un inmediato de las instrucciones tipo I solo tiene 12 bits. Con signo, eso alcanza de −2048 a 2047. Un valor cualquiera de 32 bits, o una dirección lejana, no cabe ahí.

Por eso la primera instrucción coloca los 20 bits altos (`lui` en `li`, `auipc` en `la` y `call`) y la segunda suma los 12 bits bajos. `auipc` suma esos 20 bits al PC, así que el par `auipc` + `addi` (o `jalr`, o una carga) puede alcanzar cualquier dirección relativa al punto del programa donde está el `auipc`.

La segunda instrucción extiende el signo de su inmediato de 12 bits. Si el bit 11 de la parte baja es 1, ese inmediato es negativo y la suma restaría 4096 de más. Para compensarlo se calcula la parte alta así:

```
hi = (v + 0x800) >> 12
lo = v - (hi << 12)
```

Sumar `0x800` (2048) redondea hacia arriba justo cuando la parte baja sería negativa. Así `lo` queda entre −2048 y 2047, que es lo que cabe en 12 bits con signo. Por ejemplo, `0x12345FFF` se parte en `hi = 0x12346` y `lo = -1`: `lui` deja un valor una unidad por encima y el `addi` de −1 lo corrige.

`la` y `call` siempre salen como dos instrucciones, porque la distancia al símbolo depende de dónde quedó el `auipc`. `li` usa una sola instrucción cuando el número ya cabe en 12 bits con signo, o cuando la parte baja es 0 (basta el `lui`).

Esta versión del programa no expande esas pseudoinstrucciones: hay que escribir las instrucciones base ya expandidas (`addi`, `lui`, `auipc`, `jal`, `jalr`, etc.).

## Errores que detecta

| Mensaje | Causa |
|---|---|
| `Instrucción inválida: ...` | El mnemónico no está en la tabla |
| `Registro inválido: ...` | El registro no existe (`x32`, `t7`, …) |
| `La instruccion no existe` | El nombre no está en `INST` al codificar |

Si el archivo no existe, Python lanza `FileNotFoundError`. Si faltan operandos, lanza `IndexError`. Si falta el argumento en la terminal (`python enssambler.py` sin archivo), también lanza `IndexError` al leer `sys.argv[1]`.

Ante una instrucción o un registro inválido el programa deja de traducir. El código de salida en ese caso es 0, y el `.hex` puede haber quedado creado a medias.
