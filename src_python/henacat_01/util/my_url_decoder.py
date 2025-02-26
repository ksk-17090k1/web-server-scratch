class MyURLDecoder:
    @staticmethod
    def hex2int(b1, b2):
        digit = int(b1, 16) * 16 + int(b2, 16)
        return digit

    @staticmethod
    def decode(src, enc):
        src_bytes = src.encode("ISO_8859_1")
        dest_bytes = bytearray()
        src_len = len(src_bytes)
        src_idx = 0

        while src_idx < src_len:
            if src_bytes[src_idx] == ord("%"):
                dest_bytes.append(
                    MyURLDecoder.hex2int(
                        chr(src_bytes[src_idx + 1]), chr(src_bytes[src_idx + 2])
                    )
                )
                src_idx += 3
            else:
                dest_bytes.append(src_bytes[src_idx])
                src_idx += 1

        return dest_bytes.decode(enc)
