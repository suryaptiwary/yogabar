import pandas as pd
import requests
import json, re
from bs4 import BeautifulSoup

with open("D:/Yogabar/Solution/data/assignment_data.json") as file:
    product_data = json.load(file)

total_reviews = 882       #number of reviews (assumed from product page)
reviews = []              #stores individual review text of all review pages (1-2-3...)
url = product_data["url"] #the given url of the product reviews page (https://www.amazon.in/Yogabar-Wholegrain-Breakfast-Muesli-Fruits/product-reviews/B07M6KZQCN)
asin_number = url[-10:]   #ASIN = B07M6KZQCN, extracts last 10 characters of "url"
cookie = {}                 
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def GetReviewContent(url):  #function which returns page content taking any url as a parameter
    page = requests.get(url,cookies=cookie,headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Not Found"

def GetAllReviewsLink(asin): #function which returns "see all reviews" link taking ASIN as parameter
    all_reviews_link = ""
    url = "https://www.amazon.in/dp/"+asin
    page = requests.get(url, cookies=cookie, headers=header)
    if page.status_code==200:
        soup = BeautifulSoup(page.content)
        for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
            all_reviews_link = "https://www.amazon.in"+i['href']
        return all_reviews_link
    else:
        return "Not Found"

link = GetAllReviewsLink(asin_number) #https://www.amazon.in/Yogabar-Wholegrain-Breakfast-Muesli-Fruits/product-reviews/B07M6KZQCN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews

for k in range(total_reviews//10):   #extracts review text from all pages, assuming each page contains 10 reviews
    response = GetReviewContent(link +'&pageNumber='+str(k)) #adding '&pageNumber=k' to 'link' to parse each review page
    soup = BeautifulSoup(response.content)
    for i in soup.findAll("span",{'data-hook':"review-body"}):
        reviews.append(i.text)
     
rev_dict = {'reviews':reviews}                  #converts the reviews list into a dictionary
review_data = pd.DataFrame.from_dict(rev_dict)  #converts this dictionary into a dataframe
review_data.to_csv('review_text_data.csv',index=False)  #converts the dataframe to csv


