'''
Create a program that outputs a punnett table for the cross between two parent genes, and print out the
frequencies of daughter genes in order for the user to see which combination is most likely to be produced

Take in a certain number of traits per parent gene. Users should then be able to enter the genes
'alleles', 2 for each trait. A dominant allele is indicated with a captial and lowercase letter indicates a recessive.
Users can use any letter to represent a trait as long as it consists of two matching letter alleles and the letter isn't already
used as a representation of a trait. Parents don't need to have the same alleles, but traits must be the same and inputted in the same order.
Example: (AaBb and AABB) is a valid crossing but (AaBb and CcDD) isn't.

Seperate each parent gene into their respective 'gametes', which will be the horizontal axis (parent 1) and vertical axis (parent 2)
of the table. In order to get these gamete combinations, you can split the first trait into its two alleles (Ex. “AaBbCc” -> “A” and “a”)
then combine it with every other trait allele (Ex. ABC, ABc, Abc, AbC - each one is considered a gamete). 

Each row of the table should be the  respective squares gametes combined to create the final 'genotype'.
The dominant allele should usually be written first in the sequence, and alleles that code for the same 
gene should be grouped together. (Ex “ABC” x “ABC” = “AABBCC”).

Finally, output the punnett square in a visually pleasing table format, with parent 1’s gametes being labeled at the top row
and the first column being parent 2’s gametes. The table should be printed row by row with parent 1s gametes all being crossed 
with parent 2’s gametes to then produce their respective genotypes. A frequency list should also be outputted in descending order
of the most common genotype to least. 
'''

def instructions():
    # Reading a file in order to get the instructions
    try:
        with open('Instructions.txt', 'r') as file:
            instructions_content = file.read()
            return instructions_content
    # Catch filenotfounderror to indicate if the file Im reading from isn't found
    except FileNotFoundError:
        return "Instructions file not found."

def save_freq(frequencies):
    # Open file
    f = open("cps109_a1_output.txt", "a")
    # Writing all the frequencies found by the punnett square
    f.write("\n"+frequencies) # Write on a new line
    f.close()

def boarders(s, num):
    '''
    Function to add a boarder around a given text to make program more visually pleasing
    '''
    print('\t')
    print("="*num)
    print(s)
  
def parent_alleles(n):
    '''
    Takes in # of traits in a given gene and asks user to enter the allels (2/trait)
    Appends to a list in order to store all the allels of a parent gene, grouped by trait 
    '''
    parent = []
  
    for i in range(1, n+1):

        while True:
            trait = input("Trait "+ str(i)+":")
            # Checking if input is a string, not a repeat, has 2 alleles, and that letters match (Ex "Aa" not "Ab")
            if trait.isalpha() and trait not in parent and len(trait) == 2 and trait[0].lower()==trait[1].lower():
                parent.append(trait)
                # If valid, don't ask again
                break
            else:
                print("Invalid Input. Please make sure you have inputted a string with two alleles that code for one trait. Try again.")
    
    # Returns parent genes as a list
    return parent 

def get_gene_combinations(parent):
    '''
    Takes in a list of the parents traits and alleles
    Returns all the possible gametes of a parent based on their alleles. 
    Returns as a list in order to be used in future functions
    '''
    
    if len(parent) == 1: #If a parent only has one trait
        return [parent[0][0], parent[0][1]]
    else:
        combos = [""] # Initialize combinations list with an empty string for the first iteration.
        
        # Loop through each trait of the parent gene (e.g., ['Aa', 'Bb']).
        for gene in parent: 
            # Temporary list to store combinations for the current gene.
            temp = [] 
            
            # Loop through each existing combination in the result.
            for start_allele in combos:
                # After 1st iteration, combos will become the first trait (Ex 'AaBb's first will be 'Aa')
                # Loop through each allele in the current gene other than the start allele (Ex 'B' and 'b')
                for allele in gene: 
                # Concatenate the alleles by appending them to the start allele.
                # (Ex. A+B+C, a+B+c, A+B+c, A+b+C, A+b+c and a+B+C, a+B+c, a+b+C, a+b+c )
                    temp.append(start_allele + allele)
             # Concatenate the alleles by appending them to the start allele.
             # This generates all possible gamete combinations for the current gene.
            combos = temp
        return combos
    
def get_row(parent1_gametes, parent2_gametes):
    '''
    Takes in two lists as created by 'get_gamete_combos' for each parent
    
    Returns all possible genotypes of a cross between the second parents gamete
    and all the gametes of parent one. Function returns the final genotype with corresponding
    letters beside eachother (Ex. ABC x abc = AaBbCc)
    
    The final result should be a list of all the genotypes needed for the first row of 
    the punnett square crossed with the gametes of the coloumn (parent2)
    '''
    row = []
    
    # For every gamete in the list of all parent 1's gametes 
    for parent1_gamete in parent1_gametes:
        # Temp string that will store a combo, then reset for every iteration so we can append individual genotypes to row
        combined_genotype = ""
        
        # Using a range to acess the index's of p1's gamete since it is a string (Ex. 'ABC')
        for i in range(len(parent1_gamete)):
            # In order to concatinate matching alleles (Ex. A with a), match the index of p1 and p2
            # Note: this will only work if the user inputs the traits in the same order 
            if parent2_gametes[i].isupper(): 
                
                # Concatenate parent2's allele with parent1's allele in the gamete
                combined_genotype += parent2_gametes[i] + parent1_gamete[i]
            else:
                # If parent2's allele is lowercase (recessive), reverse concatenation order. 
                # This prioritizes dominant (indicated by captial letter) alleles
                combined_genotype += parent1_gamete[i]+ parent2_gametes[i]
                
        row.append(combined_genotype)

    return row
        
def print_punnett(row, column):
    '''
    Takes in two lists, row (all of parent1's gamete possibilities/the horizontal axis)
    and column (all of parent 2's gametes/vertical of the table)
    
    Function will print a punnett square table based on parent genes 
    Table will show all possible genotypes corresponding to what gametes are crossed
    '''
    
    # Length of the table 
    length = (((len(row[0])*2)+3)*len(column))+1 #(length of a gamete*2 (length of a genotype) + 3 (begining space))*# of coloumns 
    
    # Gap for the row to be printed 
    row_gap = len(column[0])+1
    print(row_gap*" ", end='')
    
    # Using a global variable, as this will be used by another function (save_freq)
    global all_genotypes
    all_genotypes = [] #List of all genotypes in the table (repeats included)
    
    # Printing the row axis 
    for gamete in row:
        print(" "*3+str(gamete)+len(gamete)*" ", end='') # End makes sure it is all printing on one line
    print('')
    
    # Printing the table row by row
    for i in range(0, len(row)):
        # Using 'get_row' function with p1s gametes, and only the [i] gamete of the coloumn 
        temp_row = get_row(row, column[i]) # Will reset after every row so each coloumn gamete is used
        print(" "*row_gap+"-"*length)
        
        # Printing the coloumn gamete that is being crossed with p1's gametes 
        print(str(column[i])+" |", end='')

        for genotype in temp_row: # Adding genotypes in our list for future functions
            all_genotypes.append(genotype)
            print(" "+str(genotype)+" |", end='')
        # Resetting so 'end' doesn't keep the string on the same line
        print('')
        
    print(" "*row_gap+"-"*length)
    
def genotype_freq(all_geno):
    '''
    Takes in list of all possible genotypes present in the final table
    Stores and prints the genotype (key) and the # of instances it shows up on the punnette square 
    in a dictonary
    Will also store these frequencies in a string in order for file writting 
    '''

    frequency_dict = {}
    freq = ""
    for geno in all_geno:
        # Increasing value matched with key for every time the genotype is already in the dictonary
        if geno in frequency_dict:
            frequency_dict[geno] += 1
        else: # Initalizing the keys
            frequency_dict[geno] = 1
  
    # Using built in function 'sorted' and its parameters to sort dictonary by greatest to least freq
    # The 'key' parameter is set to a lambda function that extracts the second element (index 1) of each tuple (the frequency) for sorting.
    # 'reverse=True' sorts the list in descending order, so the highest frequency come first.
    sorted_dict = sorted(frequency_dict.items(), key=lambda x:x[1], reverse=True)
    for item in sorted_dict:
        # Storing and printing final sorted dictonary of freqencies in order
        print(item[0]+": "+str(item[1]))
        freq += item[0]+": "+str(item[1])+", "

    return freq
                
#Main program function
def Main():
    num_traits = int(input("Please enter number of traits in cross: ")) # 'n' parameter for function 'parent_alleles'
    

    boarders("PARENT 1:", len("PARENT 1:")*3)
    parent1 = parent_alleles(num_traits)

    # Making sure user inputs the correct order so table can print properly
    while True:
        match = True
        boarders("PARENT 2:", len("PARENT 2:")*3)
        parent2 = parent_alleles(num_traits)
        #Checking each trait they entered and if it matches with the letters of p1
        for traits in range(len(parent2)):
            if num_traits>1 and parent2[traits].lower() != parent1[traits].lower():
                #If they don't, match is set to false so the loop will continue
                match = False
        if match == True: #If match is True (no changes found), escape loop
            break
        print("Please enter your respective traits in the same order as you did for parent 1!")
    
    #Getting gametes for each parent 
    combp1 = get_gene_combinations(parent1)
    combp2 = get_gene_combinations(parent2)
    
    boarders("PUNNETT SQUARE:", 32)

    print('\t')
    print_punnett(combp1, combp2)
    boarders("FREQUENCIES", len("FREQUENCIES")*3)
    # Saving frequencies to a variable for the writing a file function
    frequencies = genotype_freq(all_genotypes)
    
    # If user wants to save, write the frequencies to a file
    save = input("Would you like to save your frequencies? (Y or N): ")
    if save.lower() == 'y':
        save_freq(frequencies)
    else:
        print()
    
# Intro only printed once
intro = instructions()
print(intro)

# While loop to allow for user to create as many punnett square tables as they need
r = True
while r == True:
    again = True
    Main()
    # Iterates until user inputs a valid entry
    x = True
    while x == True:
        new = input("Would you like to make another? (Y or N): ")
        if new.lower() == 'y':
            x = False
        elif new.lower() == 'n':
            r = False
            x = False
        else: # If user doesnt, loop and ask again.
            print("Please enter Y or N")
    

    
    