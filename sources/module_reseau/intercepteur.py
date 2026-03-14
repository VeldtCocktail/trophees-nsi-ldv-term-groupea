from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class IntercepteurRequetes(QWebEngineUrlRequestInterceptor):

    def interceptRequest(self, info):
        url = info.requestUrl().toString()

        if "tile.openstreetmap.org" in url:
            info.setHttpHeader(
                b"Referer",
                b"https://www.openstreetmap.org/"
            )

        #return super().interceptRequest(info)