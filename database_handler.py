import pandas as pd

#loading data from confluence
def load_confluence_data(filepath):
    df = pd.read_json(filepath, orient="records")

    #cleaning
    df["question_text"] = (
        df["question_text"]
        .str.strip()
        .str.lower()
    )

    #cleaning
    df["answer_text"] = (
        df["answer_text"]
        .str.strip()
    )

    df["question_id"] = (
        df["question_id"]
        .str.strip()
    )

    return df

def load_form_data(filepath):
    df = pd.read_json(filepath, orient="records")

    df["question_text"] = df["question_text"].str.strip().str.lower()

    return df

#question list
def get_questions_list(df):
    return df["question_text"].tolist()

#index list
def get_row_index(df, index):
    return df.iloc[index]

