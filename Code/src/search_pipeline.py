import os
import re
import hnswlib
import pathlib
import logging
import traceback
import numpy as np
import pandas as pd
import textdistance
from sentence_transformers import SentenceTransformer, util


logging.basicConfig(level=logging.INFO)


class SearchDescriptionPipeline:
    """ Search Engine Pipeline """
    def __init__(self, 
                 semantic_search_topk:int=10,
                 keyword_search_topk:int=2,
                 embedding_model_name:str='all-mpnet-base-v2', 
                 hardware_device='cpu') -> None:
        
        self.description_text = ""
        self.embedding_size = 768
        self.semantic_search_top_k = semantic_search_topk
        self.keyword_search_top_k = keyword_search_topk
        self.keyword_similarity_threshold = 0.85
        self.embedding_model_name = embedding_model_name
        self.hardware_device = hardware_device
        self.current_directory = pathlib.Path().resolve()
        self.description_dataset_path = os.path.join(self.current_directory, 'superhero_desc_updated.gzip')
        self.hnsw_index_path = os.path.join(self.current_directory, 'hnswlib.index')
        
        logging.info(f'Loading Artifacts ...')
        
        # check if the following files available:
        for item in [self.description_dataset_path, self.hnsw_index_path]:
            if not os.path.exists(item):
                logging.error(f'File: {item} Not Found in the location. Please check!')
        
        # Load the necessary artifacts:
        self.description_data = pd.read_parquet(self.description_dataset_path)
        self.hnsw_index = hnswlib.Index(space = 'cosine', dim = self.embedding_size)
        
        logging.info(f'Dataset Exists: {os.path.exists(self.description_dataset_path)}\nHNSW Index Exists: {os.path.exists(self.hnsw_index_path)}')
        
        logging.info("Loading HNSW index for Semantic Search")
        self.hnsw_index.load_index(self.hnsw_index_path)
        
        logging.info(f'Loaded HNSW Index. Now Setting  EFT')
        
        # Controlling the recall by setting ef:
        # ef should always be > top_k_hits
        self.hnsw_index.set_ef(50)
        
        logging.info("Loading Embedding Model for Vectorisation")
        self.embedding_model = SentenceTransformer(self.embedding_model_name, 
                                                   device=self.hardware_device)
        
        logging.info(f'Done!')
    
    
    def text_similarity(self, keyword:str, text_token:str) -> int:
        # Compute text similarity between keyword and description word token
        sim = textdistance.ratcliff_obershelp.normalized_similarity(keyword, text_token)
        return 1 if sim >= self.keyword_similarity_threshold else 0
    
    
    def tokenisation(self, text:str) -> list:
        # Clean words and tokenise the text
        text = re.sub(' ', '-', text)
        text = text.split(',')
        clean_text = []
        for token in text:
            if token.startswith('-'):
                clean_text.append(token.replace('-', ''))
            else:
                clean_text.append(token)
        text = re.sub('-', ' ', " ".join(clean_text))
        return text.split(' ')
    
    
    def run_semantic_search(self) -> list:
        
        # Perform semantic search and get the document ids
        
        inp_hero_des_embedding = self.embedding_model.encode(self.description_text)
        corpus_ids, distances = self.hnsw_index.knn_query(inp_hero_des_embedding, 
                                                          k=self.semantic_search_top_k)
        
        hits = [{'corpus_id': id, 'score': 1-score} for id, score in zip(corpus_ids[0], distances[0])]
        hits = sorted(hits, key=lambda x: x['score'], reverse=True)
        
        doc_ids = []
        for hit in hits[0:self.semantic_search_top_k]:
            doc_ids.append(hit['corpus_id'])
        return doc_ids
        
    
    def run_keyword_search(self, doc_ids:list) -> list:
        # Build a dictionary which has {'document id': Number of keywords present}
        
        freq_score_board = {}
    
        input_desc_keywords = self.description_text.split(',')
        
        # take a input description keyword and search it in the exiting description dataset
    
        for row_index in doc_ids:
            des_doc = self.description_data.iloc[row_index]['hero_description']
            des_doc_tokens = self.tokenisation(des_doc)
            bit_arry = []
            for key in input_desc_keywords:
                for des_doc_token in des_doc_tokens:
                    bit_arry.append(self.text_similarity(keyword=key, text_token=des_doc_token))
            
            freq_score_board[row_index] = sum(bit_arry)
        
        sorted_freq = {k: v for k, v in sorted(freq_score_board.items(), 
                                               key=lambda item: item[1], reverse=True)}
        
        superhero_names = []
        for index, doc_id in enumerate(sorted_freq.keys()):
            if index >= self.keyword_search_top_k:
                break
            superhero_names.append(self.description_data.iloc[doc_id]['hero_name'])
        return superhero_names
        
    
    def run_pipeline(self, description_text: str) -> list:
        self.description_text = description_text.lower()
        document_ids = self.run_semantic_search()
        result = self.run_keyword_search(doc_ids = document_ids)
        return result
        

if __name__ == '__main__':
    # device = mps for Apple M1 Macs
    search_pipeline = SearchDescriptionPipeline(hardware_device='cpu')
    input_dec = 'marvel comics, male, hero, spider powers, new york city, super strength, durability, enhanced senses'
    superhero_guess = search_pipeline.run_pipeline(description_text=input_dec)
    print(f'Input Description: {input_dec}\nGuess: {superhero_guess}')
        