from django.shortcuts import render
from .clawer_104_by_AJAX import *
from .models import result_list, Company_info_closed, Company_info_gov, RM_Confirmed
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os

SOURCE_PATH = 'D:\\TreasurePreWork\\SourceData\\'

def home_page(request):
    return render(request,"search_page.html")
    # return render(request,"result_page.html")
    # return render(request,"end_page.html")

@csrf_exempt
def main_crawler(request):
    if request.method =='POST':
        # reset DB before update or create
        result_list.objects.all().delete() 
        # get posted data from js
        keyword_list = list(request.POST.getlist('key_of_kwyword_list[]')[0].split(',')) 
        for keyword in keyword_list:
            # ignore empty search
            if keyword == '':
                continue
            # run clawer
            else:
                total_pages_num = get_total_pages(keyword)
                raw_data_list = get_json_data(keyword, total_pages_num)
                company_id_list = get_company_info(raw_data_list)[0]
                company_name_list = get_company_info(raw_data_list)[1]
                company_profile_list = get_company_info(raw_data_list)[2]
                company_product_list = get_company_product(company_id_list)
                # INSERT scraped data to DB
                for i in range(0, len(company_id_list)): 
                    id = company_id_list[i]
                    name = company_name_list[i]
                    profile = company_profile_list[i]
                    product = company_product_list[i]
                    result_list.objects.update_or_create(  # only update or create but not delete
                        company_id = id,
                        company_name = name,
                        company_profile = profile,
                        company_product = product,
                        )
    context = {
            'result_list': result_list.objects.all(),
            }
    return render(request, "result_page.html", context) 

@csrf_exempt
def csv_to_db(request):
    items_in_dir = os.listdir(SOURCE_PATH)
    for filename in items_in_dir: # loop through items in dir
        # 全國營業(稅籍)登記資料集
        if filename == "BGMOPEN1.csv": 
            df = pd.read_csv(SOURCE_PATH + filename, converters={u'統一編號':str, u'資本額':str})
            tax_id_list = df['統一編號'].values.tolist()[1:]
            company_tax_name = df['營業人名稱'].values.tolist()[1:]
            company_address = df['營業地址'].values.tolist()[1:]
            company_capital = df['資本額'].values.tolist()[1:]
            # INSERT data to DB
            Company_info_gov.objects.all().delete() 
            # for i in range(0, len(tax_id_list)):
            #     Company_info_gov.objects.create(
            #         tax_id = tax_id_list[i],
            #         company_tax_name = company_tax_name[i],
            #         company_address = company_address[i],
            #         company_capital = company_capital[i],
            #     )
            obj_list = []
            for i in range(0, len(tax_id_list)): 
                obj = Company_info_gov(
                    tax_id = tax_id_list[i],
                    company_tax_name = company_tax_name[i],
                    company_address = company_address[i],
                    company_capital = company_capital[i],
                    )
                obj_list.append(obj)
            Company_info_gov.objects.bulk_create(obj_list, batch_size = 100)
            continue
            
        # RM_TABLE
        elif filename == "RM_TABLE_20220412.xlsx":
            df = pd.read_excel(SOURCE_PATH + filename, converters={u'Customer_ID':str})
            RM_customer_id_list = df['Customer_ID'].values.tolist()
            RM_channel_chi_desc_list = df['Channel_Chi_Desc'].values.tolist()
            RM_Confirmed.objects.all().delete() 
            # for i in range(0, len(RM_customer_id_list)):
            #     RM_Confirmed.objects.create(
            #         RM_confirmed_id = RM_customer_id_list[i],
            #         RM_channel_chi_desc = RM_channel_chi_desc_list[i],
            #     )
            obj_list = []
            for i in range(0, len(RM_customer_id_list)): 
                obj = RM_Confirmed(
                    RM_confirmed_id = RM_customer_id_list[i],
                    RM_channel_chi_desc = RM_channel_chi_desc_list[i],
                    )
                obj_list.append(obj)
            RM_Confirmed.objects.bulk_create(obj_list, batch_size = 100)

        # 全國營業(稅籍)登記(停業以外之非營業中)資料集
        elif filename == "BGMOPEN1Y.csv": 
            df = pd.read_csv(SOURCE_PATH + filename, converters={u'統一編號':str})
            not_open_id = df['統一編號'].values.tolist()[1:]
            not_open_name = df['營業人名稱'].values.tolist()[1:]
            Company_info_closed.objects.all().delete()  
            # for i in range(0,len(not_open_id)):
                # Company_info_gov.objects.create(
                #     not_open_id = not_open_id[i],
                #     not_open_name = not_open_name[i],
                # )
            obj_list = []
            for i in range(0, len(not_open_id)): 
                obj = Company_info_closed(
                    not_open_id = not_open_id[i],
                    not_open_name = not_open_name[i],
                    )
                obj_list.append(obj)
            Company_info_closed.objects.bulk_create(obj_list, batch_size = 100)
        else:
            continue
    return render(request, "search_page.html") 

@csrf_exempt
def save(request):
    if request.method =='POST':
        # get posted data from js
        selected_id_list = request.POST.getlist('key_of_checked_list[]')[0].replace('checkbox_','').split(',')
        note_id_list = request.POST.getlist('key_of_note_id_list[]')[0].replace('text_','').split(',')
        note_value_list = request.POST.getlist('key_of_note_value_list[]')[0].split(',')

        # Update checked in DB
        for i in range(0, len(selected_id_list)): 
            id = selected_id_list[i]
            result_list.objects.filter(company_id = id).update(checked = True,)

        # Update Remarks in DB
        for i in range(0, len(note_id_list)): 
            id = note_id_list[i]
            note = note_value_list[i]
             # ignore empty notes
            if note =='':
                continue
            else:
                result_list.objects.filter(company_id = id).update(user_note = note,)
    return render(request, "result_page.html") 


@csrf_exempt
def mapping(request):
    items_in_dir = os.listdir(SOURCE_PATH)
    for filename in items_in_dir: # loop through items in dir
        # 全國營業(稅籍)登記(停業)資料集
        if filename == "BGMOPEN1X.csv":
            df = pd.read_csv(SOURCE_PATH + filename, converters={u'統一編號':str})
            out_of_business_id_list = df['統一編號'].values.tolist()[1:]
            out_of_business_name_list = df['營業人名稱'].values.tolist()[1:]
        else:
            continue
    selected_name_list = list(result_list.objects.filter(checked = True).values_list('company_name', flat=True))  # , flat=True !!!
    company_tax_name_list = list(Company_info_gov.objects.values_list('company_tax_name', flat=True))
    not_open_name_list = list(Company_info_closed.objects.values_list('not_open_name', flat=True))

    name_not_in_list = []
    final_tax_name_list = []
    final_out_of_business_name_list = []
    final_not_open_name_list = []


    company_Id_list = []
    for name in selected_name_list:
        if name not in company_tax_name_list and name not in out_of_business_name_list and name not in not_open_name_list:
            name_not_in_list.append(name)
            company_Id_list.append('(待補)')

        elif name in company_tax_name_list:
            final_tax_name_list.append(name)
            id = Company_info_gov.objects.filter(company_tax_name = name).values('tax_id')[0]['tax_id']
            company_Id_list.append(id)

        elif name in out_of_business_name_list:
            final_out_of_business_name_list.append(name)
            id = out_of_business_id_list[out_of_business_name_list.index(name)]
            company_Id_list.append(id + '(停業)') 

        elif name in not_open_name_list:
            final_not_open_name_list.append(name)
            id = Company_info_closed.objects.filter(not_open_name = name).values('not_open_id')[0]['not_open_id']
            company_Id_list.append(id + '(非營業中)')
        else:
            continue
        

    RM_Confirmed_list = []
    RM_Channel_Chi_Desc_list = []
    for id in company_Id_list:
        if id in RM_Confirmed.objects.values_list('RM_confirmed_id'):
            RM_Confirmed_list.append('✓')
            RM_Channel_Chi_Desc_list.append(RM_Confirmed.objects.filter(RM_confirmed_id = id).values('RM_channel_chi_desc'))
        else:
            RM_Confirmed_list.append('X')
            RM_Channel_Chi_Desc_list.append('') 

    Company_Address = [Company_info_gov.objects.filter(company_tax_name = name).values('company_address')[0]['company_address'] for name in selected_name_list]
    Company_Capital = [Company_info_gov.objects.filter(company_tax_name = name).values('company_capital')[0]['company_capital'] for name in selected_name_list]
    remarks = result_list.objects.filter(checked = True).values_list('user_note', flat=True)
    

    pd_data = {
        'company_name': selected_name_list,
        'company_Id' : company_Id_list,
        'RM_Confirmed' : RM_Confirmed_list,
        'RM_Channel_Chi_Desc' : RM_Channel_Chi_Desc_list,
        'company_Address' : Company_Address,
        'company_Capital' : Company_Capital,
        'remarks': remarks,
        }

    df = pd.DataFrame(pd_data)
    # df.to_excel(f'{exel_output_path}公司清單.xlsx')
    df.to_excel('D:\公司清單.xlsx')

    context = {
            'not_in_list' : name_not_in_list ,
            } 

    return render(request, "end_page.html", context) 


@csrf_exempt
def update_mapping(request):
    # if request.method =='POST':
        updated_id_list = list(request.POST.getlist('key_of_update_ary[]')[0].split(','))
        items_in_dir = os.listdir(SOURCE_PATH)
        for filename in items_in_dir: # loop through items in dir
        # 全國營業(稅籍)登記(停業)資料集
            if filename == "BGMOPEN1X.csv":
                df = pd.read_csv(SOURCE_PATH + filename, converters={u'統一編號':str})
                out_of_business_id_list = df['統一編號'].values.tolist()[1:]
                out_of_business_name_list = df['營業人名稱'].values.tolist()[1:]
            else:
                continue
        selected_name_list = list(result_list.objects.filter(checked = True).values_list('company_name', flat=True))  # , flat=True !!!
        company_tax_name_list = list(Company_info_gov.objects.values_list('company_tax_name', flat=True))
        not_open_name_list = list(Company_info_closed.objects.values_list('not_open_name', flat=True))

        name_not_in_list = []
        final_tax_name_list = []
        final_out_of_business_name_list  = []
        final_not_open_name_list = []
        company_Id_list = []

        for name in selected_name_list:
            if name not in company_tax_name_list and name not in out_of_business_name_list and name not in not_open_name_list:
                name_not_in_list.append(name)
                company_Id_list.append('(待補)')

            elif name in company_tax_name_list:
                final_tax_name_list.append(name)
                id = Company_info_gov.objects.filter(company_tax_name = name).values('tax_id')[0]['tax_id']
                company_Id_list.append(id)

            elif name in out_of_business_name_list:
                final_out_of_business_name_list.append(name)
                id = out_of_business_id_list[out_of_business_name_list.index(name)]
                company_Id_list.append(id + '(停業)')

            elif name in not_open_name_list:
                final_not_open_name_list.append(name)
                id = Company_info_closed.objects.filter(not_open_name = name).values('not_open_id')[0]['not_open_id']
                company_Id_list.append(id + '(非營業中)')
            else:
                continue

        updated_id_dict = dict(zip(name_not_in_list, updated_id_list))
        final_dict=dict(zip(selected_name_list, company_Id_list))
        final_dict.update(updated_id_dict)
        final_name_list = list(final_dict.keys())
        final_id_list_ = list(final_dict.values())
        final_id_list = ['x' if x=='' else x for x in final_id_list_]


        RM_Confirmed_list = []
        RM_Channel_Chi_Desc_list = []
        for id in final_id_list:
            if id in RM_Confirmed.objects.values_list('RM_confirmed_id', flat=True):
                RM_Confirmed_list.append('✓')
                RM_Channel_Chi_Desc_list.append(RM_Confirmed.objects.filter(RM_confirmed_id = id).values('RM_channel_chi_desc'))
            else:
                RM_Confirmed_list.append('')
                RM_Channel_Chi_Desc_list.append('')

        Company_Address = [Company_info_gov.objects.filter(tax_id = id).values('company_address')[0]['company_address'] for id in final_id_list]
        Company_Capital = [Company_info_gov.objects.filter(tax_id = id).values('company_capital')[0]['company_capital'] for id in final_id_list]
        remarks = result_list.objects.filter(checked = True).values_list('user_note', flat=True)
    

        pd_data = {
            'company_name': final_name_list,
        
            'company_Id' : final_id_list,
        
            'RM_Confirmed' : RM_Confirmed_list,
            'RM_Channel_Chi_Desc' : RM_Channel_Chi_Desc_list,
            'company_Address' : Company_Address,
            'company_Capital' : Company_Capital,
            'remarks': remarks,
        }

        df = pd.DataFrame(pd_data)
    # df.to_excel(f'{exel_output_path}公司清單.xlsx')
        df.to_excel('D:\公司清單.xlsx')

        context = {
            'not_in_list' : name_not_in_list ,
            }
        return render(request, "end_page.html", context)









































# @csrf_exempt
# def select_to_excel(request):
#     if request.method =='POST':
#         # get posted data from js
#         exel_output_path = request.POST.getlist('key_of_output_path[]')[0] # input by user

#         selected_company_name_list = result_list.objects.filter(checked = True).values_list('company_name')
#         selected_company_id_list = []
#         for name in selected_company_name_list:
#             a = Company_info_gov.objects.filter(company_tax_name = name).values('tax_id')
#             selected_company_id_list.append(a)

# # `       selected_company_id_list = [Company_info_gov.objects.filter(company_tax_name = name).values('tax_id') for name in selected_company_name_list]
        
#         RM_Confirmed_list = []
#         RM_Channel_Chi_Desc_list = []
#         for id in selected_company_id_list:
#             if id in RM_Confirmed.objects.values_list('RM_confirmed_id'):
#                 RM_Confirmed_list.append('✓')
#                 RM_Channel_Chi_Desc_list.append(RM_Confirmed.objects.filter(RM_confirmed_id = id).values('RM_channel_chi_desc'))
#             else:
#                 RM_Confirmed_list.append('X')
#                 RM_Channel_Chi_Desc_list.append('')

#         Company_Address = [Company_info_gov.objects.filter(company_tax_name = name).values('company_address') for name in selected_company_name_list]
#         Company_Capital = [Company_info_gov.objects.filter(company_tax_name = name).values('company_capital') for name in selected_company_name_list]
#         remarks = result_list.objects.filter(checked = True).values_list('user_note')

#         # Output to Excel by pandas
#         pd_data = {
#             'company_name': selected_company_name_list,
#             'company_Id' : selected_company_id_list,
#             'RM_Confirmed' : RM_Confirmed_list,
#             'RM_Channel_Chi_Desc' : RM_Channel_Chi_Desc_list,
#             'company_Address' : Company_Address,
#             'company_Capital' : Company_Capital,
#             'remarks': remarks,
#             }
#         df = pd.DataFrame(pd_data)
#         # df.to_excel(f'{exel_output_path}公司清單.xlsx')
#         df.to_excel('D:\公司清單.xlsx')

#     return render(request, "search_page.html")




# @csrf_exempt
# def select_to_excel(request):
#     if request.method =='POST':
#         # get posted data from js
#         selected_id_list = request.POST.getlist('key_of_checked_list[]')[0].replace('checkbox_','').split(',')
#         exel_output_path = request.POST.getlist('key_of_output_path[]')[0] # input by user
#         note_id_list = request.POST.getlist('key_of_note_id_list[]')[0].replace('text_','').split(',')
#         note_value_list = request.POST.getlist('key_of_note_value_list[]')[0].split(',')

#         # Update Remarks in DB
#         for i in range(0, len(note_id_list)): 
#             id = note_id_list[i]
#             note = note_value_list[i]
#              # ignore empty notes
#             if note =='':
#                 continue
#             else:
#                 result_list.objects.filter(company_id = id).update(user_note = note,)

#         # Checkbox & Excel output operations 
#         if selected_id_list == ['']: # ignore no checkbox selected
#             pass
#         else:
#             # pk lookup, return Querrysets which map to the pk list.
#             all_seleted_obj = result_list.objects.filter(company_id__in = selected_id_list)
#             # Output to Excel by pandas
#             pd_data = {
#                 'Company_Name': [obj.company_name for obj in all_seleted_obj],
#                 'Company_Id' : [],
#                 'RM_Confirmed' : [],
#                 'RM_Channel_Chi_Desc' : [],
#                 'Company_Address' : [],
#                 'Company_Capital' : [],
#                 'Remarks': [obj.user_note for obj in all_seleted_obj],
#             }
#             df = pd.DataFrame(pd_data)
#             df.to_excel(f'{exel_output_path}公司清單.xlsx')

#     return render(request, "search_page.html")

