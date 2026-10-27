# Ensamblador RISC-V (RV32I)

Programa en Python que lee un archivo con instrucciones RISC-V (por ejemplo `inst.asm`) y las convierte a código máquina en binario (32 bits por instrucción).

## Requisitos

- Python 3 instalado.

Para comprobarlo, abre una terminal y escribe:

```
python --version
```

En Linux o Mac puede que debas usar `python3` en lugar de `python`.

## Archivos

| Archivo | Descripción |
|---|---|
| `ensamblador.py` | El programa |
| `tu_archivo` | Tu archivo con las instrucciones (lo creas tú, con el nombre que quieras) |

Tu archivo puede llamarse como quieras y tener cualquier extensión (`inst.asm`, `programa.txt`, `prueba`, etc.). Lo más fácil es ponerlo en la **misma carpeta** que `ensamblador.py`; si está en otra, escribe la ruta completa.

## Cómo ejecutarlo

1. Abre una terminal (CMD o PowerShell en Windows, Terminal en Linux o Mac).
2. Ve a la carpeta donde están los archivos:

   ```
   cd ruta/de/tu/carpeta
   ```

3. Ejecuta el programa escribiendo el nombre de tu archivo de instrucciones:

   ```
   python ensamblador.py nombre_de_tu_archivo
   ```

   Por ejemplo: `python ensamblador.py inst.asm`, `python ensamblador.py programa.txt` o `python ensamblador.py C:\Users\tu_usuario\Documents\prueba.asm`.

El programa hace dos cosas:

1. Muestra en pantalla el resultado en binario (32 bits por instrucción).
2. Crea un archivo `.hex` con el mismo nombre que el de entrada, en la misma carpeta, con las instrucciones en hexadecimal.

   | Archivo de entrada | Archivo creado |
   |---|---|
   | `inst.asm` | `inst.hex` |
   | `programa.txt` | `programa.hex` |
   | `prueba` (sin extensión) | `prueba.hex` |

## Ejemplo

Archivo `inst.asm` (puede tener cualquier nombre):

```
addi x5, x0, 10
add  x6, x5, x5
ecall
```

Comando:

```
python ensamblador.py inst.asm
```

Salida en pantalla:

```
00000000101000000000001010010011
00000000010100101000001100110011
00000000000000000000000001110011
Archivo creado: inst.hex
```

Contenido del archivo `inst.hex` (una instrucción por línea, 8 dígitos hexadecimales):

```
00a00293
00528333
00000073
```

## Formato del archivo de instrucciones

- Una instrucción por línea.
- Los comentarios empiezan con `#`.
- Las etiquetas terminan con `:` y se pueden usar en saltos (`beq`, `bne`, `jal`, etc.).
- Los registros pueden escribirse como `x0`–`x31` o con su nombre (`zero`, `ra`, `sp`, `t0`, `a0`, `s1`, ...).
- Los números pueden ir en decimal (`10`, `-4`) o hexadecimal (`0x10`).
- Las instrucciones de memoria usan el formato `desplazamiento(registro)`, por ejemplo `lw x5, 8(sp)`.

Ejemplo completo:

```
inicio: addi x5, x0, 10     # x5 = 10
        add  x6, x5, x5     # x6 = x5 + x5
        lw   t0, 8(sp)      # carga desde memoria
        sw   t0, 12(sp)     # guarda en memoria
loop:   beq  x5, x6, fin    # salta a fin si son iguales
        jal  x1, loop       # salta a loop
fin:    lui  x7, 0x12345
        srai x5, x5, 3
        ecall
        ebreak
```

## Instrucciones soportadas

| Tipo | Instrucciones |
|---|---|
| R | `add` `sub` `xor` `or` `and` `sll` `srl` `sra` `slt` `sltu` |
| I | `addi` `xori` `ori` `andi` `slti` `sltiu` `slli` `srli` `srai` `lb` `lh` `lw` `lbu` `lhu` `jalr` `ecall` `ebreak` |
| S | `sb` `sh` `sw` |
| B | `beq` `bne` `blt` `bge` `bltu` `bgeu` |
| U | `lui` `auipc` |
| J | `jal` |

## Mensajes de error

| Mensaje | Causa |
|---|---|
| `Instrucción inválida: foo` | El nombre de la instrucción no existe |
| `Registro inválido: x99` | El registro no existe |
| `IndexError` | Faltan operandos en una instrucción |
| `FileNotFoundError` | El archivo no está en la carpeta o el nombre está mal escrito |
| `IndexError: list index out of range` en `sys.argv[1]` | Olvidaste escribir el nombre del archivo al ejecutar |

## Limitaciones

- No soporta pseudoinstrucciones (`li`, `mv`, `j`, `ret`, `nop`). Hay que escribir la instrucción real.
-El archivo de salida `.hex` ya existe, se sobrescribe.