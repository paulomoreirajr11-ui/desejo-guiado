from PIL import Image
import os, glob
base = os.path.dirname(os.path.abspath(__file__))
folders = ['modelos', 'estoque', 'resultados']
tb = ta = n = 0
errs = []
for fo in folders:
    for p in glob.glob(os.path.join(base, fo, '*.png')):
        try:
            tb += os.path.getsize(p)
            im = Image.open(p).convert('RGB')
            w, h = im.size
            if w > 850:
                im = im.resize((850, round(h * 850 / w)))
            out = p[:-4] + '.jpg'
            im.save(out, 'JPEG', quality=85, optimize=True)
            ta += os.path.getsize(out)
            n += 1
        except Exception as e:
            errs.append(os.path.basename(p) + ': ' + str(e))
print('convertidas', n, '| antes_MB', round(tb / 1e6, 1), '| depois_MB', round(ta / 1e6, 1))
if errs:
    print('ERROS:', errs)
