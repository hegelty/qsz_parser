import requests
from bs4 import BeautifulSoup

output_file = open("output.txt", "w")
output_file2 = open("output2.txt", "w")


def find_compuzonelink(id):
    url = "https://quasarzone.com/bbs/qc_qsz/views/" + str(id)
    cl_response = requests.get(url)
    if cl_response.status_code == 200:
        clhtml = cl_response.text
        clsoup = BeautifulSoup(clhtml, 'html.parser')

        clhref = clsoup.find(class_="compuzone-editor-wrap-wrap")
        print(clhref)

        if(clhref):
            title = clsoup.find(class_="title pr-0").text.strip()
            print(title)
            output_file.write(f'<a href="{url}">칼럼 보러가기 : {title}<br></a>{str(clhref)}<br>')
            output_file2.write(f'{str(clhref)}<br>')

    else:
        print("error")


def qsz_parse():
    qc_url = "https://quasarzone.com/bbs/qc_qsz?page="
    for i in range(1,2):
        qc_response = requests.get(qc_url+str(i))

        if qc_response.status_code == 200:
            html = qc_response.text
            soup = BeautifulSoup(html, 'html.parser')

            href = soup.find("div", {'class': 'list-wrap'})
            href = href.find_all("a")

            for i in href:
                link = i.attrs['href']
                id = int((str(link)[18:]).split('?')[0])
                print(id)
                find_compuzonelink(id)
        else:
            print(qc_response.status_code)

qsz_parse()