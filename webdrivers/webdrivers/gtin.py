from selenium import webdriver
import csv
import time


def go_search_amazon():
    with open("items.txt", "rt") as f:
        search_term = [url.strip() for url in f.readlines()]

    url = 'https://csi.amazon.com/diag/GTINValidationDiagnostic?resourcePath=GTINValidationDiagnostic&diag_run_id=dcb2d10b-9153-4b32-b0ae-a20a7cd2d2c5'
    browser = webdriver.Chrome(
        'D:/PycharmProjects/untitled/spido/spido/webdrivers/chromedriver.exe')

    browser.get(url)

    for item in search_term:
        try:
            time.sleep(2)
            browser.find_element_by_xpath("//div[@class='accordion'][1]//a[@class='step-toggle']/span[1]").click()
            time.sleep(2)
            search_box = browser.find_element_by_name('gtin')
            search_box.clear()
            search_box.send_keys(item)
            search_box.submit()
            time.sleep(1)
            value = [item]
            data = browser.find_element_by_xpath(
                "//div[@class='panel-group']/div/div[1]/div[2]/div[2]")

            csvfile = open('MyFile.csv', 'a')
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            value.append(''.join(data.text.replace("\n", "|")))
            writer.writerow(value)
            print("item " + item + " done")
        except Exception as e:
            print(e)

    browser.close()


if __name__ == '__main__':
    go_search_amazon()
