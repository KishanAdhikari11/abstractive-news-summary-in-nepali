import pandas as pd
import csv
def split_paragraph(paragraph):
    sentences = paragraph.split(". ")  
    result = []
    current_chunk = ''
    char_count = 0

    for sentence in sentences:
        sentence += '. '  
        if (char_count + len(sentence)) <= 800:
            current_chunk += sentence
            char_count += len(sentence)
        else:
            for i in range(len(sentence)):
                if (char_count + i) >= 200 and sentence[i] == '.':
                    current_chunk += sentence[:i+1]
                    result.append(current_chunk.strip())
                    current_chunk = sentence[i+1:]
                    char_count = len(current_chunk)
                    break
    if current_chunk:
        result.append(current_chunk.strip())

    return result

def iterate_through_csv(df,output_file):
    with open(output_file,'a') as f:
        for _,row in df.iterrows():
            paragraph=row['Article']
            split_paragraphs = split_paragraph(paragraph)
            f.write(str(split_paragraphs))
            f.write("\n")

df=pd.read_csv("republica>1000.csv")
iterate_through_csv(df,"republica.txt")
            
        
