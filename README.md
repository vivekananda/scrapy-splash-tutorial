#WIP

# Installation
  * You need to have [docker][docker-doc] installed to run this
  * [docker installation guide][docker-doc]
  * Once you have docker please pull the images with following commands
  
            docker pull vivekananda/scrapy
            docker pull scrapinghub/splash

            docker run -p 8050:8050 -p 8051:8051 scrapinghub/splash
# To run the scraper
  * Update SLASH_URL = 'http://192.168.43.145:8050' with apapropriate ip where the splash docker image is running
    * Remember not to give localhost as localhost in a docker contest is different for different docker images
    * Please give the ip of the machine on which splash docker image is running
    * You can check that by opening SLASH_URL in the browser 
  
            docker run -v $(pwd):/runtime/app vivekananda/scrapy-splash crawl faraspider -o fara_items.json
    

## Important links

  * https://hub.docker.com/r/aciobanu/scrapy/
  * http://splash.readthedocs.io/en/stable/install.html#os-x-docker
  * http://jamfie.com/2016/06/06/learning-scrapy-tutorial-javascript-sites/
  * https://www.tutorialspoint.com/scrapy/scrapy_first_spider.htm
  * https://doc.scrapy.org/en/latest/topics/selectors.html
  * http://splash.readthedocs.io/en/stable/kernel.html
  
  
[docker-docs]: https://docs.docker.com/engine/installation/