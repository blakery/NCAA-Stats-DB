from selenium import selenium 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os


def set_download_never_ask():
    fp = webdriver.FirefoxProfile()
    
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.dir", os.path.join(os.getcwd(), "stats"))
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

    return fp


def load_by_year(browser, year):
    '''
    Load a window for the given year
    '''    
    archive_site = 'http://web1.ncaa.org/stats/StatsSrv/rankings?doWhat=archive&sportCode=MBB'
    browser.get(archive_site)
    
    year_menu =Select(browser.find_element_by_name('year'))
    year_menu.select_by_value(year)
    
    browser.execute_script("javascript:doSelected();")    
    browser.switch_to_window('RPT_WIN')


def select_division(browser, division):
    ''' '''
    div = Select(browser.find_element_by_name('div'))
    div.select_by_value(str(division))


def select_reporting_week(browser, week):
    '''Selects the reporting week by value. 
    The highest numbered week indicates the final statistics for the year.
    Defaults to final.
    '''
    week_element = browser.find_element_by_name('rptWeeks')

    if week is None:
        last_week = 0
        for option in week_element.find_elements_by_tag_name("option"):
            value = int(option.get_attribute("value"))
            if value > last_week:
                last_week = value
        week = last_week

    Select(week_element).select_by_value(str(week))


def set_to_individual_stats(browser):
    stat_menu = Select(browser.find_element_by_id('LIST0'))
    stat_menu.select_by_value("-103") # "All Statistics"
    

def set_to_team_stats(browser):
    stat_menu = Select(browser.find_element_by_id('LIST2'))
    stat_menu.select_by_value("-101") # "All Statistics"


def download_stats(browser, division=1, reporting_week=None):
    '''does the bulk of the automation for downloading once the browser is on
    the correct year. Selects the correct division, reporting week, and submits
    the form. The desired statistics should already be selected'''
    
    select_division(browser, division)
    select_reporting_week(browser, reporting_week)

    submit = browser.find_elements_by_class_name('button')[3]
    submit.click()



def download_by_year(browser, year):

    load_by_year(browser, str(year))
    
    set_to_individual_stats(browser)
    download_stats(browser)

    set_to_team_stats(browser)
    download_stats(browser)


def download_all():
    browser = webdriver.Firefox(firefox_profile=set_download_never_ask())
    
    for year in range(2002, 2015):
        download_by_year(browser, year)
        for handle in browser.window_handles[1:]:
            browser.switch_to_window(handle)
            browser.close()
        browser.switch_to_window(browser.window_handles[0])

download_all()
