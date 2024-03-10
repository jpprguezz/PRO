# *************************
# BUSCANDO PALABRAS COMUNES
# *************************
import filecmp
from pathlib import Path


def run(input_path: Path) -> bool:
    output_path = 'data/common_words/output.txt'
    # TU CÓDIGO AQUÍ

    return filecmp.cmp(output_path, 'data\common_words\.expected', shallow=False)


if __name__ == '__main__':
    run('data/common_words/minizen.txt')