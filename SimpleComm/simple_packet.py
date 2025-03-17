"""
Module that contains the SimplePacket class, the basic form of the SimpleComm protocol
"""
from typing import Union
from simplecomm_utils import _check_integer_is_valid



class SimplePacket: # pylint: disable=too-many-public-methods
    """
    A class to represent the packets used in SimpleComm

    Attributes:
        SYN (int): Synchronization byte.
        MAX_DATA_LEN (int): Maximum length of the data payload.
    """
    SYN = 0x02
    MAX_DATA_LEN = 128
    _DATA_INDEX_SYN = 0
    _DATA_INDEX_EXPECTED_LEN = 1
    _DATA_INDEX_SOURCE = 2
    _DATA_INDEX_DESTINATION = 3
    _DATA_INDEX_TYPE = 4
    _DATA_INDEX_DATA = 5

    def __init__(self) -> None:
        """
        Initializes a new SimplePacket instance.
        """
        self._data = bytearray(5 + self.MAX_DATA_LEN + 1)
        self.clear()

    def clear(self) -> None:
        """
        Resets the packet data to its initial state, setting the synchronization byte,
        expected length, source, destination, and type fields to zero.
        """
        self._data[self._DATA_INDEX_SYN] = self.SYN
        self._data[self._DATA_INDEX_EXPECTED_LEN] = 0
        self._data[self._DATA_INDEX_SOURCE] = 0
        self._data[self._DATA_INDEX_DESTINATION] = 0
        self._data[self._DATA_INDEX_TYPE] = 0

    def setSource(self, source) -> None: # pylint: disable=invalid-name
        """
        Sets the source identifier for the packet.

        Args:
            source (int): The source identifier. Must be a non-negative byte.

        Raises:
            ValueError: If the source is not a valid byte.
        """
        _check_integer_is_valid(source, 1, signed = False)
        self._data[self._DATA_INDEX_SOURCE] = source
    def setDestination(self, destination) -> None: # pylint: disable=invalid-name
        """
        Sets the destination identifier for the packet.

        Args:
            destination (int): The destination identifier. Must be a non-negative byte.

        Raises:
            ValueError: If the destination is not a valid byte.
        """
        _check_integer_is_valid(destination, 1, signed = False)
        self._data[self._DATA_INDEX_DESTINATION] = destination
    def setType(self, packet_type: int) -> None: # pylint: disable=invalid-name
        """
        Sets the type of the packet.

        Args:
            packet_type (int): The packet type. Must be a non-negative byte.

        Raises:
            ValueError: If the packet type is not a valid byte.
        """
        _check_integer_is_valid(packet_type, 1, signed = False)
        self._data[self._DATA_INDEX_TYPE] = packet_type

    def getSource(self) -> int: # pylint: disable=invalid-name
        """
        Returns the source identifier of the packet.
        """
        return self._data[self._DATA_INDEX_SOURCE]
    def getDestination(self) -> int: # pylint: disable=invalid-name
        """
        Returns the destination identifier of the packet.
        """
        return self._data[self._DATA_INDEX_DESTINATION]
    def getType(self) -> int: # pylint: disable=invalid-name
        """
        Returns the type of the packet.

        Returns:
            int: The packet type.
        """
        return self._data[self._DATA_INDEX_TYPE]

    def setData(self, value: bytes) -> None: # pylint: disable=invalid-name
        """
        Sets the data payload for the packet.

        Args:
            value (bytes): The data to set. Must not exceed MAX_DATA_LEN.

        Raises:
            OverflowError: If the data length exceeds MAX_DATA_LEN.
        """
        value_len = len(value)
        if value_len > self.MAX_DATA_LEN:
            raise OverflowError("Data cannot be bigger than 128 bytes")
        self._data[self._DATA_INDEX_DATA:] = value
        self._data[self._DATA_INDEX_EXPECTED_LEN] = value_len


    def setInteger(self, value: int, n_bytes: int, signed: bool = True) -> None: # pylint: disable=invalid-name
        """
        Sets an integer value in the data payload of the packet.

        Args:
            value (int): The integer value to set. Must fit within the specified byte size.
            n_bytes (int): The number of bytes that the integer should occupy (1, 2, 4, or 8).
            signed (bool): A flag indicating whether the integer is signed (True)
                           or unsigned (False).

        Raises:
            ValueError: If the integer does not fit within the specified range based on the
                        number of bytes.
        """
        _check_integer_is_valid(value, n_bytes, signed = signed)
        self.setData(value.to_bytes(n_bytes, byteorder = "little", signed = signed))

    def setChar(self, value: Union[int, str], signed: bool = True) -> None: # pylint: disable=invalid-name
        """
        Sets an integer value in the data payload of the packet.

        Args:
            value (int or str): The integer value to set. Must fit within the specified byte size.
                                It can also be an string of length one.
            signed (bool): A flag indicating whether the integer is signed (True)
                           or unsigned (False).

        Raises:
            ValueError: If the integer does not fit within the specified range based on the
                        number of bytes.
            TypeError: If the string's length is not 1 (i.e. not a character).
        """
        if isinstance(value, str):
            if len(value) > 1:
                raise TypeError("setChar only accepts strings with length equal to 1.")
            value = ord(value)
        self.setInteger(value, 1, signed)
    def setShort(self, value: int, signed = True) -> None: # pylint: disable=invalid-name
        """
        Sets a short integer value in the data payload of the packet.

        Args:
            value (int): The short integer value to set. Must fit within the specified byte size.
            signed (bool): A flag indicating whether the integer is signed (True)
                           or unsigned (False).

        Raises:
            ValueError: If the short integer does not fit within the specified range based on the
                        number of bytes.
        """
        self.setInteger(value, 2, signed)
    def setInt(self, value: int, signed = True) -> None: # pylint: disable=invalid-name
        """
        Sets a integer value in the data payload of the packet.

        Args:
            value (int): The integer value to set. Must fit within the specified byte size.
            signed (bool): A flag indicating whether the integer is signed (True)
                           or unsigned (False).

        Raises:
            ValueError: If the integer does not fit within the specified range based on the
                        number of bytes.
        """
        self.setInteger(value, 4, signed)
    def setLong(self, value: int, signed = True) -> None: # pylint: disable=invalid-name
        """
        Sets a long integer value in the data payload of the packet.

        Args:
            value (int): The long integer value to set. Must fit within the specified byte size.
            signed (bool): A flag indicating whether the integer is signed (True)
                           or unsigned (False).

        Raises:
            ValueError: If the long integer does not fit within the specified range based on the
                        number of bytes.
        """
        self.setInteger(value, 8, signed)

    def setString(self, value) -> None: # pylint: disable=invalid-name
        """
        Sets a string value in the data payload of the packet.

        Args:
            value (str): The string to set. The string will be encoded in UTF-8 and a null
                         terminator will be added.

        Raises:
            OverflowError: If the length of the string exceeds MAX_DATA_LEN - 1
                           (to accommodate the null terminator).
        """
        string_to_set = bytearray(value, "utf-8")
        string_to_set.append(0x00)
        self.setData(string_to_set)


    def getData(self) -> bytes: # pylint: disable=invalid-name
        """
        Retrieves the data payload from the packet.

        Raises:
            AttributeError: If no data can be retrieved from this packet.
        """
        data_length = self._data[self._DATA_INDEX_EXPECTED_LEN]
        if data_length  == 0:
            raise AttributeError("No data can be retrieved from this package")
        return bytes(self._data[self._DATA_INDEX_DATA:self._DATA_INDEX_DATA + data_length])

    def getInteger(self, n_bytes: int, signed: bool = True) -> int: # pylint: disable=invalid-name
        """
        Retrieves an integer value from the data payload of the packet.

        Args:
            n_bytes (int): The number of bytes to read for the integer.
            signed (bool): A flag indicating whether the integer is signed (True)
                           or unsigned (False).

        Returns:
            int: The integer value retrieved from the packet.
        """
        data = self._data[self._DATA_INDEX_DATA : self._DATA_INDEX_DATA + n_bytes]
        return int.from_bytes(data, byteorder = "little", signed = signed)

    def getChar(self, signed: bool = True) -> int: # pylint: disable=invalid-name
        """
        Retrieves a character value from the data payload of the packet.

        Args:
            signed (bool): A flag indicating whether the character is signed (True)
                           or unsigned (False).

        Returns:
            int: The character value retrieved from the packet.
        """
        return self.getInteger(1, signed)
    def getShort(self, signed: bool = True) -> int: # pylint: disable=invalid-name
        """
        Retrieves a short integer from the data payload of the packet.

        Args:
            signed (bool): A flag indicating whether the character is signed (True)
                           or unsigned (False).

        Returns:
            int: The short integer retrieved from the packet.
        """
        return self.getInteger(2, signed)
    def getInt(self, signed: bool = True) -> int: # pylint: disable=invalid-name
        """
        Retrieves a integer from the data payload of the packet.

        Args:
            signed (bool): A flag indicating whether the character is signed (True)
                           or unsigned (False).

        Returns:
            int: The integer retrieved from the packet.
        """
        return self.getInteger(4, signed)
    def getLong(self, signed: bool = True) -> int: # pylint: disable=invalid-name
        """
        Retrieves a long integer from the data payload of the packet.

        Args:
            signed (bool): A flag indicating whether the character is signed (True)
                           or unsigned (False).

        Returns:
            int: The long integer retrieved from the packet.
        """
        return self.getInteger(8, signed)

    def getString(self) -> str: # pylint: disable=invalid-name
        """
        Retrieves a null-terminated string from the data payload of the packet.

        Returns:
            str: The string value retrieved from the packet, excluding the null terminator.

        Raises:
            TypeError: If the string is not null-terminated
        """
        data = self.getData()
        if data[len(data) - 1] != 0:
            raise TypeError("The data contained in this package is not null-terminated")
        return data[:len(data) - 1].decode("utf-8")



if __name__ == "__main__":
    packet = SimplePacket()
    packet.setSource(0x01)
    packet.setDestination(0x02)
    packet.setType(0x0F)
    assert packet.getSource() == 0x01
    assert packet.getDestination() == 0x02
    assert packet.getType() == 0x0F
    packet.clear()

    exception_caught = False
    try:
        packet.getData()
    except AttributeError:
        exception_caught = True
    assert exception_caught

    packet.setData(b'A')
    assert packet.getData() == b'A', f"Got {packet.getData()}"
    packet.setData(b'AAAAAA')
    assert packet.getData() == b'AAAAAA'
    packet.setData(b'A'*128)
    assert packet.getData() == b'A' * SimplePacket.MAX_DATA_LEN

    exception_caught = False
    try:
        packet.setData(b'A' * (SimplePacket.MAX_DATA_LEN + 1))
    except OverflowError:
        exception_caught = True
    assert exception_caught

    packet.setChar(0x45)
    assert packet.getChar() == 0x45
    assert packet.getData() == b'\x45'
    packet.setChar(-33)
    assert packet.getChar() == -33
    assert packet.getData() == b'\xdf'
    packet.setChar('A')
    assert packet.getChar() == ord('A')
    assert packet.getData() == b'A'
    packet.setChar('®', signed = False)
    assert packet.getChar(signed = False) == ord('®')
    assert packet.getData() == b'\xae'

    packet.setShort(456)
    assert packet.getShort() == 456
    assert packet.getData() == b'\xc8\x01'
    packet.setShort(-456)
    assert packet.getShort() == -456
    assert packet.getData() == b'8\xfe'

    packet.setInt(456)
    assert packet.getInt() == 456
    assert packet.getData() == b'\xc8\x01\x00\x00'
    packet.setInt(-456)
    assert packet.getInt() == -456
    assert packet.getData() == b'8\xfe\xff\xff'

    packet.setLong(456)
    assert packet.getLong() == 456
    assert packet.getData() == b'\xc8\x01\x00\x00\x00\x00\x00\x00'
    packet.setLong(-456)
    assert packet.getLong() == -456
    assert packet.getData() == b'8\xfe\xff\xff\xff\xff\xff\xff'

    packet.setString("Hello")
    assert packet.getString() == "Hello"
    assert packet.getData() == b"Hello\x00"
