import subprocess
import sys
import getpass
import os.path

try:
    from halo import Halo
except ModuleNotFoundError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'halo'], stdout=subprocess.DEVNULL)

from shutil import which

user = os.path.expanduser('~') 
spinner = Halo(text='loading', spinner='dots')

def run(cmd):
    return subprocess.run(cmd, shell=True,  text=True, check=True, stdout=subprocess.PIPE).stdout

def run_err(cmd):
    return subprocess.run(cmd, shell=True,  text=True, check=True, stderr=subprocess.PIPE).stderr

def spin_fail(name):
    spinner.fail(f'There was an error installing {name}, please try to install manually')

def program_installed(name, display_name, on_not_installed):
    spinner.start(f'Checking if {display_name} is installed')
    if which(name) is not None:
        spinner.succeed(f'{display_name} is installed')
    else:
        spinner.stop()
        on_not_installed()

def install_npm_pkg(name):
    run(f'npm install -g {name}')

def npm_pkg_installed(name, display_name, fail_on_err=False):
    spinner.start(f'Checking if {display_name} is installed')
    pkg_list = run(f'npm list -g {name}')
    if name in pkg_list:
        spinner.succeed(f'{display_name} is installed')
    elif not fail_on_err:
        spinner.text = f'{display_name} not installed: Installing...'
        install_npm_pkg(name)
        npm_pkg_installed(name, display_name, True)
    else:
        spin_fail(display_name)

def brew_fail():
    spin_fail('Homebrew')

def install_brew():
    pwd = getpass.getpass()
    spinner.start('Homebrew not installed: Installing...')
    run(f'export CI=1 && echo {pwd} | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"')
    spinner.stop()
    program_installed('brew', 'Homebrew', brew_fail)

def nvim_fail():
    spin_fail('Neovim')

def install_nvim():
    spinner.start('Nvim not installed: Installing...')
    run('brew install neovim')
    spinner.stop()
    program_installed('nvim', 'Neovim', nvim_fail)

def update_nvim(error_on_fail=False):
    spinner.start('Updating Nvim')
    message = 'is already installed and up-to-date'
    not_linked = 'it\'s just not linked'
    nvim_install = run_err('brew install --HEAD neovim')
    luajit_install = run_err('brew install --HEAD luajit') 
    run('brew install luarocks')
    run('brew install luv')
    nvim_installed = message in nvim_install 
    luajit_installed = message in luajit_install 
    nvim_unlinked = not_linked in nvim_install
    luajit_unlinked = not_linked in luajit_install
    if nvim_unlinked:
        run('brew link neovim')
        update_nvim()
        return
    if luajit_unlinked: 
        run('brew link luajit')
        update_nvim()
        return
    if nvim_installed and luajit_installed: 
        spinner.succeed('Nvim up to date')
        return
    elif error_on_fail:
        spin_fail('Nvim update')
        return

    if not luajit_installed:
        run('brew unlink luajit && brew install --HEAD luajit')
    if not nvim_installed:
        run('brew unlink neovim && brew install --HEAD neovim')
    spinner.stop()
    update_nvim(True)


def add_configs():
    config_dir = '$HOME/.config.nvim/'
    spinner.start('Adding nvim configs')
    run(f'mkdir -p {config_dir}')
    run(f'cp ./init.vim {config_dir}')
    run(f'cp ./coc-settings.json {config_dir}')
    spinner.succeed('Added nvim configs')

def install_plug(stop_on_fail=False):
    spinner.start('Checking if plug is installed')
    plug_file = f'{user}/.local/share/nvim/site/autoload/plug.vim'
    if os.path.isfile(plug_file):
        spinner.succeed('Plug is installed')
    elif not stop_on_fail:
        spinner.text = 'Plug not installed: Installing...'
        run('sh -c \'curl -fsSLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim\'')
        install_plug(True)
    else:
        spinner.fail('Could not install Plug, please try to install manually')

def install_plug_plugins():
    spinner.start('Installing nvim plugins')
    run('nvim --headless +PlugInstall +qa')
    spinner.succeed('Nvim plugins installed')

def install_nvim_language_plugins():
    spinner.start('Installing nvim python plugin')
    run('pip3 install pynvim')
    spinner.succeed('Installed nvim python plugin')
    npm_pkg_installed('neovim', 'neovim package')

def nvm_fail():
    spin_fail('nvm')

def install_nvm():
    spinner.start('nvm not installed: Installing...')
    run(f'/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh)"')
    spinner.stop()
    program_installed('nvm','nvm',nvm_fail)

def install_iterm(error_on_fail=False):
    spinner.start('Checking if iterm is installed')
    if os.path.exists('/Applications/iTerm.app'):
        spinner.succeed('iTerm is installed')
    elif not error_on_fail:
        spinner.text = 'iTerm not installed: Installing...'
        run('brew cask install iterm2')
        spinner.stop()
        install_iterm(True)
    else:
        spin_fail('iTerm')

def zsh_fail():
    spin_fail('zsh')

def install_zsh():
    spinner.start('zsh not installed: Installing...')
    run('brew install zsh')
    spinner.stop()
    program_installed('zsh', 'zsh', zsh_fail)

def install_ohmyzsh(error_on_fail=False):
    spinner.start('Checking if oh-my-zsh is installed')
    if os.path.exists(f'{user}/.oh-my-zsh'):
        spinner.succeed('Oh my zsh is installed')
    elif not error_on_fail:
        spinner.text = 'Oh my zsh not installed: Installing...'
        run('sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"')
        spinner.stop()
        install_ohmyzsh(True)
    else:
        spin_fail('Oh my zsh')

def install_font(error_on_fail=False):
    spinner.start('Checking if font is installed')
    if os.path.exists(f'{user}/Library/Fonts/Fura Code Medium Nerd Font Complete.ttf'):
        spinner.succeed('Font is installed')
    elif not error_on_fail:
        spinner.text = 'Font is not installed: Installing...'
        run(f'cp ./Fura\ Code\ Medium\ Nerd\ Font\ Complete.ttf {user}/Library/Fonts/')
        spinner.stop()
        install_font(True)
    else:
        spin_fail('Font')

def main():
    program_installed('brew', 'Homebrew', install_brew)
    program_installed('nvim', 'Neovim', install_nvim)
    update_nvim()
    add_configs()
    install_plug()
    install_plug_plugins()
    program_installed('npm','npm', install_nvm)
    install_nvim_language_plugins()
    install_iterm()
    install_ohmyzsh()
    install_font()

    print('\n🐝 \033[92mAll done! Run \033[96mpython3 install-themes.py\033[92m to install iTerm themes\033[0m')
    print('\nDon\'t forget to set font in \033[96miTerm2 > Preferences > Profile > Text > Font\033[0m\n')
if __name__ =='__main__':
    main()
