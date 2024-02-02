import pdfplumber
import json
import string
# Convert pdf to string
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text()
    return text_content

#Remove Punctutations
def remove_punctuation(text_content):
    #Translation table
    translation_table = str.maketrans("", "", string.punctuation)
    result_string = text_content.translate(translation_table)

    return result_string

def convert_txt(text_content):
    text_content=remove_punctuation(text_content)
    final_txt=text_content.split("\n")
    final_txt= [value for value in final_txt if value]
    return final_txt

if __name__ == "__main__":
    pdf_path =( r"C:\Users\parth\OneDrive\Desktop\BFB\Nestle_Catalogue_web.pdf")
    text_content = extract_text_from_pdf(pdf_path)
    final_txt=convert_txt(text_content)

   
    
    json_file_path =(r"C:\Users\parth\OneDrive\Desktop\BFB\Nestle_Catalogue_web.json")
    
    with open(json_file_path, "w") as json_file:
        json.dump(final_txt, json_file, indent=2)
    
    print(f"Data extracted and saved to '{json_file_path}'.")

    '''for i in range(len(final_txt)):
        print(final_txt[i])
        if i%3==0:
            print('\t')'''
        
        