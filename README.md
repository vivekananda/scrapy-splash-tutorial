# Installation


code

    docker pull aciobanu/scrapy
    docker pull scrapinghub/splash

    docker run -v $(pwd):/runtime/app aciobanu/scrapy startproject fara
    docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash
    docker run -p 8050:8050 -p 8051:8051 scrapinghub/splash
    
    docker run -v $(pwd):/runtime/app vivekananda/scrapy-splash crawl faraspider
    docker run -v $(pwd):/runtime/app vivekananda/scrapy-splash crawl faraspider -o temp.csv
    
    

$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt



## Important links

  * https://hub.docker.com/r/aciobanu/scrapy/
  * http://splash.readthedocs.io/en/stable/install.html#os-x-docker
  * http://jamfie.com/2016/06/06/learning-scrapy-tutorial-javascript-sites/
  * https://www.tutorialspoint.com/scrapy/scrapy_first_spider.htm
  * https://doc.scrapy.org/en/latest/topics/selectors.html
  * http://splash.readthedocs.io/en/stable/kernel.html
  
  
  