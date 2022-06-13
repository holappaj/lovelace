def format_hex(number, bits):
    return hex(number).replace("0x", "").zfill(bits // 4)
