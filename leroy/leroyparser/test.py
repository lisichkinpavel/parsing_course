url = 'https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_82,h_82,c_pad,b_white,d_photoiscoming.png/LMCode/17556486.jpg'
for r in (("w_82", "w_600"), ("h_82", "h_600")):
    url = url.replace(*r)
print(url)