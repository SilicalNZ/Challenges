def int_to_binary(int_to_binary_number, int_to_binary_byte_size):
    a = "{0:b}".format(int_to_binary_number)
    a = "0" * (int_to_binary_byte_size - len(a)) + a

    return a


def binary_to_int(binary_to_int_byte):
    return int(binary_to_int_byte, 2)


def round_key(
    key_buffer,      # [key_length]key_buffer
    key_length,      # int
    round_constant,  # int
):  # [key_length]int

    # -- Reserve memory footprint ----------
    round_key_result = [0x00] * key_length  # [key_length]int

    # -- Constants ----------
    round_constant_substitution = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]  # [10]int

    # -- Navigate ----------

    # We write to memory here so that we can iterate later
    round_key_result[0] = key_buffer[13]
    round_key_result[1] = key_buffer[14]
    round_key_result[2] = key_buffer[15]
    round_key_result[3] = key_buffer[12]

    for round_key_i in range(4):
        a = round_key_result[round_key_i]
        a = int_to_binary(a, 8)
        a = binary_substitution(a)
        round_key_result[round_key_i] = a

    round_key_result[0] ^= round_constant_substitution[round_constant]

    round_key_result[0] = round_key_result[0] ^ key_buffer[0]
    round_key_result[1] = round_key_result[1] ^ key_buffer[1]
    round_key_result[2] = round_key_result[2] ^ key_buffer[2]
    round_key_result[3] = round_key_result[3] ^ key_buffer[3]

    round_key_result[4] = round_key_result[0] ^ key_buffer[4]
    round_key_result[5] = round_key_result[1] ^ key_buffer[5]
    round_key_result[6] = round_key_result[2] ^ key_buffer[6]
    round_key_result[7] = round_key_result[3] ^ key_buffer[7]

    round_key_result[8] = round_key_result[4] ^ key_buffer[8]
    round_key_result[9] = round_key_result[5] ^ key_buffer[9]
    round_key_result[10] = round_key_result[6] ^ key_buffer[10]
    round_key_result[11] = round_key_result[7] ^ key_buffer[11]

    round_key_result[12] = round_key_result[8] ^ key_buffer[12]
    round_key_result[13] = round_key_result[9] ^ key_buffer[13]
    round_key_result[14] = round_key_result[10] ^ key_buffer[14]
    round_key_result[15] = round_key_result[11] ^ key_buffer[15]

    # -- Return result ----------
    return round_key_result


def xor(
    plain_text_buffer,      # [plain_text_length]int
    key_buffer,             # [key_length]int
    key_length,             # int
):  # [key_length]int

    # -- Reserve memory footprint ----------
    result = [0x00] * key_length  # [key_length]int

    # -- Constants ----------

    # -- Navigate ----------

    for element_index in range(key_length):
        # -- Computation on element ----------
        a = plain_text_buffer[element_index]
        b = key_buffer[element_index]
        result[element_index] = a ^ b

    # -- Return result ----------
    return result


def binary_substitution(
    binary_number  # [byte_length]bool
):  # int

    # -- Reserve memory footprint ----------
    binary_number_split = ["0"] * 4              # [4]bool
    aes_byte_substitution_matrix_index = [0, 0]  # [2]int

    # -- Constants ----------
    byte_length = 8                                                     # int
    byte_iterations = 2                                                 # int
    byte_length_half = byte_length // byte_iterations                    # int
    aes_byte_substitution_size = [16, 16]                               # [2]int
    aes_byte_substitution_size_rows = aes_byte_substitution_size[0]     # int
    aes_byte_substitution_size_columns = aes_byte_substitution_size[1]  # int

    aes_byte_substitution = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    ]  # [aes_byte_substitution_size_rows * aes_byte_substitution_size_columns]int

    # -- Navigate ----------

    # Take block and split into chunks
    for binary_chunk_iteration in range(byte_iterations):
        binary_chunk_start_index = binary_chunk_iteration * byte_length_half  # int

        for element_index in range(byte_length_half):
            element = binary_number[element_index + binary_chunk_start_index]  # bool

            # -- Computation on element ----------
            binary_number_split[element_index] = element

        # -- Computation on element ----------
        aes_byte_substitution_index_value = binary_to_int("".join(binary_number_split))

        # -- Write to reserved memory ----------
        aes_byte_substitution_matrix_index[binary_chunk_iteration] = aes_byte_substitution_index_value

    aes_byte_substitution_index = aes_byte_substitution_matrix_index[1] \
        + aes_byte_substitution_size_rows \
        * aes_byte_substitution_matrix_index[0]   # int
    result = aes_byte_substitution[aes_byte_substitution_index]  # int

    # -- Return result ----------
    return result


def substitution(
    plain_text_buffer,      # [plain_text_length]int
    key_length,             # int
):  # [key_length]int

    # -- Reserve memory footprint ----------
    result = [0x00] * key_length  # [key_length]int

    # -- Constants ----------
    byte_length = 8          # int
    key_length = key_length  # int

    # -- Navigate ----------

    # Take chunk and split into elements
    for element_index in range(key_length):
        element = plain_text_buffer[element_index]  # int

        # -- Computation on element ----------
        element_as_binary = int_to_binary(element, byte_length)  # [byte_length]bool
        element = binary_substitution(element_as_binary)         # int

        # -- Write to reserved memory ----------
        result[element_index] = element

    # -- Return result ----------
    return result


def shift_row(
    plain_text_buffer,      # [plain_text_length]int
    key_length,             # int
):  # [key_length]int

    # -- Reserve memory footprint ----------
    result = [0x00] * key_length  # [key_length]int

    # -- Constants ----------
    row_modifier = [0x00, 0x01, 0x02, 0x03]  # [4]int
    matrix_size = [4, 4]                     # [2]int
    matrix_size_rows = matrix_size[0]        # int
    matrix_size_columns = matrix_size[1]     # int
    key_length = key_length                  # int

    # -- Navigate ----------

    # Take chunk and split into rows
    for text_chunk_row_index in range(matrix_size_rows):

        # Take row and split into elements
        for text_chunk_column_index in range(matrix_size_columns):
            # Working with columns, means indexing along y-axis
            element_index = text_chunk_row_index                       # int
            element_row_modifier = row_modifier[text_chunk_row_index]  # int

            # -- Computation on element ----------
            element = plain_text_buffer[element_index + text_chunk_column_index * matrix_size_columns]  # int
            result_index = element_index + (
                (text_chunk_column_index + matrix_size_rows - element_row_modifier)
                % matrix_size_rows
            ) * matrix_size_rows  # int

            # -- Write to reserved memory ----------
            result[result_index] = element

    # -- Return result ----------
    return result


def gmul(
    a,  # int
    b,  # int
):  # int
    if b == 1:
        return a

    tmp = (a << 1) & 0xff  # int
    if a >= 128:
        tmp = tmp ^ 0x1b

    if b == 2:
        return tmp
    elif b == 3:
        return tmp ^ a


def mix_column(
    column,  # [4]int
):  # [4]int

    # -- Reserve memory footprint ----------
    result = [0x00] * 4

    # -- Constants ----------

    # -- Navigate ----------
    a = column[0]  # int
    b = column[1]  # int
    c = column[2]  # int
    d = column[3]  # int

    result[0] = gmul(a, 2) ^ gmul(b, 3) ^ gmul(c, 1) ^ gmul(d, 1)
    result[1] = gmul(a, 1) ^ gmul(b, 2) ^ gmul(c, 3) ^ gmul(d, 1)
    result[2] = gmul(a, 1) ^ gmul(b, 1) ^ gmul(c, 2) ^ gmul(d, 3)
    result[3] = gmul(a, 3) ^ gmul(b, 1) ^ gmul(c, 1) ^ gmul(d, 2)

    # -- Return result ----------
    return result


def mix_columns(
    plain_text_buffer,      # [key_length]int
    key_length,             # int
):  # [key_length]int

    # -- Reserve memory footprint ----------
    result = [0x00] * key_length  # [key_length]int
    column = [0x00] * 4

    # -- Constants ----------
    matrix_size = [4, 4]                     # [2]int
    matrix_size_rows = matrix_size[0]        # int
    matrix_size_columns = matrix_size[1]     # int
    key_length = key_length                  # int

    # -- Navigate ----------

    # Take chunk and split into columns
    for text_chunk_column_iteration in range(matrix_size_columns):
        text_chunk_column_start_index = matrix_size_columns * text_chunk_column_iteration

        # Take column and split into elements
        for text_chunk_row_index in range(matrix_size_rows):
            position = text_chunk_row_index + text_chunk_column_start_index  # int
            column[text_chunk_row_index] = plain_text_buffer[position]

        # -- Computation on element ----------
        element = mix_column(column)  # [plain_text_length]int

        position = text_chunk_column_start_index  # int

        # -- Write to reserved memory ----------
        result[position] = element[0]
        result[position + 1] = element[1]
        result[position + 2] = element[2]
        result[position + 3] = element[3]

    # -- Return result ----------
    return result


def aes(
    key,         # str
    plain_text,  # str
    iv,          # str
):  # str

    # -- Constants ----------
    key_length = len(key)  # int
    assert key_length == 16
    assert len(iv) == key_length

    plain_text_length = len(plain_text)  # int

    # Pad plain_text
    if plain_text_length % key_length != 0:
        plain_text_padding = key_length - (plain_text_length % key_length)
        plain_text_length += plain_text_padding
        plain_text += " " * plain_text_padding

    # -- Reserve memory footprint ----------
    key_buffer = list(map(ord, key))                         # [key_length]int
    plain_text_buffer = list(map(ord, plain_text))           # [plain_text_length]int
    plain_text_chunk_buffer = [0 for _ in range(key_length)] # [key_length]int
    result = [0 for _ in range(plain_text_length)]           # [plain_text_length]int
    previous_plain_text_chunk_buffer = list(map(ord, iv))    # [key_length]int

    plain_text_iterations = plain_text_length // key_length  # int

    # -- Navigate ----------

    # Take block and split into chunks
    for text_chunk_iteration in range(plain_text_iterations):
        plain_text_start_index = key_length * text_chunk_iteration  # int

        for i in range(key_length):
            plain_text_chunk_buffer[i] = plain_text_buffer[plain_text_start_index + i]

        # -- Computation on element ----------
        plain_text_current_buffer = xor(previous_plain_text_chunk_buffer, plain_text_chunk_buffer, key_length)

        # Round 0, Add Roundkey
        plain_text_current_buffer = xor(plain_text_current_buffer, key_buffer, key_length)

        latest_key = key_buffer
        for round_constant in range(10):
            # Substitution Bytes
            plain_text_current_buffer = substitution(plain_text_current_buffer, key_length)

            # Shift Row
            plain_text_current_buffer = shift_row(plain_text_current_buffer, key_length)

            # Mix Column
            if round_constant != 9:
                plain_text_current_buffer = mix_columns(plain_text_current_buffer, key_length)

            # Add Roundkey
            latest_key = round_key(latest_key, key_length, round_constant)
            plain_text_current_buffer = xor(plain_text_current_buffer, latest_key, key_length)

        # -- Write to reserved memory ----------
        for i in range(key_length):
            result[plain_text_start_index + i] = plain_text_current_buffer[i]
            previous_plain_text_chunk_buffer[i] = plain_text_current_buffer[i]

    # -- Return result ----------
    return result

if __name__ == "__main__":
    print(list(map(hex, aes("Thats my Kung Fu", "Two One Nine TwoTwo One Nine Two", "abcdefghijklmnop"))))
