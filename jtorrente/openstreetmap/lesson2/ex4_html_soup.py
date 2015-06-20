#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the approprate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
import os
from bs4 import BeautifulSoup
import requests
import json

DATADIR = "../../../data/"
html_page = "page_source.html"


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html)
        all_forms = soup.find_all('form')
        form = None
        for f in all_forms:
            if f['name'] == "form1":
                form = f

        if form == None:
            return data

        all_inputs = form.find_all('input')
        for input_control in all_inputs:
            attrs = input_control.attrs
            if attrs == None or not attrs.has_key('name'):
                continue
            #print input_control['name']
            #print ""
            if input_control['name'] == "__VIEWSTATE":
                data['viewstate'] = input_control['value']
            elif input_control['name'] == "__EVENTVALIDATION":
                data['eventvalidation'] = input_control['value']
        #print form

    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    save_path = os.getcwd()
    os.chdir(DATADIR)

    data = extract_data(html_page)
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")

    os.chdir(save_path)

test()
