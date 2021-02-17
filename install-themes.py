import subprocess
from halo import Halo

def run(cmd):
    return subprocess.run(cmd, shell=True,  text=True, check=True, stdout=subprocess.PIPE).stdout

spinner = Halo(text='Cloning repo', spinner='dots') 
spinner.start()
run('git clone --quiet git@github.com:mbadolato/iTerm2-Color-Schemes.git > /dev/null')
spinner.succeed()
spinner.start('Importing color schemes')
run('iTerm2-Color-Schemes/tools/import-scheme.sh iTerm2-Color-Schemes/schemes/*')
spinner.succeed()
spinner.start('Removing git folder')
run('rm -rf ./iTerm2-Color-Schemes')
spinner.succeed()

spinner.start()
spinner.succeed('Done')
