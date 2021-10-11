import requests
from bs4 import BeautifulSoup

today_file = open("today", "w")
today_string = str("")


def find_compuzonelink(url):
    cl_response = requests.get("https://quasarzone.com" + url)
    if cl_response.status_code == 200:
        clhtml = cl_response.text
        clsoup = BeautifulSoup(clhtml, 'html.parser')

        clhref = clsoup.find("div", {'class': 'view-content'})
        clhref = clhref.find_all("a")

        for i in clhref:
            link = i.attrs['href']
            if str(link).startswith("https://quasarzone.com/compuzoneLink?"):
                title = clsoup.select_one("#content > div.sub-content-wrap > div.view-content-wrap > div.view-content-area > div.view-title-wrap > h1").text
                print(title + " : " + link)
                today_file.write('<a href="'+ link + '">' + title + "</a><br>")
                break

    else:
        print("error")


def qsz_parse():
    lastnum_file = open("lastnum", "r")
    today_file = open("today", "w")
    last_num = int(lastnum_file.read())
    lastnum_file.close()

    qc_url = "https://quasarzone.com/bbs/qc_qsz"
    qc_response = requests.get(qc_url)

    if qc_response.status_code == 200:
        html = qc_response.text
        soup = BeautifulSoup(html, 'html.parser')

        href = soup.find("div", {'class': 'list-wrap'})
        href = href.find_all("a")

        lastnum_changed = False

        for i in href:
            link = i.attrs['href']
            if int(str(link)[18:]) > last_num:
                if not lastnum_changed:
                    lastnum_file = open("lastnum", "w")
                    lastnum_file.write(str(link)[18:])
                    lastnum_changed = True

                print(int(str(link)[18:]))
                find_compuzonelink(str(link))

        today_file.close()
    else:
        print(qc_response.status_code)

qsz_parse()