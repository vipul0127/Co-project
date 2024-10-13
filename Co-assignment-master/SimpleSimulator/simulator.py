import sys
l=[]                
for line in sys.stdin:
    l.append(line.strip())
reg_index={'R0':1,'R1':2,'R2':3,'R3':4,'R4':5,'R5':6,'R6':7,'FLAGS':8}
pc_line=['00000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000','0000000000000000']
reg_value={'R0':0,'R1':0,'R2':0,'R3':0,'R4':0,'R5':0,'R6':0,'FLAGS':0}
reg_addr={'000':'R0','001':'R1','010':'R2','011':'R3','100':'R4','101':'R5','110':'R6','111':'FLAGS'}
cycle=0
l_memory=[] # IT IS A LIST WHICH REPRESENTS 256 LINES OF MEMORY

s='0000000000000000' # 16 BIT MEMORY
def decimalTobinary_8bits(n):
    n=int(n)
    no_bit=0
    n_bin=''
    while n>0:
        d=n%2
        n=n//2
        no_bit+=1
        n_bin+=str(d)
    n_bin=n_bin[-1::-1]
    no_bit=0
    zero_left=8-len(n_bin)
    n_bin=('0'*zero_left)+n_bin
    no_bit=1
    return n_bin

def decimalTobinary_16bits(n):
    n=int(n)
    no_bit=0
    n_bin=''
    while n>0:
        d=n%2
        n=n//2
        no_bit+=1
        n_bin+=str(d)
    n_bin=n_bin[-1::-1]
    no_bit=0
    zero_left=16-len(n_bin)
    n_bin=('0'*zero_left)+n_bin
    no_bit=1
    return n_bin

def binaryTodecimal(st):
    n_dec=0
    sl=0
    st=st[-1::-1]
    for i in range(0,len(st)):
        sl+=1
        a=int(st[i])
        if sl>1:
            sl+=1
        n_dec+=a*2**i
    return n_dec
  
def addition(line):
    flag=0
    no_var=1
    reg_value[reg_addr[line[6:]]]=reg_value[reg_addr[line[0:3]]]+reg_value[reg_addr[line[3:6]]]

    # CHECKING FOR OVERFLOW AND UNDERFLOW (V=1)
    if flag==0:
        reg_value['FLAGS']=0
        var+=1
        pc_line[reg_index['FLAGS']]='0000000000000000'
    if reg_value[reg_addr[line[6:]]]<(2**16) and reg_value[reg_addr[line[6:]]]>=0:
        no_var+=1
        pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])

    else:
        flag=1
        if var<1:
            flag=0
        if reg_value[reg_addr[line[6:]]]>=(2**16): # OVERFLOW
            no_var=1
            reg_value[reg_addr[line[6:]]]=(reg_value[reg_addr[line[6:]]])%(2**16)
            
            pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
            var+=1
            reg_value['FLAGS']=8 # SETTING 'V' BIT = 1
            pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])
            var+=1

        else: # UNDERFLOW
            reg_value[reg_addr[line[6:]]]=0
            if var<1:
                flag=0
            pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
            var+=1
            reg_value['FLAGS']=8 # SETTING V BIT = 1
            var=var-1
            pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])

def subtraction(line):
    flag=0
    
    reg_value[reg_addr[line[6:]]]=reg_value[reg_addr[line[0:3]]]-reg_value[reg_addr[line[3:6]]]
    no_of_op=4

    # CHECKING FOR OVERFLOW AND UNDERFLOW (V=1)
    if flag==0:
        reg_value['FLAGS']=0
        pc_line[reg_index['FLAGS']]='0000000000000000'
    if reg_value[reg_addr[line[6:]]]<(2**16) and reg_value[reg_addr[line[6:]]]>=0:
        var+=1
        pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])

    else:
        flag=1
        no_of_op+=1
        if reg_value[reg_addr[line[6:]]]>=(2**16): # OVERFLOW
            var+1
            reg_value[reg_addr[line[6:]]]=(reg_value[reg_addr[line[6:]]])%(2**16)
            no_of_op+=1
            pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
            reg_value['FLAGS']=8 # SETTING 'V' BIT = 1
            no_of_op-=1
            pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])

        else: # UNDERFLOW
            no_of_op+=1
            reg_value[reg_addr[line[6:]]]=0
            var=0
            pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
            if no_of_op>1:
                var+=1
            pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])
            reg_value['FLAGS']=8 # SETTING V BIT = 1
            no_of_op+=1

def multiplication(line):
    flag=0
    no_of_op=4

    reg_value[reg_addr[line[6:]]]=reg_value[reg_addr[line[0:3]]]*reg_value[reg_addr[line[3:6]]]
    var=0
    # CHECKING FOR OVERFLOW AND UNDERFLOW (V=1)
    if flag==0:
        reg_value['FLAGS']=0
        pc_line[reg_index['FLAGS']]='0000000000000000'
    if reg_value[reg_addr[line[6:]]]<(2**16) and reg_value[reg_addr[line[6:]]]>=0:
        var+=1
        pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
        no_of_op+=1

    else:
        flag=1
        var1=4
        if reg_value[reg_addr[line[6:]]]>=(2**16): # OVERFLOW
            print(reg_value[reg_addr[line[6:]]])
            if no_of_op>1:
                var+=1
            reg_value[reg_addr[line[6:]]]=(reg_value[reg_addr[line[6:]]])%(65536)
            no_of_op=1
            print(reg_value[reg_addr[line[6:]]])
            var1+=1
            pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
            reg_value['FLAGS']=8 # SETTING 'V' BIT = 1
            if no_of_op>1:
                var+=1
            pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])

        else: # UNDERFLOW
            reg_value[reg_addr[line[6:]]]=0
            no_of_op+=1
            pc_line[reg_index[reg_addr[line[6:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[6:]]])
            var1=0
            reg_value['FLAGS']=8 # SETTING V BIT = 1
            if no_of_op>1:
                var+=1
            pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])

def move_immediate(line):
    no_of_op=0
    var1=0
    reg_value[reg_addr[line[0:3]]]=binaryTodecimal(line[3:])
    if no_of_op>1:
                var1+=1
    pc_line[reg_index[reg_addr[line[0:3]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[0:3]]])
    reg_value['FLAGS']=0
    var1=0
    pc_line[reg_index['FLAGS']]='0000000000000000'

def move_register(line): # mov r1 r2 we give r2 = r1
    no_of_op=0
    reg_value[reg_addr[line[3:]]]=reg_value[reg_addr[line[0:3]]]
    var1=0
    pc_line[reg_index[reg_addr[line[3:]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[3:]]])
    var1+=1
    reg_value['FLAGS']=0
    if no_of_op>1:
                var1+=1
    pc_line[reg_index['FLAGS']]='0000000000000000'

def load(line):
    no_of_op=0
    index=binaryTodecimal(line[3:]) # mem_addr is index of the var in the memory list
    var1=0
    reg_value[reg_addr[line[0:3]]]=binaryTodecimal(l_memory[index]) # the value at that index is to be stored in register
    
    no_of_op=0
    pc_line[reg_index[reg_addr[line[0:3]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[0:3]]])

    if no_of_op>1:
                var1+=1
    reg_value['FLAGS']=0
    var1=1
    pc_line[reg_index['FLAGS']]='0000000000000000'

def store(line):
    value_var=reg_value[reg_addr[line[0:3]]] # extract the value of register
    var1=0
    index=binaryTodecimal(line[3:]) # mem_addr is index of the var in the memory list
    if no_of_op>1:
                var1+=1
    no_of_op=0
    l_memory[index]=decimalTobinary_16bits(value_var) # store the value at the index pointed by mem_addr
    reg_value['FLAGS']=0
    pc_line[reg_index['FLAGS']]='0000000000000000'
    no_of_op+=1
   
def divide(line): # div r3 r4 means R0=quo(r3/r4) and R1=rem(r3/r4)
    no_of_op=0
    reg_value['R0']=int((reg_value[reg_addr[line[0:3]]])/(reg_value[reg_addr[line[3:]]]))
    var1=0
    reg_value['R1']=reg_value[reg_addr[line[0:3]]]-(reg_value['R0']*(reg_value[reg_addr[line[3:]]]))
    if no_of_op>1:
                var1+=1
    pc_line[reg_index['R0']]=decimalTobinary_16bits(reg_value['R0'])
    var1=1
    pc_line[reg_index['R1']]=decimalTobinary_16bits(reg_value['R1'])
    no_of_op=1
    reg_value['FLAGS']=0   

    pc_line[reg_index['FLAGS']]='0000000000000000'
    
def compare(line):
    no_of_op=0
    val_1=reg_value[reg_addr[line[0:3]]]
    var1=0
    val_2=reg_value[reg_addr[line[3:]]]
    if val_1>val_2:
        var1=1
        reg_value['FLAGS']=2
        if no_of_op>1:
                var1+=1
    elif val_1<val_2:
        no_of_op=0

        reg_value['FLAGS']=4
    else:
        reg_value['FLAGS']=1
        if no_of_op>1:
                var1+=1
    pc_line[reg_index['FLAGS']]=decimalTobinary_16bits(reg_value['FLAGS'])
    var1+=1

def unconditional_jump(line):
    no_of_op=0
    index=binaryTodecimal(line[0:])
    var1=0
    pc_line[0]=decimalTobinary_8bits(i)
    no_of_op=2
    reg_value['FLAGS']=0
    if no_of_op>1:
                var1+=1
    pc_line[reg_index['FLAGS']]='0000000000000000'
    var+=1
    return index

def less_than_jump(line):
    no_of_op=4
    index=binaryTodecimal(line[0:])
    var1=0
    if no_of_op>1:
                var1+=1
    if reg_value['FLAGS']==4:
        no_of_op=0
        pc_line[0]=decimalTobinary_8bits(i)
        var1=1
        reg_value['FLAGS']=0
        if no_of_op>1:
                var1+=1
        pc_line[reg_index['FLAGS']]='0000000000000000'
    
        return index
    else:
        reg_value['FLAGS']=0
        var1+=1
        pc_line[reg_index['FLAGS']]='0000000000000000'
        return -1

def greater_than_jump(line):
    no_of_op=0
    index=binaryTodecimal(line[0:])
    var1=0
    if no_of_op>1:
                var1+=1
    if reg_value['FLAGS']==2:
        pc_line[0]=decimalTobinary_8bits(i)
        var1+=1
        reg_value['FLAGS']=0
        if no_of_op>1:
                var1+=1
        pc_line[reg_index['FLAGS']]='0000000000000000'
        no_of_op=2
        return index
    else:
        reg_value['FLAGS']=0
        no_of_op=2
        pc_line[reg_index['FLAGS']]='0000000000000000'
        var+=1
        return -1

def equal_jump(line):
    no_of_op=0
    
    index=binaryTodecimal(line[0:])
    var1=0
    if reg_value['FLAGS']==1:
        no_of_op=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op>1:
                var1+=1
        reg_value['FLAGS']=0
        var1+=1
        pc_line[reg_index['FLAGS']]='0000000000000000'
        
        return index
    else:
        reg_value['FLAGS']=0
        no_of_op=0
        pc_line[reg_index['FLAGS']]='0000000000000000'
        var1=1
        return -1

def right_shift(line):
    no_of_op=0
    imm_shift=binaryTodecimal(line[3:])
    var1=0
    reg_value[reg_addr[line[0:3]]]/=(2**imm_shift)
    pc_line[reg_index[reg_addr[line[0:3]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[0:3]]])
    no_of_op+=1
    reg_value['FLAGS']=0
    if no_of_op>1:
                var1+=1
    pc_line[reg_index['FLAGS']]='0000000000000000'
    var=2

def left_shift(line):
    no_of_op=0
    imm_shift=binaryTodecimal(line[3:])
    var1=0
    reg_value[reg_addr[line[0:3]]]*=(2**imm_shift)
    if no_of_op>1:
                var1+=1
    pc_line[reg_index[reg_addr[line[0:3]]]]=decimalTobinary_16bits(reg_value[reg_addr[line[0:3]]])
    no_of_op=1
    reg_value['FLAGS']=0
    pc_line[reg_index['FLAGS']]='0000000000000000'

def exclusive_xor(line):
    no_of_op=0
    s=''
    s_1=pc_line[reg_index[reg_addr[line[0:3]]]]
    var1=0
    s_2=pc_line[reg_index[reg_addr[line[3:6]]]]
    for i in range(len(s_1)):
        s+=str(int(s_1[i])^int(s_2[i]))
        if no_of_op>1:
                var1+=1
    pc_line[reg_index[reg_addr[line[6:]]]]=s
    no_of_op+=1
    reg_value[reg_addr[line[6:]]]=binaryTodecimal(s)
    reg_value['FLAGS']=0
    if no_of_op>1:
                var1+=1
    pc_line[reg_index['FLAGS']]='0000000000000000'

def or_operation(line):
    s=''
    no_of_op=0
    s_1=pc_line[reg_index[reg_addr[line[0:3]]]]
    var1=0
    s_2=pc_line[reg_index[reg_addr[line[3:6]]]]
    for i in range(len(s_1)):
        no_of_op=1
        s+=str(int(s_1[i])|int(s_2[i]))
        if no_of_op>1:
                var1+=1
    pc_line[reg_index[reg_addr[line[6:]]]]=s
    var=1
    reg_value[reg_addr[line[6:]]]=binaryTodecimal(s)
    reg_value['FLAGS']=0
    if no_of_op>1:
                var1+=1
    else:
        var=0
    pc_line[reg_index['FLAGS']]='0000000000000000'

def and_operation(line):
    total_variable=0
    total_counter=0
    s=''
    s_1=pc_line[reg_index[reg_addr[line[0:3]]]]
    if total_variable==0:
        total_counter+=1
    s_2=pc_line[reg_index[reg_addr[line[3:6]]]]
    for i in range(len(s_1)):
        if total_variable==0:
            total_counter+=1
        s+=str(int(s_1[i])&int(s_2[i]))
    total_variable+=1
    pc_line[reg_index[reg_addr[line[6:]]]]=s
    total_counter+=1
    reg_value[reg_addr[line[6:]]]=binaryTodecimal(s)
    total_variable=0
    reg_value['FLAGS']=0
    pc_line[reg_index['FLAGS']]='0000000000000000'
    total_counter=0

def not_operation(line):
    s=''
    no_of_op=0
    s_1=pc_line[reg_index[reg_addr[line[0:3]]]]
    var1=0
    for i in range(len(s_1)):
        s+=str(int(not int(s_1[i])))
        if no_of_op>1:
                var1+=1
        else:
            var=0
    pc_line[reg_index[reg_addr[line[3:]]]]=s
    no_of_op+=1
    reg_value[reg_addr[line[3:]]]=binaryTodecimal(s)
    reg_value['FLAGS']=0
    var1=1

    pc_line[reg_index['FLAGS']]='0000000000000000'

for j in range(128):
    if j<len(l):
        l_memory.append(l[j])
    else:
        l_memory.append(s)
 
while(i<len(l)):
    opcode=l[i][0:5] # EXTRACTING OPCODE AND THEN PERFORMING THE OPERATION
    no_op=1
    var1=0
    if(opcode=='00000'):
        no_op+=1
        addition(l[i][7:]) # 0 1 2 3 4 for opcode and 5 6 unused
        if no_op>1:
                var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        var1+=1
        print(*pc_line)
        i+=1
    elif opcode=='00001':
        no_op+=1
        subtraction(l[i][7:]) # 0 1 2 3 4 for opcode and 5 6 unused
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='00110':
        no_op+=1
        multiplication(l[i][7:]) # 0 1 2 3 4 for opcode and 5 6 unused
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1
        
    elif opcode=='00010':
        no_op+=1
        move_immediate(l[i][5:]) # 0 1 2 3 4 for opcode
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='00011':
        no_op+=1
        move_register(l[i][10:]) # 0 1 2 3 4 for opcode and 5 6 7 8 9 unused
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='00100':
        no_op+=1
        load(l[i][5:]) # 0 1 2 3 4 for opcode ; 5 6 7 reg addr; 8 - 15 mem_addr (TYPE D)
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='00101':
        no_op+=1
        store(l[i][5:]) # type D
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='00111':
        no_op+=1
        divide(l[i][10:]) # type C
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='01000':
        no_op+=1
        right_shift(l[i][5:]) # type B
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='01001':
        no_op+=1
        left_shift(l[i][5:]) # type B
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        
        print(*pc_line)
        i+=1

    elif opcode=='01010':
        no_op+=1

        
        exclusive_xor(l[i][7:]) # type A
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='01011':
        no_op+=1
        or_operation(l[i][7:]) # type A
        if no_of_op==1:
            var1+=1
        else:
            var=0
        pc_line[0]=decimalTobinary_8bits(i)
        var1+=1
        print(*pc_line)
        i+=1

    elif opcode=='01100':
        no_op+=1
        and_operation(l[i][7:]) # type A
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='01101':
        no_op+=1
        not_operation(l[i][10:]) # type C
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='01110':
        no_op+=1
        compare(l[i][10:]) # type c
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        print(*pc_line)
        i+=1

    elif opcode=='01111':
        no_op+=1
        pc_line[0]=decimalTobinary_8bits(i)
        var1+=1
        print(*pc_line)
        if no_of_op==1:
            var1+=1
        else:
            var=0
        i=unconditional_jump(l[i][8:]) #type E

    elif opcode=='11100':
        no_op+=1
        i_shift=less_than_jump(l[i][8:]) #type E
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if i_shift==-1:
            i+=1
            var1+=1
        else:
            i=i_shift
            var=0
        print(*pc_line)
        

    elif opcode=='11101':
        no_op+=1
        i_shift=greater_than_jump(l[i][8:]) #type E
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if i_shift==-1:
            i+=1
            var1+=1
        else:
            i=i_shift
        print(*pc_line)

    elif opcode=='11111':
        no_op+=1
        i_shift=equal_jump(l[i][8:]) #type E
        var1+=1
        pc_line[0]=decimalTobinary_8bits(i)
        if i_shift==-1:
            i+=1
        else:
            i=i_shift
        print(*pc_line)

    elif opcode=='11010':
        no_op+=1
        reg_value['FLAGS']=0
        var1+=1
        pc_line[reg_index['FLAGS']]='0000000000000000'
        if no_of_op==1:
            var1+=1
        else:
            var=0
        pc_line[0]=decimalTobinary_8bits(i)
        print(*pc_line)
        break
    cycle+=1
for i in l_memory:
    print(i)

