from dataclasses import dataclass
import PackToSo
import subprocess
import os

def __af(arg: str, iff: bool) -> str:
    return arg if iff else ''

def run(cmd: str, dismissErr: bool) -> bool:
    output = subprocess.run(cmd, capture_output=True, shell=True)
    if output.stderr == b'':
        return True
    print(output.stderr.decode('utf-8'), end='')
    if not dismissErr:
        raise subprocess.CalledProcessError(
            returncode=output.returncode,
            cmd=cmd,
            stderr=output.stderr.decode('utf-8')
            )
    return False

def copy(src: str, dst: str, force=False, dismissErr=False) -> bool:
    return run(f'cp -r{__af("f", force)} {src} {dst}', dismissErr)

def remove(src: str, force=False, dismissErr=False) -> bool:
    return run(f'rm -r{__af("f", force)} {src}', dismissErr)

def move(src: str, dst: str, force=False, dismissErr=False) -> bool:
    return run(f'mv {__af("f", force)} {src} {dst}', dismissErr)

def create_file(src: str):
    os.makedirs(src) if not os.path.exists(src) else False


if __name__ == '__main__':
    PackToSo.PackToSo()
    copy('sample', 'build', force=True)
