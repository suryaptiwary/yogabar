from lxml import html
import json
import pandas as pd
import requests
import json, re
from dateutil import parser as dateparser
from time import sleep
from extract_review_text import link

total_reviews = 882       #number of reviews (assumed from product page)
cookie = {}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}

def GetAdditionalData(link):  #extracts rating, review header, review posted date and author name and returns them as a dictionary
  page = requests.get(link, headers = header, cookies = cookie)
  page_response = page.text

  parser = html.fromstring(page_response)

  XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
  XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

  reviews = parser.xpath(XPATH_REVIEW_SECTION_1)

  if not reviews:
      reviews = parser.xpath(XPATH_REVIEW_SECTION_2)

  reviews_list = []

  if not reviews:
      raise ValueError('Unable to find reviews')

      
  for review in reviews:  
      
      #parsing individual reviews
      XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
      XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
      XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
      XPATH_AUTHOR  = './/span[contains(@class,"profile-name")]//text()'

      raw_review_author = review.xpath(XPATH_AUTHOR)
      raw_review_rating = review.xpath(XPATH_RATING)
      raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
      raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
    
      #cleaning parsed data
      author = ' '.join(' '.join(raw_review_author).split())
      review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
      review_header = ' '.join(' '.join(raw_review_header).split())
      review_posted_date = dateparser.parse(timestr = ' '.join((''.join(raw_review_posted_date).split())[-3:])).strftime('%d %B %Y')
      
      review_dict = {
                'review_posted_date':review_posted_date,
                'review_header':review_header,
                'review_rating':review_rating,
                'review_author':author
              }
      reviews_list.append(review_dict)
  
  return reviews_list

extracted_data = []   #stores list of all reviews (from all review pages) stored as dictionary

for k in range(total_reviews//10): #extracts additional review data from all pages, assuming each page contains 10 reviews
  data = GetAdditionalData(link+'&pageNumber='+str(k))
  for review in data:
        extracted_data.append(review)
 
df = pd.DataFrame(extracted_data) #converts list of dictionaries to dataframe
df.to_csv('add_review_data.csv',index=False) #converts dataframe to csv

