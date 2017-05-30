from cefpython3 import cefpython as cef
import platform
import sys
import thread
import time
from bitcoinkiosk_config import pages

def main():
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    for page in pages:
        page["browser"] = cef.CreateBrowserSync(url=page["url"],
                          window_title=page["title"])
        size = page["size"]
        pos = page["position"]
        page["browser"].SetBounds(pos[0], pos[1], size[0], size[1])
        page["browser"].SetZoomLevel(page["zoom"]) 

        if page["fullscreen"]:
            page["browser"].ToggleFullscreen()

    thread.start_new_thread(refresher, (pages,))
    cef.MessageLoop()
    cef.Shutdown()


def refresher(pages):
    for page in pages:
        page["timetoreload"] = page["reload"];
       	page["browser"].SetZoomLevel(page["zoom"]) 
    while True:
        time.sleep(1)
        for page in pages:
            if page["reload"] is 0:
                continue
            page["timetoreload"] = page["timetoreload"] - 1;

            if page["timetoreload"] is 0:
                page["browser"].Reload()
        	page["browser"].SetZoomLevel(page["zoom"]) 
                page["timetoreload"] = page["reload"]

if __name__ == '__main__':
    main()

