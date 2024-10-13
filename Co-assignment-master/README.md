group member name 


ROLL NO      NAME                      GMAIL  


2022418      Roshan kumar mahto        roshan22418@iiitd.ac.in


202234       nootan sharma             nootan22340@iiitd.acin


2022576      vipul                     vipul22576@iiitd.ac.in


2022463      satyam panday             satyam22463@iiitd.ac.in



The code defines several dictionaries for opcodes, registers, labels, and variable names. It also initializes empty lists to store errors and the generated machine code.

The labeler() function scans the main file and extracts labels, storing them in the labels dictionary with their corresponding line numbers.

The variable() function scans the main file for variable declarations and stores them in the labeldic dictionary with their corresponding variable names.

The errordetection() function is responsible for detecting errors in each line of the program. It checks the syntax and validity of instructions, registers, variables, and labels. If any error is found, it appends the error message to the errorlist list.

The d2b() function converts a decimal number to a binary number of 7 bits.

The assembler() function processes each instruction of the main file, generates the machine code based on the opcode and operands, and appends it to the outputlist.

The main() function is the entry point of the program. It reads the main file, calls the labeler() and variable() functions to set up labels and variables, performs error detection, and finally generates the machine code or prints the error messages if any.

Overall, the code takes an assembly-like input file, performs label and variable processing, performs error detection, and generates the corresponding machine code as output.





Regenerate respons
