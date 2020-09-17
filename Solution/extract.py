import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
with open('D:\Yogabar\Solution\product_data.json') as file:
    product_data = json.load(file)

reviews = []              #stores reviews of all review pages (1-2-3...)
url = product_data["url"] #the given url of the product reviews page (https://www.amazon.in/Yogabar-Wholegrain-Breakfast-Muesli-Fruits/product-reviews/B07M6KZQCN)
asin_number = url[-10:]   #ASIN = B07M6KZQCN, extracts last 10 characters of "url"
cookie = {}                 
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}


def GetReviewContent(url):  #function which returns page content taking any url as a parameter
    page = requests.get(url,cookies=cookie,headers=header)
    if page.status_code == 200:
        return page
    else:
        return "Error"

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
        return "Error"

link = GetAllReviewsLink(asin_number)

""" 
for k in range(100):   
    response = GetReviewContent(link +'&pageNumber='+str(k))
    soup = BeautifulSoup(response.content)
    for i in soup.findAll("span",{'data-hook':"review-body"}):
        reviews.append(i.text)
"""

print(link)

"""
rev_dict = {'reviews':reviews}                  #converting the reviews list into a dictionary
review_data = pd.DataFrame.from_dict(rev_dict)  #converting this dictionary into a dataframe
review_data.to_csv('scraped_reviews_data.csv',index=False)

print(review_data.sample(10))
#https://www.amazon.in/Yogabar-Wholegrain-Breakfast-Muesli-Fruits/product-reviews/B07M6KZQCN/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews

"""