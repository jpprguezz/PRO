# ****************
# TODO SON CARITAS
# ****************


def run(emoji_text: str) -> str:
    # TU CÓDIGO AQUÍ
    emoji = emoji_text
    match emoji_text.lower:
        case 'happy':
            print('😀')
        case 'SAD':
            print('😔')
        case 'Angry':
            print('😡')
        case 'peNsive':
            print('🤔')
        case 'surpriseD':
            print('😮')

    return emoji


if __name__ == '__main__':
    run('happy')