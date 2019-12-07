from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

CSV_NAME = 'smartevals.csv'
COURSE_LISTS_CSV_NAME = 'fce_course_list.csv'
IMPLICIT_WAIT = 10
LOGIN_URL = "https://cmu.smartevals.com/"
FCE_RESULT_URL = 'https://wwwh.smartevals.com/reporting/StudentsSeeResults.aspx'
ELEMENT_NAME = 'j_username'
ELEMENT_PASSWORD = 'j_password'
COURSE_ID_FIELD_NAME = '_ctl0:cphContent:grd1:DXFREditorcol7'
YEAR_FIELD_NAME = '_ctl0:cphContent:grd1:DXFREditorcol3'
FCE_ROW_CLASS = 'dxgvDataRow_Custom'
START_YEAR = 2015
END_YEAR = 2019
USERNAME = 'myafi'
PASSWORD = '????'

# APPEND rows to smartevals.csv
# need to be careful not to add same course twice
def add_to_csv(rows, course_id):
    with open("fce/fce_" + course_id + ".csv", 'a') as f:
        for cell_texts in rows:
            first_write = True
            for cell in cell_texts:
                if not first_write:
                    f.write(',')
                first_write = False

                # sanitize ','
                if cell.find(",") != -1:
                    f.write('"' + cell + '"')
                else:
                    f.write(cell)
            f.write('\n')


# read from fce_course_list.csv.
# return list of course id needs to be fetch ['95718','95143']
def get_fce_course_lists():
    with open(COURSE_LISTS_CSV_NAME, 'r') as f:
        data = [i.strip() for i in f]
    return data


# return list of course id which already fetched
# def get_fce_course_fetched():
#     ret = set()
#     with open(CSV_NAME, 'r') as f:
#         for line in f:
#             cells = line.strip().split(',')
#             ret.add(cells[4])
#     return list(ret)


# def get_fce_course_need_to_be_fetch():
#     all_list = get_fce_course_lists()
#     read = get_fce_course_fetched()
#     result = set(all_list) - set(read)
#     result = list(result)
#     result.sort()
#     return result


# do a login using web driver
def login(driver):
    driver.get(LOGIN_URL)
    # assert "Python" in driver.title
    elem = driver.find_element_by_name(ELEMENT_NAME)
    elem.send_keys(USERNAME)
    elem = driver.find_element_by_name(ELEMENT_PASSWORD)
    # put elem password here
    elem.send_keys(PASSWORD)
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    driver.implicitly_wait(IMPLICIT_WAIT)


# run web scraping based on course_id
# return [[2019,Fall,Heinz College,...],[2019,Fall,Heinz College,...]]
def webdriver_search_by_course_id(driver, course_id):
    driver.get(FCE_RESULT_URL)
    driver.implicitly_wait(IMPLICIT_WAIT)
    elem = driver.find_element_by_name(COURSE_ID_FIELD_NAME)
    elem.send_keys(course_id)
    time.sleep(5)
    # driver.implicitly_wait(IMPLICIT_WAIT)

    data = []
    print('course_id = ', course_id)
    for year in range(END_YEAR, START_YEAR - 1, -1):
        elem = driver.find_element_by_name(YEAR_FIELD_NAME)
        elem.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, year)
        time.sleep(5)
        # driver.implicitly_wait(IMPLICIT_WAIT)
        table = driver.find_element_by_id('_ctl0_cphContent_grd1_DXMainTable')
        # print(table.text)
        rows = table.find_elements_by_class_name(FCE_ROW_CLASS)
        print('course_id =', course_id, 'year = ', year)
        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            cell_texts = []
            for c in cells:
                cell_texts.append(c.text)
            # the last cell is trash cell
            cell_texts = cell_texts[0:-1]
            data.append(cell_texts)
    return data


# simple password encyrption
def intsToString(xs):
    s = ""
    for x in xs:
        s = s + chr(x)
    return s


def main():
    fce_course_lists = get_fce_course_lists()
    driver = webdriver.Chrome()
    login(driver)

    course_need_to_be_fetch = fce_course_lists
    for course_id in course_need_to_be_fetch:
        data = webdriver_search_by_course_id(driver, course_id)
        add_to_csv(data, course_id)

    input('press any key to continue')
    driver.close()


if __name__ == '__main__':
    main()
