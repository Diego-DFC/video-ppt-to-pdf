#ffmpeg -i v.mkv -vsync 0 -vf select="eq(pict_type\,PICT_TYPE_I)" -f image2 %04d.png
import subprocess, os, img2pdf
from glob import glob
videos = glob('*.mp4') + glob('*.mkv')
print(videos)
for video in videos:
    process=subprocess.run('ffmpeg -vsync 0 -vf select="eq(pict_type\,PICT_TYPE_I)" -f image2 %04d.png -i ' + "\"" + video + "\"", capture_output=False, shell=True)

files = glob('*.png')
#print(files)
similarity=0
removed=[]
total=len(files)
count=0
for file in files:
    try:
        file2=files[files.index(file)+1]
    except:
        break
    #print(files)
    #print(file)
    if os.path.exists(file) and os.path.exists(file2):
        process=subprocess.run(['magick','compare','-metric','SSIM',str(file),str(file2),'diff.png'], capture_output=True, text=True)
        similarity=float(process.stderr)
        #print(similarity)
        count +=1
        print(count, 'of', total, 'files processed')
    if similarity>0.9:
        if os.path.exists(file2):
            removed.append(file2)
            #print('remove ', file2)
#print(removed)
for file in removed:
    os.remove(file)
if os.path.exists('diff.png'):
    os.remove('diff.png')
imgs = glob('*.png')
with open("ppt.pdf","wb") as f:
    f.write(img2pdf.convert(imgs))
for file in imgs:
    os.remove(file)