import pandas as pd
import numpy as np
import string

def aikenize_pairing_csv(csv_path, aiken_path, number_of_choices = 5,  number_of_questions = None, fix_col = "LATIN", choice_col = "HUN", delimiter = ";", verbose = True):
  assert number_of_choices >= 1

  answer_chars = np.array([c for c in string.ascii_uppercase[:number_of_choices]])
  
  pairing_df = pd.read_csv(csv_path, delimiter= delimiter).dropna(axis=0,how="any").reset_index(drop=True)
  
  choice_pool = np.array(pairing_df[choice_col].to_list()) 
  
  pairing_df = pairing_df.sample(frac=1, replace=False).reset_index(drop=True)
  if isinstance(number_of_questions,type(None)):
    number_of_questions = len(pairing_df.index)
  
  pairing_df = pairing_df.head(number_of_questions)

  aiken_list = []
  for index, row in pairing_df.iterrows():
    question = row[fix_col]
    right_answer = row[choice_col]
    possible_answers = [right_answer]
    possible_answers.extend(np.random.choice(choice_pool[choice_pool!=right_answer], number_of_choices-1, replace=False).tolist())
    possible_answers = np.random.permutation(possible_answers)
    right_answer_char = answer_chars[np.where(possible_answers==right_answer)][0]

    aiken_list.append(question)
    if verbose: print(question)

    for answer_char, answer in zip(answer_chars,possible_answers):
      aiken_answer_row = f"{answer_char}. {answer}"
      aiken_list.append(aiken_answer_row)
      if verbose: print(aiken_answer_row)

    aiken_answer_row = f"ANSWER: {right_answer_char}"
    aiken_list.append(aiken_answer_row)
    if verbose:print(aiken_answer_row)
  
  with open(aiken_path,"w") as aiken:
    aiken.writelines("\n".join(aiken_list))
      


if __name__ == "__main__":
  latin_path = "examples/latin.csv"
  out_path = "examples/latin_aiken.txt"
  aikenize_pairing_csv(latin_path, out_path)
