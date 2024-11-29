# text_chunking.py

import os
import json
from transformers import AutoTokenizer

class TextChunker:
    def __init__(self, tokenizer_name='xlm-roberta-base', max_tokens=512, overlap_tokens=50, output_folder='chunked_text'):
        """
        Initialize the TextChunker object.
        Args:
            tokenizer_name (str): The name of the pre-trained tokenizer to use.
            max_tokens (int): The maximum number of tokens in each chunk.
            overlap_tokens (int): The number of overlapping tokens between chunks.
            output_folder (str): The name of the folder to save the chunked text.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.output_folder = output_folder
    
    def chunk_text(self, text):
        """
        Split text into chunks with specified max tokens and overlap.
        Args:
            text (str): The input text to split into chunks.
        Returns:
            chunks (list): List of dictionaries with 'chunk' and 'start_index'.
        """
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        total_tokens = len(tokens)
        chunks = []
        start = 0
        while start < total_tokens:
            end = min(start + self.max_tokens, total_tokens)
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            char_start_index = self.tokenizer.decode(tokens[:start], clean_up_tokenization_spaces=False)
            char_start_index = len(char_start_index)
            chunks.append({
                'chunk': chunk_text,
                'start_index': char_start_index
            })
            start += self.max_tokens - self.overlap_tokens
        return chunks

    def save_chunks_to_json(self, chunks, output_file_path):
        """
        Save chunks to a JSON file.
        """
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

    
    def generate_chunks_file(self, input_path):
        """
        Generate chunked text from input text.
        Args:
            input_path (str): The path to the input text file.
        Returns:
            path (str): The path to the saved JSON file with chunked text.
            number_of_chunks (int): The number of chunks created.
            first_chunk (str): The text of the first chunk.
        """
         # Check if the file is a .txt file
        if not input_path.lower().endswith('.txt'):
            raise ValueError("Input file must be a .txt file.")

        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            print(f"Error reading file {input_path}. Skipping.")
            return
        
        # Generate output file name
        base_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_filename = f"{name_without_ext}.json"
        output_path = os.path.join(self.output_folder, output_filename)

        chunks = self.chunk_text(content)
        number_of_chunks = len(chunks)
        first_chunk = chunks[0]['chunk'][:500]
        self.save_chunks_to_json(chunks, output_path)
        return output_path, number_of_chunks, first_chunk
        
