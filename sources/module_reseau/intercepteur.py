from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

class IntercepteurRequetes(QWebEngineUrlRequestInterceptor):

    def __init__(self, parent, debug):
        super().__init__(parent)
        self.debug = debug

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if self.debug: print("Requête :", url)

        if "tile.openstreetmap.org" in url:
            info.setHttpHeader(
                b"Referer",
                b"https://www.openstreetmap.org/"
            )
            info.setHttpHeader(
                b"User-Agent",
                b"CarteForets/1.0 (educational project)"
            )
