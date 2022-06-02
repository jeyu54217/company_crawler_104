import pandas as pd
import os
import csv
import time
import openpyxl

SOURCE_PATH = 'D:\\TreasurePreWork\\SourceData\\'
OUTPUT_PATH = 'D:\\TreasurePreWork\\OutputData\\'

start_time = time.time() 
def get_data():
    items_in_dir = os.listdir(SOURCE_PATH)
    for filename in items_in_dir: # loop through items in dir
        # 全國營業(稅籍)登記資料集
        if filename == "BGMOPEN1.csv": 
            df = pd.read_csv(SOURCE_PATH + filename, converters={u'統一編號':str, u'資本額':str})
            tax_id_list = df['統一編號'].values.tolist()[1:]
            company_tax_name = df['營業人名稱'].values.tolist()[1:]
            company_address = df['營業地址'].values.tolist()[1:]
            company_capital = df['資本額'].values.tolist()[1:]
            # print(company_address)

            print(len(tax_id_list),len(company_tax_name),len(company_address),len(company_capital),)
            # pass



        # # 全國營業(稅籍)登記(停業)資料集
        # elif filename == "BGMOPEN1X.csv": 
        #     with open(SOURCE_PATH + filename, encoding="utf-8") as csvfile:
        #         reader = csv.reader(csvfile)
        #         out_of_business_id_list = [row[1] for row in reader]
        # # 全國營業(稅籍)登記(停業以外之非營業中)資料集
        # elif filename == "BGMOPEN1Y.csv": 
        #     with open(SOURCE_PATH + filename, encoding="utf-8") as csvfile:
        #         reader = csv.reader(csvfile)
        #         not_open_id = [row[1] for row in reader]
        #         print( not_open_id)
        # # RM_TABLE
        # elif filename == "RM_TABLE_20220412.xlsx":
        #     df = pd.read_excel(SOURCE_PATH + filename, converters={u'Customer_ID':str})
        #     RM_customer_id_list = df['Customer_ID'].values.tolist()
        #     RM_channel_chi_desc_list = df['Channel_Chi_Desc'].values.tolist()
        #     print(RM_channel_chi_desc_list)
        # else:
        #     print('FileNameError: Please check your source file name') 



#   grade_list = []
#             #read csv file
#             with open(csv_file.file_name.path, 'r') as file:
#                 reader = csv.reader(file)

#                 for i, row in enumerate(reader):
#                     if i == 0:
#                         pass
#                     else:
#                         subject = Subject.objects.get(subject_name = row[3])
#                         profile = get_object_or_404(StudentProfile, LRN_or_student_number = row[0])

#                         new_grade = StudentGrade(
#                             student=profile.student.student,
#                             period = period,
#                             subject = subject,
#                             grade = row[4],
#                             )

#                         grade_list.append(new_grade)

#                         # this is slow
#                         # new_grade = StudentGrade.objects.create(
#                         #     student=profile.student.student,
#                         #     period = period,
#                         #     subject = subject,
#                         #     grade = row[4],
#                         #     )
#                 new_grades = StudentGrade.objects.bulk_create(grade_list)








#  queryset = Book.objects.all()

#     # Check the books table is empty or not

#     if queryset.exists() == False:

#        # Insert 5 records in the books table at a time

#         Book.objects.bulk_create([

#             Book(title='Python Crash Course, 2nd Edition', author='Eric Matthes', price=15, published_year=2019),

#             Book(title='Automate the Boring Stuff with Python, 2nd Edition', author='Al Sweigart', price=30,

#                   published_year=2019),

#             Book(title='Learning Python', author='Mark Lutz', price=15, published_year=2019),

#             Book(title='Head First Python', author='Paul Barry', price=45, published_year=2016),

#             Book(title='A Byte of Python', author='Swaroop C H', price=15, published_year=2013),


#         ])


if __name__ == '__main__':
    get_data()

print("Cost：" + str(time.time() - start_time) + " s")

