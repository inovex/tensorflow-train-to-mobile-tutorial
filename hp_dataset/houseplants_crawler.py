import os
from icrawler.builtin import GoogleImageCrawler
from icrawler import ImageDownloader
from six.moves.urllib.parse import urlparse
import base64






def ensure_dir(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)



class Base64NameDownloader(ImageDownloader):

    def get_filename(self, task, default_ext):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                    'jpg', 'jpeg'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        # works for python 3
        filename = base64.b64encode(url_path.encode()).decode()
        filename=filename[0:30]
	return '{}.{}'.format(filename, extension)


plants_list=['maranta leuconeura erythroneura','phlebodium pseudoaureum','euphorbia trigona rubra','senecio rowleyanus','crassula ovata','Aloe Vera','Haworthia limifolia','euphorbia triangularis','monstera deliciosa','senecio kleiniiformis','fatsia japonica','calathea orbifolia','calathea lancifolia','ficus elastica','oxalis triangularis','chlorophytum comosum vittatum','pilea peperomioides','ficus lyrata','Persea gratissima','tradescantia zebrina','Tradescantia fluminensis Tricolor','Tradescantia pallida','Sansevieria trifasciata','Dracanea marginata','echeveria elegans','dracaea reflexa']

for plant in plants_list:
    ensure_dir('./images/'+plant)
    google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,downloader_cls=Base64NameDownloader,storage={'root_dir': './images/'+plant})
    google_crawler.crawl(keyword=plant, max_num=100,date_min=None, date_max=None,min_size=(200,200), max_size=None)
