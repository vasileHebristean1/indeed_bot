from argparse import Action
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class indeedBot:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.query_string = "https://ro.indeed.com/jobs?l&q=remote&forceLocation=0&vjk=a416ab6102f2a1c5"
        self.jobs = []
        self.expres_apply_jobs = []

    def nav(self, url):
        self.driver.get(url)
        time.sleep(3)

    def _convert_query(self, job, city, state):
        job = '+'.join(job.split(" "))
        city = city.lower()

        if len(state) != 2:
            raise Exception("State must be 2 characters long")
        state = state.upper()

        return job, city, state

    def query(self, job, city, state):
        job, city, state = self._convert_query(job, city, state)
        query = self.query_string.format(job=job, city=city, state=state)
        self.nav(query)

    def find_express_jobs(self):
        self.jobs = self.driver.find_element_by_class_name(
            'jobsearch-SerpJobCard')
        print(f'Number of jobs found: {len(self.jobs)}')

        for job in self.jobs:
            try:
                job.find_element_by_class_name('jobCardShelfContainer')
                self.expres_apply_jobs.append(job)
            except:
                pass

    def apply_to_express_jobs(self, profile):
        print(f'Number of jobs to apply: {len(self.expres_apply_jobs)}')
        for job in self.expres_apply_jobs:
            self._process_job(job)
            self._process_apply_button()
            self._fill_applicant_form(profile)

    def _process_apply_button(self):
        apply_button = self.driver.find_element_by_id(
            'indeedApplyButtonContainer')
        apply_button.click()
        time.sleep(4)

    def _process_job(self, job):
        job_a_tag = job.find_element_by_tag_name('a')
        job_href = job_a_tag.get_attribute('href')
        job_href = job.href.split('&from'[0])
        self.nav(job_href)

    def _fill_applicant_form(self, profile):
        actions = ActionChains(self.driver)
        actions.send_keys(profile['name'] + Keys.TAB +
                          profile['email'] + Keys.TAB +
                          profile['phone_number'] + Keys.TAB)
        actions.perform()


if __name__ == '__main__':
    profile = {
        'name': 'John Doe',
        'email': 'johndoe@gmail.com',
        'phone_number': '+40 722 123 456',
        'resume': os.getcwd() + '/resume.pdf'
    }

    id_bot = indeedBot()

    id_bot.query('python developer', 'web developer',
                 'cluj-napoca', 'oradea', 'ro')
    id_bot.find_express_jobs()
    id_bot.apply_to_express_jobs(profile)