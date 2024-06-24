#imports
import re
from PIL import Image
from pytesseract import pytesseract

#set the path to the tesseract executable
tesseract_path = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.tesseract_cmd = tesseract_path


#clean up text data from ocr
def clean_text(text):
    '''Accepts the string of text data produced by OCR.
    
    Returns a list of strings, each string being one line of the invoice document.'''
    return [line for line in text.split('\n') if line != '']


#extract text from set of invoices
def extract_text(file_list, ocr=pytesseract):
    '''Accepts a list of files, where each file is an image of an invoice.
    
    Returns a list of dictionaries, where each dictionary contains the filename and the text data.'''
    file_text = []
    
    for file in file_list:
        file_info = {}

        text = ocr.image_to_string(file)
        text = clean_text(text)

        file_info['file'] = file
        file_info['text'] = text
        
        file_text.append(file_info)

    return file_text


#large function to extract addresses
def extract_addresses(file_info):
    '''Accepts the list of dictionaries containing filename and text.
    
    Returns the list with the extracted addresses for each document.'''
    regexp_one = r'\d+ [a-zA-Z0-9\.\s]+? [a-zA-Z\.]+'
    regexp_two = r'[a-zA-Z\s]+, [A-Z]{2} \d{5}'
    regexp_full = r'\d+ [a-zA-Z0-9\.\s]+? [a-zA-Z\.]+,? ([a-zA-Z]\s?)+, [A-Z]{2} \d{5}'

    for file in file_info:
        addresses = []
        for i, line in enumerate(file['text']):
            second_half = re.findall(regexp_two, line)
            if second_half:
                if len(second_half) == 1:
                    full_address = re.search(regexp_full, line)
                    if full_address:
                        addresses.append(full_address)
                    else:
                        try:
                            first_half = re.search(regexp_one, file['text'][i-1]).group(0)
                            full_address = first_half + ', ' + second_half[0]
                            addresses.append(full_address)
                        except:
                            continue
                elif len(second_half) == 2:
                    first_halves = re.findall(regexp_one, file['text'][i-1])
                    try:
                        address_one = first_halves[0] + ', ' + second_half[0]
                        address_two = first_halves[1] + ', ' + second_half[1]
                        addresses.append(address_one)
                        addresses.append(address_two)
                    except:
                        continue
                else:
                    continue
        file['addresses'] = addresses

    return file_info                        


#pipeline function
def get_addresses(file_list):
    '''Pipeline function that accepts a list of invoice image files.
    
    Returns a list of dictionaries, with each dictionary containing the filepath, text, and addresses.'''
    text = extract_text(file_list)

    return extract_addresses(text)