# fibonacci.asm

    addi t0, zero, 0    
    addi t1, zero, 1     
    addi t2, zero, 0     
    addi t3, zero, 8     
bucle:
    beq t3, zero, fin     
    sw t0, 0(t2)       
    add t4, t0, t1        
    add t0, t1, zero      
    add t1, t4, zero      
    addi t2, t2, 4        
    addi t3, t3, -1      
    jal zero, bucle       
fin:
    ebreak
