import sys
import traceback

from browser import window, bind, ajax, console, html, document as doc
from javascript import JSON

DEFAULT_PROGRAM = """
async def main():
    pixels.fill('BLACK')
    pixels.setPixelColor(2, 'RED')
    pixels.show()
    await sleep(1)
    
    pixels.setPixelColor(2, 'WHITE')
    pixels.show()
    await sleep(1)

if __name__ == '__main__':
    run(main())
"""

OUTPUT = ''
M = window.M


class cOutput:
    encoding = 'utf-8'

    def __init__(self):
        self.cons = doc["console"]
        self.buf = ''

    def write(self, data):
        self.buf += str(data)

    def flush(self):
        self.cons.value += self.buf
        self.buf = ''

    def __len__(self):
        return len(self.buf)


class SaveCodeFlow:
    def __init__(self, code):
        self.code = code
        self.process_toast = None

        self._spinner = '<div class="preloader-wrapper small active" style="margin-right: 25px"><div class="spinner-layer spinner-green-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div>'

    def start(self):
        req = ajax.ajax()
        req.open("POST", f'/api/teams/{window.TEAM}', True)
        req.set_header('content-type', 'application/json')
        req.bind("complete", self.oncomplete)
        req.send(JSON.stringify({"code": self.code}))
        self.process_toast = M.toast({
            'html': f'{self._spinner} <span>Saving ...</span>',
            'displayLength': 10000,
            'outDuration': 2000
        })

    def oncomplete(self, res):
        if self.process_toast:
            self.process_toast.dismiss()

        if res.status == 200:
            console.log('Saved')
            M.toast({
                'html': '<span>Code saved!</span>',
                'displayLength': 2000
            })
        else:
            console.log(f'Error: {res.status} - {res.text}')


class LoadCodeFlow:
    def __init__(self, show_toast=True):
        self.process_toast = None
        self.show_toast = show_toast

        self._spinner = '<div class="preloader-wrapper small active" style="margin-right: 25px"><div class="spinner-layer spinner-green-only"><div class="circle-clipper left"><div class="circle"></div></div><div class="gap-patch"><div class="circle"></div></div><div class="circle-clipper right"><div class="circle"></div></div></div></div>'

    def start(self):
        ajax.get(f'/api/teams/{window.TEAM}', oncomplete=self.oncomplete)

        if self.show_toast:
            self.process_toast = M.toast({
                'html': f'{self._spinner} <span>Loading ...</span>',
                'displayLength': 10000,
                'outDuration': 2000
            })
        else:
            # search for existing spinner
            toast_elements = doc.select('.loading_spinner')
            if toast_elements:
                self.process_toast = M.Toast.getInstance(toast_elements[0])

    def oncomplete(self, res):
        if self.process_toast:
            self.process_toast.dismiss()

        editor = window.ace.edit("editor")
        try:
            if res.status == 200:
                data = JSON.parse(res.text)

                if 'code' in data:
                    editor.setValue(data['code'])
                    editor.execCommand("gotolineend")
                    return

            editor.setValue(DEFAULT_PROGRAM)

        finally:
            editor.execCommand("gotolineend")
            editor.setReadOnly(False)
            doc['save'].classList.remove('disabled')
            doc['versions'].classList.remove('disabled')


class Pixels:
    def __init__(self, root):
        self._container = root
        self._leds = []

        self._setup()
        self.show()

    def _setup(self):
        attrs = self._container.attrs
        if 'data-leds' in attrs:
            num = int(attrs['data-leds'])
        else:
            num = 10

        for i in range(num):
            self._container <= html.DIV('', Class="led")
            self._leds.append('WHITE')

    def set_pixel(self, num, color):
        # todo validate
        self.set(num, color)

    def set(self, num, color):
        self._leds[num] = color

    def show(self):
        for color, led in zip(self._leds, self._container.children):
            led.style.color = color


def load_versions(*args):
    pass


if __name__ == '__main__':
    # Load program
    editor = window.ace.edit("editor")
    LoadCodeFlow(show_toast=False).start()

    version_modal = M.Modal.init(doc['versions-modal'], {
        'onOpenStart': load_versions
    })

    # setup console
    cOut = cOutput()
    sys.stdout = cOut
    sys.stderr = cOut


    # Bind actions
    @bind(doc['run'], "click")
    def run(*args):
        global OUTPUT
        doc["console"].value = ''
        src = editor.getValue()
        try:
            from browser import aio, document, window
            pixels = document.select('virtual-lightstrip')[0]
            ns = {
                '__name__': '__main__',
                'pixels': pixels,
                'sleep': aio.sleep,
                'run': aio.run,
            }
            exec(src, ns)
            state = 1
        except Exception as exc:
            traceback.print_exc(file=sys.stderr)
            state = 0
        sys.stdout.flush()
        OUTPUT = doc["console"].value

        return state


    @bind(doc, "keydown")
    def catch_ctrl_s(e):
        is_mac = 'Mac' in window.navigator.platform
        if (e.metaKey if is_mac else e.ctrlKey) and e.keyCode == 83:
            e.preventDefault()
            save()


    @bind(doc['save'], "click")
    def save(*args):
        editor = window.ace.edit("editor")
        SaveCodeFlow(editor.getValue()).start()


    @bind(doc['versions'], 'click')
    def open_versions_modal(*args):
        version_modal.open()
