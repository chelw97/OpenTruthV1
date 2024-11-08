import pickle
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from os.path import exists
import os

from webdriver_manager.chrome import ChromeDriverManager


class twAuto:
    driver = None
    cookies_exists = exists('cookies.pkl')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])

    def __init__(
        self,
        password="",
        username="",
        email="",
        headless=True,
        debugMode=False,
        chromeDriverMode="auto", #manual or auto
        driverPath = "./chrome.exe", #if you use manual, pass the driverPath
        pathType = "testId", #xPath or testId
        createCookies = True
    ):
        self.email = email
        self.username = username
        self.password = password
        self.chromeDriverMode = chromeDriverMode
        self.driverPath = driverPath
        self.pathType = pathType
        self.headless = headless
        self.debugMode = debugMode
        self.createCookies = createCookies
        if headless:
            twAuto.chrome_options.add_argument('--headless')
        if debugMode:
            print("twAuto started.")

    # start selenium driver
    def start(self):
        print("Starting twAuto...")
        try:
            if self.chromeDriverMode == "auto":
                print("Downloading Chrome Driver...")
                #chromedriver_autoinstaller.install() 

                twAuto.driver = webdriver.Chrome(ChromeDriverManager().install(), options=twAuto.chrome_options)
                print("Chrome Driver Downloaded Successfully")
            else:
                print("Using Chrome Driver from the path: "+self.driverPath)
                twAuto.driver = webdriver.Chrome(self.driverPath, options=twAuto.chrome_options)
        except Exception as e:
            if self.debugMode:
                print("twAuto Error: ", e)
    # test function to open twitter on chrome
    def openTw(self):
        twAuto.driver.get("https://x.com/home")

    # login to twitter
    def login(self):
        try:
            twAuto.driver.get("https://x.com/")
            # this cookie importing prevents 'New login notification" in every action
            if twAuto.cookies_exists:
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    twAuto.driver.add_cookie(cookie)
            if twAuto.cookies_exists:
                twAuto.driver.get("https://x.com/")
            else:
                twAuto.driver.get("https://x.com/login")
                try:
                    wait = WebDriverWait(twAuto.driver, 120)
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")))
                except TimeoutException:
                    pass
                mailInput = twAuto.driver.find_element(
                    'xpath', "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
                mailInput.send_keys(self.email)
                twAuto.driver.find_element(
                    'xpath', "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div").click()
                time.sleep(3)
#'xpath', "//input[@autocomplete=username']").click()
                try:
                    userNameInput = twAuto.driver.find_element(
                        'xpath', "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
                except:
                    userNameInput = twAuto.driver.find_element(
                        'xpath', "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")

                userNameInput.send_keys(self.username)

                twAuto.driver.find_element(
                    'xpath', "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div").click()

                try:
                    wait = WebDriverWait(twAuto.driver, 120)
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")))
                except TimeoutException:
                    pass
                passwordInput = twAuto.driver.find_element(
                    'xpath', "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
                passwordInput.send_keys(self.password)
                twAuto.driver.find_element(
                    'xpath', "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div").click()

            try:
                wait = WebDriverWait(twAuto.driver, 120)
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='react-root']/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[1]")))
                print("Succesfully Logged In")
            except Exception as e:
                if self.debugMode:
                    print("twAuto Error: ", e)

            twAuto.driver.get("https://x.com/Twitter/")

            if not twAuto.cookies_exists:
                if self.createCookies:
                    pickle.dump(twAuto.driver.get_cookies(), open("cookies.pkl", "wb"))
                
        except Exception as e:
            if self.debugMode:
                    print("twAuto Error: ", e)
            return False   

    #this functions is for the ones that having trouble in the login process, 
    #you must pass the headless parameter as true to use this function
    #after you login manually, open the console window and enter any key to continue
    #this function will save the cookies to the cookies.pkl file
    #and after that you can use the login function and module without any problem
    def manualCookieCreation(self):
        if not self.headless:
            twAuto.driver.get("https://x.com/login")
            input("Please login to your account. After you login, press any key to save your cookies to current folder.")
            pickle.dump(twAuto.driver.get_cookies(), open("cookies.pkl", "wb"))
        else:
            print("Please pass the headless parameter as False to use this function")
            sleep(3)
            self.close()

    # tweet text
    def tweet(self, imgpath=None, text=""):
        # load tweeting page
        twAuto.driver.get("https://x.com/home")
        urlWithText = "https://x.com/compose/tweet?text="+text
        twAuto.driver.get(urlWithText)
        if self.pathType=="xPath":
            try:
                try:
                    wait = WebDriverWait(twAuto.driver, 120)
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]")))
                except TimeoutException:
                    print('Couldnt tweet.')
                    
                if imgpath != None:
                    element = twAuto.driver.find_element(
                        By.XPATH, "//input[@type='file']")
                    '''//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[1]/div[1]'''
                    twAuto.driver.execute_script(
                        "arguments[0].style.display = 'block';", element)

                    element.send_keys(imgpath)

                twAuto.driver.find_element(By.XPATH,
                                        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]').click()
                try:
                    wait = WebDriverWait(twAuto.driver, 5)
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span")))
                    twAuto.driver.find_element(
                        'xpath', "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span").click()
                    tweetUrl = twAuto.driver.current_url
                    print("Tweeted Successfully")
                    print("Tweet URL:"+tweetUrl)
                    return tweetUrl
                except TimeoutException:
                    try:
                        twAuto.driver.find_element(
                            'xpath', "//*[@id='layers']/div[3]/div/div/div/div/div[1]")
                        print('Couldnt Tweet.')
                        return None
                    except:
                        try:
                            wait = WebDriverWait(twAuto.driver, 5)
                            wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span")))
                            twAuto.driver.find_element(
                                By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span").click()
                            tweetUrl = twAuto.driver.current_url
                            print("Tweeted Successfully")
                            print("Tweet URL:"+tweetUrl)
                        except:
                            print('Couldnt Tweet.')
                            return None
            except Exception as e:
                if self.debugMode:
                    print("twAuto Error: ", e)
                return False

        if self.pathType == "testId":
            try:
                try:
                    wait = WebDriverWait(twAuto.driver, 120)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetButton"]')))
                    
                except TimeoutException:
                    print('Couldnt tweet.' )
                
                if imgpath != None:
                    element = twAuto.driver.find_element(
                        By.XPATH, "//input[@type='file']")

                    twAuto.driver.execute_script(
                        "arguments[0].style.display = 'block';", element)

                    element.send_keys(imgpath)
                
                #find tweet button
                tweetButton = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
                
                #click tweet button
                twAuto.driver.execute_script("arguments[0].click()", tweetButton)

                try:
                    wait = WebDriverWait(twAuto.driver, 5)
                    wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span")))
                    twAuto.driver.find_element(
                        'xpath', "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span").click()
                    tweetUrl = twAuto.driver.current_url
                    print("Tweeted Successfully")
                    print("Tweet URL:"+tweetUrl)
                    return tweetUrl
                except TimeoutException:
                    try:
                        twAuto.driver.find_element(
                            'xpath', "//*[@id='layers']/div[3]/div/div/div/div/div[1]")
                        print('Couldnt Tweet.')
                        return None
                    except:
                        try:
                            wait = WebDriverWait(twAuto.driver, 5)
                            wait.until(EC.presence_of_element_located(
                                (By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span")))
                            twAuto.driver.find_element(
                                By.XPATH, "//*[@id='layers']/div[2]/div/div/div/div/div[2]/a/span").click()
                            tweetUrl = twAuto.driver.current_url
                            print("Tweeted Successfully")
                            print("Tweet URL:"+tweetUrl)
                        except:
                            print('Couldnt Tweet.')
                            return None
            except Exception as e:
                if self.debugMode:
                    print("twAuto Error: ", e)
                return False

        
    # quote tweet. this function uses the "adding the quoted tweets url to end of the text method" but maybe i will add the another version of this function that uses the quote tweet function later
    def quoteTweet(self, url="", imgpath="", text=""):
        
        try:
            twAuto.driver.get("https://x.com/home")
            fixUrl=url+"?s=20"
            twAuto.driver.get(fixUrl)
            container_element = self.findTweet(url=url)
            
            if self.pathType == "testId":
                try:

                    body_element = container_element.find_element(By.XPATH, './/div[@data-testid="retweet"]')
                    twAuto.driver.execute_script("arguments[0].click()", body_element)
                    
                except Exception as e:
                    body_element = container_element.find_element(By.XPATH, './/div[@data-testid="unretweet"]')
                    twAuto.driver.execute_script("arguments[0].click()", body_element)
                    try:
                        quoteButton = twAuto.driver.find_element(
                            By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/a')
                        twAuto.driver.execute_script("arguments[0].click()", quoteButton)
                        input_field = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
                        input_field.send_keys(text+" ")
                        if imgpath != None:
                            element = twAuto.driver.find_element(
                                By.XPATH, "//input[@type='file']")

                            twAuto.driver.execute_script(
                                "arguments[0].style.display = 'block';", element)

                            element.send_keys(imgpath)
                        tweetButton = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
                        twAuto.driver.execute_script("arguments[0].click()", tweetButton)
                        return True
                    except:
                        return False
                try:
                    quoteButton = twAuto.driver.find_element(
                        By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/a')
                    twAuto.driver.execute_script("arguments[0].click()", quoteButton)
                    input_field = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="tweetTextarea_0"]')
                    input_field.send_keys(text+" ")
                    if imgpath != None:
                            element = twAuto.driver.find_element(
                                By.XPATH, "//input[@type='file']")

                            twAuto.driver.execute_script(
                                "arguments[0].style.display = 'block';", element)

                            element.send_keys(imgpath)
                    tweetButton = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
                    twAuto.driver.execute_script("arguments[0].click()", tweetButton)
                    return True
                except:
                    return False
            
            if self.pathType == "xPath":
                modified_text = text + "\n" + url
                result = self.tweet(text=modified_text, imgpath=imgpath)
                if result == None:
                    print('Quote Tweet Failed')
                    return None
                else:
                    print('Quoted Tweet Successfully')
                    print('Quote Tweet URL:'+result)
                    return result
            #old method for qutoing, this method adds url of the tweet at the end of the text for quoting, then tweets the text.
            '''modified_text = text + "\n" + url
            result = self.tweet(text=modified_text)
            if result == None:
                print('Quote Tweet Failed')
                return None
            else:
                print('Quoted Tweet Successfully')
                print('Quote Tweet URL:'+result)
                return result
            '''
        except Exception as e:
            if self.debugMode:
                print("twAuto Error: ", e)
            return False
            
    # retweet and like functions are not working with tweets or replies with no text. I will fix it in the future.
    def retweet(self, url=""):
        try:
            twAuto.driver.get("https://x.com/home")
            fixUrl=url+"?s=20"
            twAuto.driver.get(fixUrl)
            container_element = self.findTweet(url=url)
            if self.pathType=="xPath":
                try:
                    try:
                        body_element = container_element.find_element(
                            By.XPATH, './/div[3]/div[8]/div/div[2]/div')
                    except:
                        body_element = container_element.find_element(
                            By.XPATH, './/div[3]/div[7]/div/div[2]/div')
                    body_element.click()
                    try:
                        retweetButton = twAuto.driver.find_element(
                            By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div')
                        retweetButton.click()
                        return True
                    except:
                        return False
                except:
                    return False
            if self.pathType == "testId":
                try:

                    body_element = container_element.find_element(By.XPATH, './/div[@data-testid="retweet"]')
                    twAuto.driver.execute_script("arguments[0].click()", body_element)
                except Exception as e:
                    print("This account already retweeted this tweet.")
                try:
                    retweetButton = twAuto.driver.find_element(
                        By.XPATH, './/div[@data-testid="retweetConfirm"]')
                    twAuto.driver.execute_script("arguments[0].click()", retweetButton)
                    return True
                except:
                    return False
        except Exception as e:
            if self.debugMode:
                print("twAuto Error: ", e)
            return False
        
    # likes tweet
    def like(self, url=""):
        print("-1")
        try:
            twAuto.driver.get("https://x.com/home")
            fixUrl = url + "?s=20"
            twAuto.driver.get(fixUrl)
            print("-0.5")
            # Wait for the tweet container to load
            container_element = self.findTweet(url=url)
            print("0")
            if container_element:
                # Use WebDriverWait to ensure the like button is loaded
                try:
                    if self.pathType == "xPath":
                        try:
                            print("2")
                            WebDriverWait(twAuto.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-testid="like"]'))
                            )
                            print("3")
                            # Find the like button and click it
                            body_element = container_element.find_element(By.CSS_SELECTOR, 'button[data-testid="like"]')
                            body_element.click()
                            return True
                        except Exception as e:
                            print(f"Error finding like button by XPath: {e}")
                            return False
                    elif self.pathType == "testId":
                        # Wait for the like button to become clickable
                        WebDriverWait(twAuto.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, './/div[@data-testid="like"]'))
                        )
                        body_element = container_element.find_element(By.XPATH, './/div[@data-testid="like"]')
                        twAuto.driver.execute_script("arguments[0].click()", body_element)
                        return True
                except Exception as e:
                    if self.debugMode:
                        print("Error interacting with like button: ", e)
                    return False
            else:
                print("Error: Could not find the tweet container.")
                return False
        except Exception as e:
            if self.debugMode:
                print("twAuto Error: ", e)
            return False

    # reply to a tweet
    def reply(self, url="", imgpath="", text=""):
        try:
            twAuto.driver.get("https://x.com/home")
            tweet_id = self.extract_tweet_id(url)
            urlWithText = "https://x.com/intent/tweet?in_reply_to="+tweet_id+"&text="+text
            twAuto.driver.get(urlWithText)
            if self.pathType == "testId" or self.pathType == "xPath":
                #data-testid="tweetTextarea_0_label"]tweetButton
                try:
                    try:
                        if imgpath != "":
                            element = twAuto.driver.find_element(
                                By.XPATH, "//input[@type='file']")

                            twAuto.driver.execute_script(
                                "arguments[0].style.display = 'block';", element)

                            element.send_keys(imgpath)
                        
                        #check if there is a mask
                        try:
                            maskClose = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="app-bar-close"]')
                            twAuto.driver.execute_script("arguments[0].click()", maskClose)
                        except:
                            pass
                        #find tweet button
                        time.sleep(1)
                        wait = WebDriverWait(twAuto.driver, 120)
                        try:
                            wait = WebDriverWait(twAuto.driver, 320)
                            tweetButton = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="tweetButton"]')))
                            #click tweet button
                            twAuto.driver.execute_script("arguments[0].click()", tweetButton)
                        except Exception as e:
                            wait.until(EC.presence_of_element_located(
                                (By.XPATH, '//div[@data-testid="tweetButton"]')))
                            tweetButton = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
                            print("tweetButton:", tweetButton)
                            #click tweet button
                            twAuto.driver.execute_script("arguments[0].click()", tweetButton)
                        wait = WebDriverWait(twAuto.driver, 120)
                        wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//div[@data-testid="toast"]')))
                        replyURLButton = twAuto.driver.find_element(
                            By.XPATH, '//div[@data-testid="toast"]')
                        replyURLElement = replyURLButton.find_element(By.XPATH, './/div[2]/a[1]').get_attribute("href")
                        return replyURLElement
                    except Exception as e:
                        if self.debugMode : print("twAuto Error: ", e)
                        return False
                except Exception as e:
                    if self.debugMode : print("twAuto Error: ", e)
                    return False
        except Exception as e:
            if self.debugMode : print("twAuto Error: ", e)
            return False
                
    # locates tweet in the page based on the tweets content
    def findTweet(self, url=""):
        try:
            #twAuto.driver.get(url)
            try:
                wait = WebDriverWait(twAuto.driver, 120)
                print(2.1)
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-testid="tweet"]')))
                time.sleep(1)
                print(2.2)
                tmp_element = twAuto.driver.find_element(
                    By.CSS_SELECTOR, '[data-testid="tweet"]')
                print(2.3)
                container_element = tmp_element.find_element(By.XPATH, '..')
                return container_element
            except TimeoutException:
                return None
        except Exception as e:
            if self.debugMode:
                print("twAuto Error: ", e)
            return False
    def scrapeNotifications(self):
        print("Scraping notifications...")
        twAuto.driver.get("https://x.com/notifications")
        try:
            wait = WebDriverWait(twAuto.driver, 120)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div")))
        except TimeoutException:
            print('Couldnt find notifications container')
        notifications = twAuto.driver.find_elements(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/section/div/div/div')
        notificationList = []
        for notification in notifications:
            notificationList.append(notification.text)
        print("Notifications scraped successfully")
        print("Notification list:")
        return notificationList
    # undo retweet action - !!!Unstable!!!
    def unretweet(self, url=""):
        twAuto.driver.get("https://x.com/home")
        fixUrl=url+"?s=20"
        twAuto.driver.get(fixUrl)
        container_element = self.findTweet(url=url)
        #unretweetConfirm
        try:
            wait = WebDriverWait(twAuto.driver, 120)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@data-testid="unretweet"]')))
            
            #find unretweet button
            unretweetButton = container_element.find_element(By.XPATH, './/div[@data-testid="unretweet"]')
                    
            #click unretweet button
            twAuto.driver.execute_script("arguments[0].click()", unretweetButton)
            
             #find unretweet button
            unretweetConfirmButton = twAuto.driver.find_element(By.XPATH, '//div[@data-testid="unretweetConfirm"]')
                    
            #click unretweet button
            twAuto.driver.execute_script("arguments[0].click()", unretweetConfirmButton)
            return True
        except Exception as e:
            if self.debugMode:
                print("twAuto Error: ", e)
            return False
    
    # logs out from twitter and deletes the cookies
    def logout(self):
        twAuto.driver.get("https://x.com/logout")
        try:
            wait = WebDriverWait(twAuto.driver, 120)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]")))
        except TimeoutException:
            print('Couldnt log out.')
        twAuto.driver.find_element(
            'xpath', "/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[1]").click()
        os.remove("cookies.pkl")
        print("Succesfully logged out")
        
    # closes selenium driver
    def close(self):
        twAuto.driver.quit()
    def extract_tweet_id(self, url):
        url = url.replace("https://", "")  # Remove "https://"
        url = url.replace("http://", "")  # Remove "http://"
        print("url:", url)
        url_parts = url.split("/")
        if "x.com" in url_parts:
            url_parts.remove("x.com")
        return url_parts[2] if len(url_parts) >= 3 else None
