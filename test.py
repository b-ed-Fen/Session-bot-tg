import progressbar
import time

bar = progressbar.ProgressBar(maxval=10.0, widgets=[
    'Just a progress bar test: ',  # Статический текст
    progressbar.Bar(left='[', marker='=', right=']'),  # Прогресс
    progressbar.SimpleProgress(),  # Надпись "6 из 10"
]).start()

t = 0.0
while t <= 10.0:
    bar.update(t)
    time.sleep(0.01)
    t += 0.1
bar.finish()