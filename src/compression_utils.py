import copy
from queue import *
from dataclasses import *
from typing import *
from byte_utils import *

# [!] Important: This is the character code of the End Transmission Block (ETB)
# Character -- use this constant to signal the end of a message
ETB_CHAR = "\x17"

class HuffmanNode:
    '''
    HuffmanNode class to be used in construction of the Huffman Trie
    employed by the ReusableHuffman encoder/decoder below.
    '''
    
    # Educational Note: traditional constructor rather than dataclass because of need
    # to set default values for children parameters
    def __init__(self, char: str, freq: int, 
                 zero_child: Optional["HuffmanNode"] = None, 
                 one_child: Optional["HuffmanNode"] = None):
        '''
        HuffNodes represent nodes in the HuffmanTrie used to create a lossless
        encoding map used for compression. Their properties are given in this
        constructor's arguments:
        
        Parameters:
            char (str):
                Really, a single character, storing the character represented
                by a leaf node in the trie
            freq (int):
                The frequency with which the character / characters in a subtree
                appear in the corpus
            zero_child, one_child (Optional[HuffmanNode]):
                The children of any non-leaf, or None if a leaf; the zero_child
                will always pertain to the 0 bit part of the prefix, and vice
                versa for the one_child (which will add a 1 bit to the prefix)
        '''
        self.char = char
        self.freq = freq
        self.zero_child = zero_child
        self.one_child = one_child

    def is_leaf(self) -> bool:
        '''
        Returns:
            bool:
                Whether or not the current node is a leaf
        '''
        return self.zero_child is None and self.one_child is None

class ReusableHuffman:
    '''
    ReusableHuffman encoder / decoder that is trained on some original
    corpus of text and can then be used to compress / decompress other
    text messages that have similar distributions of characters.
    '''
    
    def __init__(self, corpus: str):
        '''
        Constructor for a new ReusableHuffman encoder / decoder that is fit to
        the given text corpus and can then be used to compress and decompress
        messages with a similar distribution of characters.
        
        Parameters:
            corpus (str):
                The text corpus on which to fit the ReusableHuffman instance,
                which will be used to construct the encoding map
        '''
        self._encoding_map: dict[str, str] = dict()
        
        # [!] TODO: complete construction of self._encoding_map by constructing
        # the Huffman Trie -- remember to save its root as an attribute!
    
    def get_encoding_map(self) -> dict[str, str]:
        '''
        Simple getter for the encoding map that, after the constructor is run,
        will be a dictionary of character keys mapping to their compressed
        bitstrings in this ReusableHuffman instance's encoding
        
        Example:
            {ETB_CHAR: 10, "A": 11, "B": 0}
            (see unit tests for more examples)
        
        Returns:
            dict[str, str]:
                A copy of this ReusableHuffman instance's encoding map
        '''
        return copy.deepcopy(self._encoding_map)
    
    # Compression
    # ---------------------------------------------------------------------------
    
    def compress_message(self, message: str) -> bytes:
        '''
        Compresses the given String message / text corpus into its Huffman-coded
        bitstring, and then converted into a Python bytes type.
        
        [!] Uses the _encoding_map attribute generated during construction.
        
        Parameters:
            message (str):
                String representing the corpus to compress
        
        Returns:
            bytes:
                Bytes storing the compressed corpus with the Huffman coded
                bytecode. Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            compressed_message = huff_coder.compress_message("ABBBCC")
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            solution = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual(solution, compressed_message)
        '''
        # [!] TODO: Complete compression!
        return b'\x00'
    
    # Decompression
    # ---------------------------------------------------------------------------
    
    def decompress (self, compressed_msg: bytes) -> str:
        '''
        Decompresses the given bytes representing a compressed corpus into their
        original character format.
        
        [!] Should use the Huffman Trie generated during construction.
        
        Parameters:
            compressed_msg (bytes):
                Formatted as (1) the compressed message bytes themselves,
                (2) terminated by the ETB_CHAR, and (3) [Optional] padding of 0
                bits to ensure the final byte is 8 bits total.
        
        Returns:
            str:
                The decompressed message as a string.
        
        Example:
            huff_coder = ReusableHuffman("ABBBCC")
            # byte 0: 1010 0011 (100 = ETB, 101 = 'A', 0 = 'B', 11 = 'C')
            # byte 1: 1110 0000
            # [!] Only first 5 bits of byte 1 are meaningful (rest are padding)
            compressed_msg: bytes = bitstrings_to_bytes(['10100011', '11100000'])
            self.assertEqual("ABBBCC", huff_coder.decompress(compressed_msg))
        '''
        # [!] TODO: Complete decompression!
        return ""
    
        