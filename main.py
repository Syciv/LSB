"""Программма прячет текст в картинке, 
записывая в биты информации в наименее значимый бит байта, отвечающего за цвет
желательно bmp-изображение
"""

def hide_text(path, message, new_file_name):
    """Скрытие сообщение в изображении"""
    # Добавляем размер сообщения в начало (4 байта)
    num = len(message).to_bytes(4, byteorder="big")
    message = num + message

    with open(path, mode='rb') as source_file:
        with open(new_file_name, mode='wb') as destination_file:

            bytes = source_file.read(100)
            destination_file.write(bytes)

            for i in message:
                bits = 128

                for j in range(8):
                    byte = source_file.read(1)
                    if bits & i == 0:
                        new_bit = 0
                    else:
                        new_bit = 1
                    new_byte = (int.from_bytes(byte, "big") & 254) | new_bit
                    destination_file.write(new_byte.to_bytes(1, byteorder="big"))
                    bits = int(bits) >> 1

            byte = source_file.read(1)
            while byte:
                destination_file.write(byte)
                byte = source_file.read(1)


def reveal_text(path):
    """Расшифровка сообщения в картинке"""
    with open(path, mode='rb') as file:
        file.read(100)
        num_bytes = file.read(32)
        nums = read_from_bytes(num_bytes)
        num = int.from_bytes(nums, "big")
        mes_bytes = file.read(8*num)
        message = read_from_bytes(mes_bytes)
        return message


def read_from_bytes(bytes):
    """Считывание скрытой информации из заданного потока байт"""
    result = b''
    bits = 0
    res_byte = 0
    for i in bytes:
        bit = i & 1
        bits += 1
        res_byte = res_byte * 2 + bit
        if bits == 8:
            result += res_byte.to_bytes(1, byteorder="big")
            bits = 0
            res_byte = 0
    return result


if __name__ == '__main__':
    image_path = 'image.bmp'
    result_image_path = 'image-with-no-any-secret-message.bmp'

    act = input("1: спрятать\n2: раскрыть\n")
    if act == '1':
        message = input("Секретное сообщение: ")
        hide_text(image_path, message.encode(), result_image_path)
    elif act == '2':
        # path = input("Раскрываем файл: ")
        path = 'image-with-no-any-secret-message.bmp'
        message = reveal_text(path)
        print(message.decode())
    else:
        print("Чел...")