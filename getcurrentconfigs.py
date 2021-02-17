import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True,  text=True, check=True, stdout=subprocess.PIPE).stdout

if __name__ == '__main__':
    config_dir = '$HOME/.config/nvim'
    run(f'cp {config_dir}/* .')
    print('Done')
