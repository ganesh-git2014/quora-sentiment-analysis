'''
convert files from
commonmark, docbook, docx, epub, haddock, html, json, latex, markdown,
markdown_github, markdown_mmd, markdown_phpextra, markdown_strict, mediawiki, native, odt, opml, org, rst, t2t, textile, twiki

'''


import urllib.request
import pypandoc
import time
from nltk import word_tokenize
from nltk.corpus import stopwords
import re
import urllib.request
from bs4 import BeautifulSoup


stop_words = set(stopwords.words('english'))

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True
 
def valid_link_text(url,query_flag = 1):
    try:
        cleaned = urllib.request.urlopen(url)
    except urllib.error.URLError :
        print("404 : Page Not Found ")
        return False
    if query_flag == 1 :
        soup = BeautifulSoup(cleaned,"lxml")

        data = soup.findAll(text=True)
        result =  filter(visible,data)
        time.sleep(5)		# get_result
        return list(result)
    else:
        return True

def save_data(data,data_name,question_name,from_extension = None,to_extension = None,):
    if from_extension!=None:
        print("conv")
        #out = pypandoc.convert_file("temp.html",'docx',outputfile='Done.docx')

    elif to_extension!=None:
        text_file = open("texts/"+"words_answer-"+data_name+to_extension,"w")
        text_file.write(question_name)
        text_file.write("\n")
        # ignore top 10 lines 	and save in particular words
        break_point = ["Sitemap:","Related Questions"]

        for line in data[10:] :
            if line in break_point:
                break               # setting temperory break-point
            words = word_tokenize(line)

            for word in words :
                if word not in stop_words:
                    content = re.sub('\s+', ' ', word)  # condense all whitespace
                    content = re.sub('[^A-Za-z ]+', '', content)  # remove non-alpha chars
                    text_file.write(str(content).lower())
                    text_file.write("\n")

        text_file.close()
    else:
        print(" Invalid conversion ! ")

def get_answer_blog():
    start_url = input("Enter answer / blog url :")
    # start_url = "https://www.quora.com/profile/Aman-Goel-9"
    text_data = valid_link_text(start_url)
    if text_data == False:
        return
    # print(text_data)
    c = 1
    save_data(text_data,data_name=str(c),to_extension=".txt")
    #for line in soup.findAll('span',{'class':'rendered_qtext'}):
    print("grabbed answer / blog successfully")

def get_latest_questions(url):
    raw = urllib.request.urlopen(url)
    soup = BeautifulSoup(raw, "lxml")

    data = soup.findAll('span',{"class":"rendered_qtext"})
    result = filter(visible, data)
    time.sleep(2)  # get_result
    data  = list(result)
    question_bag = []
    for it in data:
        txt = str(it.text)
        txt.lower()
        if "?" in txt:
            txt = txt[:-1].replace(' ','-')             # get re here to refine
            question_bag.append("http://quora.com/"+txt)
    print("grabbed question_bag successfully ")
    return question_bag


def get_latest_answers():

    start_url= input("Enter profile link :")

    text_data = valid_link_text(start_url,query_flag=0)
    if text_data == False:
        return
    questions = get_latest_questions(start_url)
    size = len(questions)
    for question in range(size):
        validity = valid_link_text(questions[question])
        print(questions[question])
        print("got - #"+str(question+1))
        if validity != False:
            save_data(validity,data_name=str(question+1),to_extension=".txt",question_name=questions[question])
        else:
            print("Validate question_bag link index #"+str(question+1))
    print("grabbed answers successfully")


if __name__ == "__main__":
    #get_answer_blog()
    get_latest_answers()