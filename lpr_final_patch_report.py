import re, sys


#If NAC is on the switch you will need to know the model number

# Use this online complier https://www.onlinegdb.com/online_python_compiler


def ask_y_or_n(question):
  while True:
    answer = input(question + " (Y/N): ").upper()
    if answer == "Y":
      return True
    elif answer == "N":
      return False
    else:
      print("Invalid answer. Please enter Y or N.")

def get_input():
    """Gets input from the user and saves it to a variable."""
    input_text = sys.stdin.read()
    return input_text


def save_input(input_text):
    """Saves the input text to a variable."""
    global user_input
    user_input = input_text


def main():
    """The main function."""
    input_text = get_input()
    save_input(input_text)
    # Convert the user_input into a list with each element a new line.
    lines = re.split("\n", input_text)
    return lines

if __name__ == "__main__":
    print('''\n

##############################################################################
        ############################################################

               DONT NOT paste in any password into the script. 
               
        ############################################################
##############################################################################

''')
    print('''\nThis script will assist with creating a CSV that can later be used to populate the data in Excel format to be used in the Spreadsheet for creating the cable labels.\n
            Use NetBrain to run the commands and paste in the output to this script. 
         ''')
    commands = ['show lldp neighbor','show int description | i nac-  ( Only if NAC is on the switch)']
    hostname = input("\nEnter the hostname of the switch: ")
    nac = ask_y_or_n('Is there a Forescout NAC connected to the switch? ')
    print('##############', nac)

    nacs = {'1':['FS-HW-5120, FS-HW-5140, FS-HW-5160', 'E2', 'E3'], '2':['FS-HW-5140, FS-HW-5160 10 Gig Sites', 'E4' , 'E5'],
            '3':['CT-4000 10G, CT-10000 10G', 'E4' , 'E5'], '4':['CT-2000', 'eth1', 'eth4'], '5':['CT-1000', 'eth1', 'eth2'],
            '6':['CT-100', 'eth2', 'eth4']}
    if nac:
        print('\nPossible NAC model numbers:')
        for number, model in nacs.items():
            print(f'Choice: {number} is {model[0]}')
        nac = ''
        while nac not in ('1', '2', '3', '4', '5', '6'):
            nac = input('Enter the model of the NAC: (1,2, etc) ')
            nac = str(nac)
        print(f'The model of the NAC is {nacs[nac][0]}')
    
    print('\nCommands to input on the Cisco switch:\n')
    for command in commands:
        print(command)    
    print("\nNext, Paste in the output from the 'show lldp neighbor' command from the Cisco switch: <press 'Enter' then 'ctrl + d' to continue after paste>") 
    lldp_text = main()
    if nac:
        print("\nFinally, Paste in the output from the 'show int description | i nac-' command from the Cisco switch: <press 'Enter' then 'ctrl + d' to continue after paste>") 
        nac_text = main()
    

    print('\nOnce the script is complete, paste in the output to a text file and save as a .CSV')
    print('Then, open the CSV and then paste that into the DATA tab on the labels spreadsheet\n')
    destination_hostnames = []
    source_interfaces = []
    destination_interfaces = []
    print('Hostname, Port, Cable Number Patchpannel Name, Room No, Rack Unit, Port Floor Tank Rumber, Hostname')
    for line in lldp_text:
        destination_hostname = re.findall('\w{3}\d{2}\-ap\-\d{1,3}\-\d{1,3}|\w{3}.+\.net|\w{5}\-\S+', line)
        #print(destination_hostname)
        if destination_hostname:
            destination_hostname = destination_hostname[0].replace('.net', '')
        source_interface = re.findall('Gi\S+|Te\S+|Fa\S+|Fi\S+|Twe\S+|Hu\S+', line)
        destination_interface = re.findall('\S+\n|\S+$', line)
        is_mac_address = re.findall('\w{4}\.\w{4}\.\w{4}', line)
        if destination_hostname:
            if is_mac_address:
                destination_interface = ['N/A']
            try:
                print(f'{hostname}, {source_interface[0]}, , , , , ,{destination_interface[0]}, {destination_hostname}')
            except:
                print(f'Error in line: {line}')

    if nac:
        print('Hostname, Port, Cable Number Patchpannel Name, Room No, Rack Unit, Port Floor Tank Rumber, Hostname')
        for line in nac_text:
            destination_hostname = re.findall('nac-.+', line)
            if destination_hostname:
                destination_hostname = destination_hostname[0].replace(' nac_excluded', '')
                source_interface = re.findall('Gi\S+|Te\S+|Fa\S+|Fi\S+|Twe\S+|Hu\S+', line)
                
                if 'nac-01-1-ilo' in line:
                    destination_interface = 'ilo'
                if 'nac-01-2-ilo' in line:
                    destination_interface = 'ilo' 
                if 'nac-01-1-mon1' in line:
                    destination_interface = nacs[nac][1]
                if 'nac-01-2-mon1' in line:
                    destination_interface = nacs[nac][2]
                if 'nac-01-1-mon2' in line:
                    destination_interface = nacs[nac][1]
                if 'nac-01-2-mon2' in line:
                    destination_interface = nacs[nac][2]
                if 'nac-01-1-mgmt' in line:
                    destination_interface = 'eth0'
                if 'nac-01-2-mgmt' in line:
                    destination_interface = 'eth0'
            
    
                try:
                    print(f'{hostname}, {source_interface[0]}, , , , , ,{destination_interface}, {destination_hostname}')
                except:
                    print(f'Error in line: {line}')

    pause = input('Hit any key to close...')
