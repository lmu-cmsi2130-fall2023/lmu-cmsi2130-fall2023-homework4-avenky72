import copy
from queue import *
from dataclasses import *
from typing import *
from byte_utils import *
"""
ATUL VENKATESAN
"""
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

    def __lt__(self, other: "HuffmanNode") -> bool:
        if self.freq == other.freq:
            return self.char < other.char
        return self.freq < other.freq
                
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
        # >> [BAC] Great use of helper methods!
        self._encoding_map: dict[str, str] = dict()
        charfreq = self.char_frequency(corpus)
        self.trie: "HuffmanNode" = self.make_trie(charfreq)
        self.encoding_map(self.trie, "")
    
        
        # [!] TODO: complete construction of self._encoding_map by constructing
        # the Huffman Trie -- remember to save its root as an attribute!
        
    """Frequency dictionary of characters"""    
    # >> [BAC] Provide proper docstrings for ALL methods, the comment should go inside the function
    # and describe its parameters, return type and purpose. (-1).
    def char_frequency(self, str1: str) -> dict[str, int]:
        char_freq: dict = {}
        char_freq[ETB_CHAR] = 1
        for i in str1:
            if i in char_freq:
                char_freq[i] += 1
            else:
                char_freq[i] = 1
        return char_freq

    """Creates a trie based on the frequency dictionary"""
    def make_trie(self, freq: dict[str, int]) -> "HuffmanNode":
        tree: PriorityQueue[HuffmanNode] = PriorityQueue() 
        for key, value in freq.items():
            node = HuffmanNode(key, value)
            tree.put(node)
        """Start from ETB as root and incorporate the next node from the PQ
        """
        # >> [BAC] Remove commented code before submission (-0.5)
        # root = HuffmanNode(ETB_CHAR, 1)
        # root.zero_child = HuffmanNode(ETB_CHAR, root.freq + tree.get().freq)
        while tree.qsize() > 1:
            zero_child = tree.get()
            one_child = tree.get()
            if zero_child.char < one_child.char: 
                parent = HuffmanNode(zero_child.char, zero_child.freq+one_child.freq, zero_child, one_child)
            else:
                parent = HuffmanNode(one_child.char, zero_child.freq+one_child.freq, zero_child, one_child)
            tree.put(parent)
        root = tree.get()
        return root
    
    """Works through the trie to create an encoding map"""
    def encoding_map(self, root: Optional["HuffmanNode"], value: str) -> None:
        if root is None:
            return
        if root.is_leaf() == True:
            self._encoding_map[root.char] = value
        self.encoding_map(root.zero_child, value+"0")
        self.encoding_map(root.one_child, value+"1")         
    
    def get_encoding_map(self) -> dict[str, str]:
        return copy.deepcopy(self._encoding_map)
    
    # Compression
    # ---------------------------------------------------------------------------

    """Compresses the message by slicing the string by 8 bits and adding it to a list to convert to bytes
            convert message into string of bits
        substrings of 8 bits
        the i index in list corresponds to the ith string of bits
        add the extra 0s to the end of the final substring to get to 8 bits
        run the list through bitstring_to_bytes
        """
    def compress_message(self, message: str) -> bytes:  
        compress: str = ""
        # Where to add ETB? Is ETB part of the message or do I include it in the end of the message?
        for i in range(len(message)):
            compress += self._encoding_map[message[i]]
        compress += self._encoding_map[ETB_CHAR]
        length: int = len(compress)//8
        data: list[str] = []
        for i in range(0, length*8, 8):
            data.append(compress[i:i+8])
        remaining: str = compress[(length*8):]
        num2: int = len(remaining)
        data.append(remaining)
        num3: int = 8 - num2
        num4: int = 0
        while num4 < num3:
            data[length] += "0"
            num4+=1
        return bitstrings_to_bytes(data)
        
    
    # Decompression
    # ---------------------------------------------------------------------------

    """Iterates through the bytes and converts them into a string of bits, then iterates through each 
    bit and goes through the trie"""
    def decompress (self, compressed_msg: bytes) -> str:
        # How to iterate through the bytes
        # How to convert the bytes to bitstring
    
        message: str = ""
        for i in compressed_msg:
            # Does it convert it properly?
            message+= byte_to_bitstring(i)

        mesg: str = ""
        curr: "HuffmanNode" = self.trie
        
        for counter in message:
            
            if curr.is_leaf() == True:
                if curr.char == ETB_CHAR:
                    return mesg
                mesg+=curr.char
                curr = self.trie
            if counter == "1":
                curr = curr.one_child
            else:
                curr = curr.zero_child
        # >> [BAC] Watch all this spacing!
            
                
            
        return mesg
    
            
        
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
        # >> [BAC] These comments should go after the function declaration and before any code is written
        # >> [BAC] This return will never be executed given the first return on line 197
        return 
# ===================================================
# >>> [BAC] Summary
# A solid effort that has a lot to like, and I'd say
# you got the main pieces of the algorithm down, but
# just didn't have the time to test some crucial edge
# cases that could've exposed the bugs with your
# tie breaking mechanism. Likewise, remember to give
# yourself time to lint your submission for stylistic
# improvements, which are often as important as the
# functional aspects when it comes time to technical
# interviews and portfolio display. Onwards to the
# next! 
# ---------------------------------------------------
# >>> [BAC] Style Checklist
# [X] = Good, [~] = Mixed bag, [ ] = Needs improvement
# 
# [X] Variables and helper methods named and used well
# [ ] Proper and consistent indentation and spacing
# [~] Proper JavaDocs provided for ALL methods
# [X] Logic is adequately simplified
# [X] Code repetition is kept to a minimum
# ---------------------------------------------------
# Correctness:         92.5 / 100 (-1.5 / missed test)
# Style Penalty:      -1.5
# Mypy Penalty:       -5
# Total:             86.0 / 100
# ===================================================
