import prompt
import os, subprocess

want_number = prompt.string("Enter RDSH's number: ")
the_path = r'\\rdsh' + want_number + r'\C$\Users'
print(the_path)
subprocess.run(['explorer', os.path.realpath(the_path)])

    

      
