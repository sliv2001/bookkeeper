import os
import subprocess

for f in os.listdir('bookkeeper/view/'):
    if f.endswith('.ui'):
        subprocess.run(["pyside6-uic", 'bookkeeper/view/'+f,
                        '-o', 'bookkeeper/view/'+'Ui_'+f.removesuffix('.ui')+'.py'])
