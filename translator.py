import string
from typing import Final, List, Tuple, Dict, Generator

# DON'T DO AS FOLLOWING
# a = ('1', '2')
# b = ('2', '1')
lang_common = ('1', '2', '3', 'ц', '0', 'й')
lang_orcish = ('1', '2', '3', '6', '0', 'й')
lang_test = ('s', '2', 'ю', 'b', 'a', '7')


class Translator:
    """
        Provide interface for World of Warcraft cross-faction messaging
    """
    def __init__(self, lang_uniq_symbols: tuple):
        """
        Constructor
        """
        self._symbols_used_to_encode: Final[int] = 3
        self._encoding_alphabet: Final[Tuple[str, ...]] = lang_uniq_symbols
        self._alphabet: Final[Tuple[str]] = self.__setup_message_alphabet()
        self._head: Final[str] = self.__get_prefix()
        self._tail: Final[str] = self.__get_postfix()
        self._encoding_table: Final[Dict[str, str]] = self.__setup_encoding_table()
        self._decode_table: Final[Dict[str, str]] = self.__setup_decoding_table()

    def encode(self, message: str) -> str:
        """
        Encode message. Add service data
        Structure of the message:
            head
            alphabet
            message
            tail
        :param message: input message
        :return: encoded message
        """
        encoded_data: List[str, ...] = list()
        encoded_data.append(self._head)
        encoded_data.extend(self._encoding_alphabet)
        for char in message:
            encoded_char = self._encoding_table[char]
            encoded_data.append(encoded_char)
        encoded_data.append(self._tail)

        encoded_string = ''.join(encoded_data)
        encoded_string = self.__prepare_message(encoded_string)

        return encoded_string

    def decode(self, message: str) -> str:
        """
        Decode message. Assume that message is valid
        :param message: input message
        :return: decoded message
        """
        message = self.__filter_message(message)
        self.__fast_verify_message(message)

        translated_message: str = self.__translate_message(message)
        self.__verify_message(translated_message)

        # Remove head and tail from message
        translated_message = translated_message.removeprefix(self._head)
        translated_message = translated_message.removesuffix(self._tail)

        encoded_symbols: List[str, ...] = list()
        # Slice encoded message by parts of encoded symbol len
        for i in range(0, len(translated_message), self._symbols_used_to_encode):
            slice_begin: int = i
            slice_end: int = i + self._symbols_used_to_encode
            encoded_symbols.append(
                translated_message[slice_begin:slice_end]
            )

        # Decode chars
        decoded_symbols: List[str, ...] = list(
            map(
                self._decode_table.get,
                encoded_symbols
            )
        )
        decoded_message: Final[str] = ''.join(decoded_symbols)

        return decoded_message

    def is_encoded(self, message: str) -> bool:
        """
        Checks that message is encoded
        :param message: input message
        :return: bool result of verification
        """
        try:
            self.__fast_verify_message(
                self.__filter_message(message)
            )
        except AssertionError:
            return False
        except Exception:
            raise
        else:
            return True

    @staticmethod
    def __uniq_combination_generator(coding_table_alphabet) -> Generator[str, None, None]:
        for a in coding_table_alphabet:
            for b in coding_table_alphabet:
                for c in coding_table_alphabet:
                    res = ''.join([a, b, c])
                    yield res

    @staticmethod
    def __setup_message_alphabet() -> Tuple[str]:
        """
        Generate input message alphabet
        :return: tuple with alphabet chars
        """
        cyrillic_letters = 'ецьюлтйждбпфчгъукроазхвсямэиныщёшієї'
        special_chars = tuple(' ')

        alphabet: List[str] = list()
        alphabet.extend(tuple(string.ascii_lowercase))
        alphabet.extend(tuple(string.ascii_uppercase))
        alphabet.extend(tuple(cyrillic_letters.lower()))
        alphabet.extend(tuple(cyrillic_letters.upper()))
        alphabet.extend(tuple(string.digits))
        alphabet.extend(tuple(string.punctuation))
        alphabet.extend(special_chars)

        return tuple(alphabet)

    @staticmethod
    def __filter_message(message: str) -> str:
        """
        Remove unneeded data from message
        :param message: input message
        :return: filtered message
        """
        message: str = message.replace(" ", "")
        return message

    @staticmethod
    def __prepare_message(message: str) -> str:
        """
        Prepare message for printing
        :param message: encoded message
        :return: prepared message
        """
        message: str = ' '.join(message)
        return message

    def __fast_verify_message(self, message: str) -> None:
        """
        Basic verification of filtered message. Used before transformations
        :param message: filtered message
        :return: None
        """
        assert message[0] == message[1] == message[-2] == message[-3]
        assert (len(message) - len(self._encoding_alphabet)) % self._symbols_used_to_encode == 0

    def __encoding_alphabet_from_msg(self, message: str) -> List[str]:
        """
        Extract encoding alphabet from filtered message
        :param message: filtered message
        :return: encoding alphabet
        """
        alphabet_start_index: Final[int] = len(self._head)
        alphabet_len: Final[int] = len(self._encoding_alphabet)
        alphabet_end_index: Final[int] = alphabet_start_index + alphabet_len

        other_alphabet: List[str] = list(
            message[alphabet_start_index:alphabet_end_index]
        )

        return other_alphabet

    def __translate_message(self, message: str) -> str:
        """
        Translate message from other language to current.
        Extract other alphabet from the message. Replace message symbols by current language symbols.
        E.g:
            our_alphabet: [a, b, c, ...]
            their_alphabet: [1, 2, 3, ...]
            According to alphabets 1==b 2==b 3==c and so on
            message: "1 2 3"
            translated_message: "a b c"
        :param message: filtered message
        :return: translated message
        """
        other_alphabet: list = self.__encoding_alphabet_from_msg(message)

        # remove other_alphabet from message
        alphabet_start_index: Final[int] = len(self._head)
        alphabet_len: Final[int] = len(self._encoding_alphabet)
        alphabet_end_index: Final[int] = alphabet_start_index + alphabet_len
        message = message[:alphabet_start_index] + message[alphabet_end_index:]

        # Translate message
        for match, substitution in zip(other_alphabet, self._encoding_alphabet):
            message = message.replace(match, substitution)

        return message

    def __get_postfix(self) -> str:
        """
        Create encoded message tail
        :return: message tail
        """
        symbol_index: Final[int] = -1
        encoding_value: Final[str] = self._encoding_alphabet[symbol_index]
        temp: Final[str] = encoding_value * (self._symbols_used_to_encode - 1) + self._encoding_alphabet[0]
        return temp

    def __get_prefix(self) -> str:
        """
        Create encoded message head
        :return: message head
        """
        symbol_index: Final[int] = -1
        encoding_value: Final[str] = self._encoding_alphabet[symbol_index]
        temp: Final[str] = encoding_value * (self._symbols_used_to_encode - 1) + self._encoding_alphabet[1]
        return temp

    def __setup_encoding_table(self) -> Dict[str, str]:
        """
        Generate encoding dictionary
        :return: dictionary with "input char": "encoded representation" items
        """
        gen = self.__uniq_combination_generator(self._encoding_alphabet)
        temp_table: Dict[str, str] = dict()
        for char in self._alphabet:
            temp_table[char] = gen.__next__()

        return temp_table

    def __setup_decoding_table(self) -> Dict[str, str]:
        """
        Generate decoding dictionary
        :return: dictionary with "encoded representation": "input char" items
        """
        temp_table: Dict[str, str] = {val: key for key, val in self._encoding_table.items()}
        return temp_table

    def __verify_message(self, message: str) -> None:
        """
        Checks that passed message is encoded
        :param message: filtered message
        """
        assert len(message) % self._symbols_used_to_encode == 0
        assert message.startswith(self._head) and message.endswith(self._tail)
