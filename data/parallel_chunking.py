"""
    PARALLEL CHUNKING AND PROCESSING:
- THIS IS SUITED TO THE PARTICULAR PROBLEM IN THREAT INTELLIGENCE I WAS SOLVING
    - THE CHUNKING CODE IS NOT GENERALISED YET.
- CHUNKING A DATAFRAME
- EXECUTING IN PARALLEL USING MULTIPROCESSING
   - NOTE: THERE ARE VARIOUS OTHER WAYS TO ACHIEVE THIS PLS EXPLORE
   - I WANTED TO KEEP IT AS PYTHONIC AS POSSIBLE

"""

import multiprocessing
import numpy as np
import pandas as pd
from notebook_logging import setup_logging
# @TODO CHUNKING A DATAFRAME GENERALLY!
logger = setup_logging()

def process_dataframe_chunk(df_chunk):
    """_summary_

    Args:
        df_chunk (pd.DataFrame): A Dataframe to be chunked by the applied text and named functions

    Returns:
        pd.DataFrame: Processed Data frame for parallel execution
    """
    # Apply all your processing functions here
    df_chunk["text"] = df_chunk["text"].progress_apply(reduce_text)
    df_chunk['attack_patterns'] = df_chunk['entities'].progress_apply(isolate_attack_patterns)
    df_chunk['features_found'] = df_chunk['entities'].progress_apply(extract_features)
    df_chunk['threat_labels'] = df_chunk['entities'].progress_apply(isolate_labels)
    df_chunk['one_hot_labels'] = df_chunk['threat_labels'].progress_apply(one_hot)
    df_chunk["tokens"] = df_chunk["text"].progress_apply(tokenize_text)
    logger.info("{} rows processed".format(len(df_chunk)))
    return df_chunk

def parallel_execution(df):
    """Executes the parallel execution of a set of functions using the multiprocessing library
        and putting them onto the device

    Args:
        df (pd.DataFrame): A processed data frame

    Returns:
        df (pd.DataFrame): A p
    """
    # Split dataframe into chunks for parallel processing
    num_partitions = multiprocessing.cpu_count()
    df_split = np.array_split(df, num_partitions)

    # Create multiprocessing pool
    pool = multiprocessing.Pool(num_partitions)
    df_processed_list = pool.map(process_dataframe_chunk, df_split).to(device)
    pool.close()
    pool.join()

    # Concatenate all chunks back into a single DataFrame
    df_processed = pd.concat(df_processed_list).to(device)
    return df_processed
