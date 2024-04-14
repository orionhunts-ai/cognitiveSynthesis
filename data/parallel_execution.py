"""
    PARALLEL CHUNKING AND PROCESSING:
- THIS IS SUITED TO THE PARTICULAR PROBLEM IN THREAT INTELLIGENCE I WAS SOLVING
    - THE CHUNKING CODE IS NOT GENERALISED YET.
- CHUNKING A DATAFRAME
- EXECUTING IN PARALLEL USING MULTIPROCESSING
   - NOT: THERE ARE VARIOUS OTHER WAYS TO ACHIEVE THIS PLS EXPLORE
   - I WANTED TO KEEP IT AS PYTHONIC AS POSSIBLE

"""

import multiprocessing
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm


def parallel_execution_function(df):
    """
    Executes the parallel processing of a DataFrame using the multiprocessing library.

    Args:
        df (pd.DataFrame): The input DataFrame to process.

    Returns:
        pd.DataFrame: The processed DataFrame.
    """
    # Split dataframe into chunks for parallel processing
   
    num_partitions = multiprocessing.cpu_count()
    df_split = np.array_split(df, num_partitions)

    # Create a multiprocessing pool using a context manager (advised by Docs)
    with multiprocessing.Pool(num_partitions) as pool:
        df_processed_list = pool.map(process_dataframe_chunk, df_split)

    # Concat all chunks to a DatafRame
    df_processed = pd.concat(df_processed_list)
    return df_processed

def process_dataframe_chunk(df_chunk):
    """_summary_

    Args:
        df_chunk (pd.DataFrame): A Dataframe to be chunked by the applied text and named functions

    Returns:
        pd.DataFrame: Processed Data frame for parallel execution
    """
    print(df_chunk)
    # progress_apply using pandas.
    df_chunk['attack_patterns'] = df_chunk['entities'].progress_apply(isolate_attack_patterns)
    df_chunk['features_found'] = df_chunk['entities'].progress_apply(extract_features)
    df_chunk['threat_labels'] = df_chunk['entities'].progress_apply(isolate_labels)
    df_chunk["text"] = df_chunk.progress_apply(reduce_text)
    df_chunk['one_hot_labels'] = df_chunk['threat_labels'].progress_apply(one_hot)
    df_chunk["tokens"] = df_chunk["text"].progress_apply(tokenize_text)
    
    return df_chunk


