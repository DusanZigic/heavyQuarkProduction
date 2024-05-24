#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from os import path, mkdir, remove
from params import params

if __name__ == '__main__':

    if not params["quarks"] or len(params["quarks"]) == 0:
        params["quarks"] = ["charm", "bottom"]
    if not isinstance(params["quarks"], list):
        params["quarks"] = [params["quarks"]]
    
    if not params["sNN"] or len(params["sNN"]) == 0:
        params["sNN"] = ["200GeV", "2760GeV", "5020GeV", "5440GeV"]
    if not isinstance(params["sNN"], list):
        params["sNN"] = [params["sNN"]]

    driver = webdriver.Firefox()
    
    for sNN in params["sNN"]:
        for heavyQuark in params["quarks"]:

            driver.get("http://www.lpthe.jussieu.fr/~cacciari/fonll/fonllform.html")
            driver.implicitly_wait(0.5)

            collider = {"5440GeV": "8", "5020GeV": "16", "2760GeV": "9", "200GeV": "4"}
            collider_dropdown = Select(driver.find_element_by_xpath("/html/body/div/div[2]/form/div[1]/div[1]/div/select"))
            collider_dropdown.select_by_value(collider[sNN])

            heavyQuark_dropdown = Select(driver.find_element_by_xpath("/html/body/div/div[2]/form/div[2]/div[1]/div/select"))
            heavyQuark_dropdown.select_by_visible_text(heavyQuark)

            crossSection_dropdown = Select(driver.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/div[1]/div/select"))
            crossSection_dropdown.select_by_value("4")

            pTmin = 1
            pTmin_input = driver.find_element_by_xpath("/html/body/div/div[2]/form/div[4]/div[1]/div[1]/input")
            pTmin_input.clear()
            pTmin_input.send_keys(str(pTmin))

            pTmax = 100 if sNN == "200GeV" else 200
            pTmax_input = driver.find_element_by_xpath("/html/body/div/div[2]/form/div[4]/div[1]/div[2]/input")
            pTmax_input.clear()
            pTmax_input.send_keys(str(pTmax))

            npoints = pTmax - pTmin + 1
            if sNN == "200GeV": npoints *= 2
            npoints_input = driver.find_element_by_xpath("/html/body/div/div[2]/form/div[4]/div[1]/div[5]/input")
            npoints_input.clear()
            npoints_input.send_keys(str(npoints))

            displayResults_checkbox = driver.find_element_by_xpath("/html/body/div/div[2]/form/center/label[1]/input")
            displayResults_checkbox.click()

            submit_button = driver.find_element_by_xpath("//button[@type='submit']")
            submit_button.click()
            driver.implicitly_wait(0.5)

            results = driver.find_element_by_xpath("/html/body/pre")
            results = results.text.split('\n')

            resDir = path.abspath("ptDists")
            if not path.exists(resDir): mkdir(resDir)
            resDir = path.join(resDir, f"ptDist{sNN}")
            if not path.exists(resDir): mkdir(resDir)
            fOut = open(path.join(resDir, f"ptDist_{sNN}_{heavyQuark.capitalize()}.dat"), 'w')
            for res in results:
                if res[0] == '#': continue
                pT         = float(res.split()[0])
                dsigmadpt2 = float(res.split()[1])*3.141592653589793
                fOut.write(f"{pT:5.1f} {dsigmadpt2:.6e}\n")
            fOut.close()
    
    driver.quit()