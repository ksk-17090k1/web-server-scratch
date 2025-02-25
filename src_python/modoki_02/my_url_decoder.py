class MyURLDecoder:
    @staticmethod
    def hex2int(b1, b2):
        """
        16進数2桁をASCIIコードで示すバイトを、intに変換する。
        """
        if b1 >= "A":
            # 小文字を大文字に変換し、16進数の数値を取得
            digit = (ord(b1.upper()) - ord("A") + 10) * 16
        else:
            digit = (ord(b1) - ord("0")) * 16

        if b2 >= "A":
            digit += ord(b2.upper()) - ord("A") + 10
        else:
            digit += ord(b2) - ord("0")

        return digit

    @staticmethod
    def decode(src, enc):
        """
        URLエンコードされた文字列をデコードする。
        """
        src_bytes = src.encode("ISO-8859-1")  # Javaの `getBytes("ISO_8859_1")` 相当
        dest_bytes = bytearray()

        src_idx = 0
        while src_idx < len(src_bytes):
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

        return dest_bytes.decode(enc)  # Javaの `new String(destBytes2, enc)` 相当
