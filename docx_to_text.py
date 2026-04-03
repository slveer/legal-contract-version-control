import random
import docx2txt 
import string

text = docx2txt.process("/Users/danielphillion/Library/Containers/com.apple.mail/Data/Library/Mail Downloads/493F5694-AD2A-4C27-AEBB-6A65007EB42E/Doc1.docx")

file_hash = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

with open(f"{file_hash}.txt", "w") as f:
    f.write(text)

