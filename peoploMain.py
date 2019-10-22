import requests
from bs4 import BeautifulSoup
import csv
import time

def get_htm(url):
    R = requests.get(url)
    return R.text

def get_pages(html):
    #ЛУЧШЕ ПРОВЕРЯТЬ ЗНАЧЕНИЯ КЛАССОВЫХ ЛИТЕРАЛОВ
    time.sleep(1)
    pages = []
    soup = BeautifulSoup(html, "html.parser")
    pages_name = soup.find_all('a', class_="icMQ_ YYC5F f-test-link- _3dPok")
    obraovans = []
    experienses = []
    ages = []
    compensations = []
    #print(pages_name)
    ############################################
    try:
        for i in range(len(pages_name)):
            ########зарплата##########
            compensations.append("".join(pages_name[i].find('span', class_="_3mfro _3Q_Pz _1ZlLP _2JVkc")
                                     .find("span").find_all("span")[0].text.split()))
            ##########################
            ########возраст###########
            if len(pages_name[i].find('span', class_="_3mfro _9fXTd _2JVkc _3e53o").find("span").find_all("span")) > 0:
                ages.append(pages_name[i].find('span', class_="_3mfro _9fXTd _2JVkc _3e53o").find("span")
                        .find_all("span")[0].text.split(" ")[0])
            else:
                ages.append("30")
            ##########################
            #########опыт работы#######
            opt_buf = pages_name[i].find('span', class_="_3mfro _9fXTd _2JVkc _3Ll36").find("span")
            int_buf = 0
            if opt_buf:
                if len(opt_buf) > 0:
                    opt_buf = opt_buf.text
                    opt_list = opt_buf.split()
                    for i in range(0, len(opt_list)):
                        if i == 0 and opt_list[i].isdigit() and len(opt_list) > 2:
                            int_buf = int(opt_list[i])*12
                        else:
                            if i == 0 and opt_list[i].isdigit() and len(opt_list) > 1:
                                if opt_list.count("год") != 0 or opt_list.count("лет") != 0 or opt_list.count("года") != 0:
                                    int_buf = int(opt_list[i])*12
                                else:
                                    int_buf = int(opt_list[i])
                        if i > 2 and opt_list[i].isdigit():
                            int_buf += int(opt_list[i])
                    experienses.append(int_buf)
                else:
                    experienses.append("0")
            else:
                experienses.append("0")
            #########################
            #########образование######
            url1 = "https://www.superjob.ru" + pages_name[i].get("href")
            soup1 = BeautifulSoup(get_htm(url1), "html.parser")
            obrs = soup1.find_all('div', class_="_3mfro _9fXTd _2JVkc _3e53o _3LJqf _15msI")
            mstr = ''.join(map(str, obrs))
            obraa = 0
            if mstr.find("Среднее специальное образование") != -1:
                obraa = 1
            if mstr.find("Высшее образование") != -1:
                obraa = 2
            obraovans.append(obraa)
            ##############################
    except:
        print("error")
        pass
    ###########Итог########################
    for k in range(len(ages)):
        if len(compensations) > k and len(experienses) > k and len(obraovans) > k:
            pages.append({"age": ages[k], "experience": experienses[k]
                             , "obrazovan":obraovans[k], "compensations": compensations[k]})
    return pages


def write_csv1(data):
    with open("ITschnimi.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(("#",data["age"], data["experience"], data["obrazovan"], data["compensations"]))

def write_csv2(data):
    with open("Drivers.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow(("#",data["age"], data["experience"], data["obrazovan"], data["compensations"]))
def write_csv3(data):
    with open("ExpertDoctors.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow(("#", data["age"], data["experience"], data["obrazovan"], data["compensations"]))
def write_csv4(data):
    with open("Tourizm.csv",'a') as f:
        writer = csv.writer(f)
        writer.writerow(("#",data["age"], data["experience"], data["obrazovan"], data["compensations"]))

#########################################################################
#########################################################################
f1=open("ITschnimi.csv",'w')
#f2=open("Drivers.csv",'w')
#f3 = open("ExpertDoctors.csv", 'w')
#f4=open("Tourizm.csv",'w')

writer = csv.writer(f1)
#writer = csv.writer(f2)
#writer = csv.writer(f3)
#writer = csv.writer(f4)
writer.writerow(("#age", "#opit", "#obrazovan", "#zp"))

f1.close()
#f2.close()
#f3.close()
#f4.close()


for i in range(1, 100):
    print(i)
    url1 = "https://www.superjob.ru/resume/search_resume.html?payment_no_agreement=1&catalogues%5B0%5D=33&t%5B0%5D=4&page="+str(i)
    #url2 = "https://www.superjob.ru/resume/search_resume.html?payment_no_agreement=1&catalogues%5B0%5D=86&t%5B0%5D=4&page="+str(i)
    #url3 = "https://www.superjob.ru/resume/search_resume.html?payment_no_agreement=1&catalogues%5B0%5D=136&t%5B0%5D=4&page=" + str(i)
    #url4 = "https://www.superjob.ru/resume/search_resume.html?payment_no_agreement=1&catalogues%5B0%5D=197&t%5B0%5D=4&page="+str(i)

    pages1 = get_pages(get_htm(url1))
    #print(pages1)
    # pages2 = get_pages(get_htm(url2))
    #pages3 = get_pages(get_htm(url3))
    #pages4 = get_pages(get_htm(url4))
    for j1 in pages1:
        write_csv1(j1)
    #for j2 in pages2:
    #    write_csv2(j2)
    #for j3 in pages3:
    #    write_csv3(j3)
    #for j4 in pages4:
    #     write_csv4(j4)
    print("finish step")
print("finish")


