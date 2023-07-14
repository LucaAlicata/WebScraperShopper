from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import email.message
from selenium.webdriver.common.keys import Keys
import time, sys
import smtplib

ableToBuyToggle = False     # the bot can purchase the product otherwise it stops one click from buying
mailOn = False              # the bot sends emails to inform: it found a product available, bought a product, the bot crashed
errorSave = 5               # how many times it can restart after a crash
delay = 4                   # delay for the loading of a page
elementDelay = 2            # delay for the loading of page elements
stdPath = './'              # path to the chromedriver
siteInfos = {
    "email": "...", 
    "password": "...", 
    "name": "...", 
    "lastname": "...", 
    "address": "...", 
    "addressNumber": "...", 
    "city": "...", 
    "postalCode": "...", 
    "phone": "..." 
    }
creditCardInfos = {
    "number": "...", 
    "month": "...", 
    "year": "...", 
    "cvv": "...", 
    "name": "..." 
    }
mailInfos = {
    "email": "...", 
    "password": "...", 
    "sendToMailAddress": "..."
    }


def login():
    while login1:
        try:
            user = browser.find_element_by_id("user")
            pw = browser.find_element_by_id("pwd_in")
            user.send_keys(siteInfos["email"])
            pw.send_keys(siteInfos["password"])
            log = browser.find_elements_by_class_name("btn")
            log[2].click()
        except:
            time.sleep(3)
            print("login error")
        else:
            print("login done")
            login1 = False

    title = browser.find_element_by_name('titolo')
    name = browser.find_element_by_name('reg_nome')
    lastname = browser.find_element_by_name('reg_cognome')
    address = browser.find_element_by_name('reg_indirizzo')
    city = browser.find_element_by_name('reg_citta')
    addressNumber = browser.find_element_by_name('reg_civico')
    postalCode = browser.find_element_by_name('reg_cap')
    phone = browser.find_element_by_name('reg_cellulare')
    phone2 = browser.find_element_by_name('reg_telefono')

    title.send_keys(siteInfos["name"])
    name.send_keys(siteInfos["name"])
    lastname.send_keys(siteInfos["lastname"])
    address.send_keys(siteInfos["address"])
    city.send_keys(siteInfos["city"])
    addressNumber.send_keys(siteInfos["addressNumber"])
    postalCode.send_keys(siteInfos["postalCode"])
    phone.send_keys(siteInfos["phone"])
    phone2.send_keys(siteInfos["phone"])


def startup():
    browser.get("https://www.eprice.it/login.aspx?zona=5&dove=0")

    timeout = 3
    while timeout > 0:
        try:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
        except TimeoutException as e:
            restartBot(e)
            browser.get("https://www.eprice.it/login.aspx?zona=5&dove=0")
            timeout -= 1
        else:
            timeout = -1
    if timeout == 0:
        sendEmail(mailType = 2, retStr = "the site does not respond")
        browser.quit()

    privacy = browser.find_element_by_id("onetrust-accept-btn-handler")
    privacy.click()

    user = browser.find_element_by_id("user")
    pw = browser.find_element_by_id("pwd_in")
    user.send_keys(siteInfos["email"])
    pw.send_keys(siteInfos["password"])
    login = browser.find_elements_by_class_name("btn")
    login[0].click()


def setLocation(link):
    timeout = 3
    while timeout > 0:
        try:
            WebDriverWait(browser, delay).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='linkSub js_choiceLoc']")))
        except TimeoutException as e:
            restartBot(e)
            browser.get(link)
            timeout -= 1
        else:
            timeout = -1
    if timeout == 0:
        sendEmail(mailType = 2, retStr = "the site does not respond")
        browser.quit()

    loc = browser.find_elements_by_xpath("//span[@class='linkSub js_choiceLoc']")
    if len(loc) == 0:
        loc = browser.find_elements_by_xpath("//span[@class='btn js_choiceLoc']")
    loc[0].click()
    loctxt = browser.find_element_by_id('città')
    loctxt.send_keys(siteInfos["postalCode"])
    WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "fakelink")))
    fakeLink = browser.find_elements_by_class_name("fakelink")
    fakeLink[0].click()


def restartBot(e):
    global browser
    global errorSave
    try:
        if str(e) == 'Message:':
            browser.quit()
            browser = webdriver.Chrome(PATH)
            browser.minimize_window()
            startup()
        else:
            if str(e).find("window") == -1:
                browser.get_screenshot_as_file(stdPath + 'majorErr.png')
            if mailOn:
                sendEmail(mailType = 2, retStr = str(e))
            browser.quit()
            browser = webdriver.Chrome(PATH)
            browser.minimize_window()
            startup()
            errorSave = errorSave - 1
    except Exception as e2:
        if mailOn:
            sendEmail(mailType = 2, retStr = str(e2))
        print(str(e2))
        sys.exit()


def autoBuy():
    isStuck = 20
    alreadyLogged = True
    clickedBtn1 = True
    while clickedBtn1 and isStuck != 0:
        try:
            cont = browser.find_element_by_id("SpallaButtonNextStep")
            cont.click()
        except TimeoutException:
            return "TOE: Continue 1"
        except:
            time.sleep(elementDelay)
            print("button not found")
        else:
            print("continue btn clicked")
            clickedBtn1 = False
        isStuck = isStuck - 1

    if isStuck == 0:
        return "Continue 1"
    else:
        isStuck = 20

    radio = True
    while radio and isStuck != 0:
        try:
            time.sleep(3)
            Radio = browser.find_elements_by_class_name("js_clickRadio")
            if len(Radio) < 2:
                Radio[0].click()
            else:
                Radio[1].click()
        except TimeoutException:
            return "TOE: Radio button"
        except:
            time.sleep(elementDelay)
            print("radio not found")
        else:
            print("radioButton clicked")
            radio = False
        isStuck = isStuck - 1
    if isStuck == 0:
        return "Radio button"
    else:
        isStuck = 20

    time.sleep(elementDelay)
    clickedBtn2 = True
    while clickedBtn2 and isStuck != 0:
        try:
            continueBtn = browser.find_element_by_id("SpallaButtonNextStep")
            continueBtn.click()
        except TimeoutException:
            return "TOE: Continue 2"
        except:
            print("continue button not found")
            time.sleep(elementDelay)
        else:
            print("continue button done")
            clickedBtn2 = False
        isStuck = isStuck - 1

    if isStuck == 0:
        return "Continue 2"
    else:
        isStuck = 20

    login1 = not alreadyLogged
    if (login1):
        login()

    radio2 = True
    while radio2 and isStuck != 0:
        try:
            radioCards = browser.find_elements_by_class_name("contCarte")
            radioCards[0].click()
        except TimeoutException:
            return "TOE: Radio carte"
        except:
            print("radio cards not found")
            time.sleep(elementDelay)
        else:
            print("radioButton clicked")
            radio2 = False
        isStuck = isStuck - 1
    if isStuck == 0:
        return "Radio cards"
    else:
        isStuck = 20

    insertCarta = True
    while insertCarta and isStuck != 0:
        try:
            number = browser.find_element_by_name('numeroCarta')
            month = browser.find_element_by_name('mese')
            year = browser.find_element_by_name('anno')
            name = browser.find_element_by_name('nome')
            cvv = browser.find_element_by_name('cvv')

            number.send_keys(creditCardInfos["number"])
            month.send_keys(creditCardInfos["month"])
            year.send_keys(creditCardInfos["year"])
            name.send_keys(creditCardInfos["name"])
            cvv.send_keys(creditCardInfos["cvv"])
            if ableToBuyToggle:
                end = browser.find_element_by_id("SpallaButtonNextStep")
                end.click()

        except TimeoutException:
            return "TOE: insert card"
        except:
            print("insert card not found")
            time.sleep(elementDelay)
        else:
            print("insert card clicked")
            insertCarta = False
        isStuck = isStuck - 1

    if isStuck == 0:
        return "insert card details"
    else:
        isStuck = 20

    if ableToBuyToggle:
        amexKey = True

        time.sleep(12)
        while amexKey and isStuck != 0:
            try:
                js = 'continueWithoutPoints()'
                browser.execute_script(js)
            except TimeoutException:
                return "TOE: amex safekey"
            except:
                print("amex safekey not found")
                time.sleep(elementDelay)
            else:
                print("Purchase done")
                amexKey = False
            isStuck = isStuck - 1
        if isStuck == 0:
            return "amex safekey"
        else:
            isStuck = 20

    return "done"


def sendEmail(mailType, link = None, price = None, retStr = None):
    gmail_user = mailInfos["email"]
    gmail_password = mailInfos["password"]
    sent_from = gmail_user
    to = mailInfos["sendToMailAddress"]
    if mailType == 0:
        subject = 'ePrice bot - Prodotto Acquistato !!! '
    elif mailType == 1:
        subject = 'ePrice bot - Ho trovato un prodotto'
    elif mailType == 2:
        subject = 'ePrice bot - Errore bot '
    m = email.message.Message()
    m['From'] = gmail_user
    m['To'] = to
    m['Subject'] = subject
    if mailType == 0:
        m.set_payload('Transazione andata a buon fine')
    elif mailType == 1:
        m.set_payload('Prodotto link: %s\nAl prezzo di: %s' % (link, str(price)))
    elif mailType == 2:
        m.set_payload('error: %s' % retStr)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, m.as_string())
        server.close()

        print('Email sent!')
    except Exception as e:
        print('Something went wrong...')
        print(e)


def AddUrls():
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-13979812?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ZOTAC/d-13979805?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ZOTAC/d-13979807?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-13972310?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-13979815?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-13979812?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-13979810?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-13979814?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-13979817?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-13972311?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-13972313?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-13972312?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3080))

    # Rtx 3070
    productList.append(
        "https://www.eprice.it/schede-video-ZOTAC/d-13979806?metb=widget-prodotti-nvidia-geforce-rtx-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-14039973?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-14039972?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-14039878?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-14042082?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-14039876?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-14039876?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-MSI/d-14039974?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))
    productList.append(
        "https://www.eprice.it/schede-video-ASUS/d-14039875?metb=widget-prodotti-nvidia-geforce-rtx-3070-widget_01")
    productPrice.append(float(Price3070))

    # Rtx 3060Ti
    productList.append("https://www.eprice.it/schede-video-MSI/d-14093957")
    productPrice.append(float(Price3070))


def checkResponseFromSite():
    timeout = 3
    while timeout > 0:
        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'imgPrinc')))
        except TimeoutException as e:
            restartBot(e)
            browser.get(productList[i])
            timeout -= 1
        else:
            timeout = -1
    if timeout == 0:
        sendEmail(mailType = 2, retStr = "the site does not respond")
        browser.quit()


def buyProduct(i):
    global browser, boughtProduct

    browser.get_screenshot_as_file(stdPath + 'found.png')
    if mailOn:
        sendEmail(mailType = 1, link = productList[i], price = price)
    setLocation(productList[i])
    addToCart = browser.find_elements_by_class_name("add-to-basket-warranty")
    addToCart[0].click()
    try:
        no_thx = browser.find_elements_by_class_name("closeOver")
        no_thx[0].click()
    except:
        print("no aggiunte")
    retStr = autoBuy()
    if retStr == "fine":
        browser.get_screenshot_as_file(stdPath + 'purchase.png')
        if mailOn:
            sendEmail(mailType = 0)
        print("Prodotto comprato")
        boughtProduct = True
    else:
        browser.get_screenshot_as_file(stdPath + 'error.png')
        sendEmail(mailType = 2, retStr = retStr)
        browser.quit()
        browser = webdriver.Chrome(PATH)
        browser.minimize_window()
        startup()



PATH = stdPath + 'chromedriver'
browser = webdriver.Chrome(PATH)
boughtProduct = False 
Price3080 = 1100
Price3070 = 700
Price3060 = 700
productList = []
productPrice = []


AddUrls()
startup()
i = 0
while i < len(productList) and errorSave > 0 and not boughtProduct:
    try:
        browser.get(productList[i])
        try:
            WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/h1[1]")))
            denied = browser.find_element_by_xpath("/html/body/h1[1]")
            if denied.text == 'Access Denied':
                browser.quit()
                browser = webdriver.Chrome(PATH)
                browser.minimize_window()
                startup()
                browser.get(productList[i])
                time.sleep(1)
        except:
            pass

        checkResponseFromSite()

        outOfStock = browser.find_elements_by_class_name("disable")
        if len(outOfStock) == 1:
            checkPrice = browser.find_elements_by_class_name("big")
            price = float(checkPrice[0].text.replace('.', '').replace(',', '.'))
            time.sleep(1)
            prime = browser.find_elements_by_class_name("mktPlace")
            if price < productPrice[i] and len(prime) == 0:
                buyProduct(i)
                
        i = (i + 1) % len(productList)

    except Exception as e:
        restartBot(e)

else:
    browser.quit()
