
import time
import sys
import requests

start_time = time.time()  # timer

URL_AJAX = "https://www.104.com.tw/company/ajax/"
HEADERS = { 
   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
   'Host': 'www.businessweekly.com.tw',
   'Referer': 'https://www.104.com.tw/',
   }

def get_total_pages(keyword):
    total_pages_num = requests.get(
        URL_AJAX + "list?keyword={}".format(keyword),
        # URL_AJAX + f"list?keyword={keyword}", # added in Python 3.6+ only
        headers = HEADERS
        ).json()['metadata']['pagination']['lastPage'] + 1
    return total_pages_num
    
def get_json_data(keyword, total_pages_num):
    company_data_list = []
    for page in range(1, total_pages_num):
        json_dict_data = requests.get(
            URL_AJAX + "list?keyword={}&page={}".format(keyword,page),
            # URL_AJAX + f"list?keyword={keyword}&page={page}",
            headers = HEADERS,
            ).json()['data']
        if json_dict_data == None:
            continue
        company_data_list.extend(json_dict_data)
    return company_data_list

def get_company_info(company_data_list):
    company_id_list = [company['encodedCustNo'] for company in company_data_list]
    company_name_list = [company['name'] for company in company_data_list]
    company_profile_list = [company['profile'].replace('\r','').replace('\n','').replace('\u3000','').replace('\uf06c','') for company in company_data_list]
    return company_id_list, company_name_list, company_profile_list

def get_company_product(company_id_list):
    company_product_list = []
    for company_id in company_id_list:
        company_product = requests.get(
            URL_AJAX + "content/{}".format(company_id),
            # URL_AJAX + f"content/{company_id}",
            headers = HEADERS,
            ).json()['data']['product'].replace('\n','').replace('\r','').replace('\u3000','').replace('\uf06c','').replace('\t','')
            # .replace('\xa0','')
        company_product_list.append(company_product)
    return company_product_list

if __name__ == '__main__':
    keyword = sys.argv[1]
    total_pages_num = get_total_pages(keyword)
    company_data_list = get_json_data(keyword, total_pages_num)
    company_id_list = get_company_info(company_data_list)[0]
    company_name_list = get_company_info(company_data_list)[1]
    company_profile_list = get_company_info(company_data_list)[2]
    company_product_list = get_company_product(company_id_list)
    result = list(zip(company_id_list, company_name_list, company_profile_list, company_product_list))
    print(result)


print("Cost：" + str(time.time() - start_time) + " s")