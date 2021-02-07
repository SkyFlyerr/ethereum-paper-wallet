# First install all dependencies:
#   $ pip install -r requirements.txt

# Then launch script, it will generate 2 PDF files: paper wallet itself and cover (220x110 mm):
#   $ python3 walletgen.py

# Don't forget to securely wipe files from your system after printing them:
#   $ wipe *.pdf

# Feel free to support this project (Ethereum, DAI) 0x374F6EFC0A28144914854d9fdb10738be79a6c88

import fpdf
import qrcode
import numpy
from ecdsa import SigningKey, SECP256k1
import sha3
import random

def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=4,
)

# Generating new wallet
keccak = sha3.keccak_256()
priv = SigningKey.generate(curve=SECP256k1)
pub = priv.get_verifying_key().to_string()
keccak.update(pub)
address = keccak.hexdigest()[24:]
privstr = priv.to_string().hex()
addrstr = checksum_encode(address)

# Initializing PDF object
pdf = fpdf.FPDF()
pdf.add_page()
pdf.set_font('Arial', '', 10)

# print address and key to PDF sheet
pdf.set_text_color(0)
pdf.text(15, 15, 'Wallet address:')
pdf.text(48, 15, addrstr)
pdf.text(15, 20, 'Wallet private key:   ')
pdf.set_text_color(150)
pdf.text(48, 20, privstr)
pdf.set_text_color(0)
pdf.text(15, 30, 'You can import this private key into your mobile wallet using this QR code below:')

# Generating QR code with private key and printing it to PDF sheet
pdf.set_fill_color(150)
qr.add_data(privstr)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
A = numpy.asarray(img)
box = 1. # QR code dot size
x = 0
y = 0
pdf.set_line_width(0.1)
for row in A:
    for val in row:
        if val==0: pdf.rect(x*box+85, y*box+40, box+0.05, box+0.05, 'F')
        x+=1
        # print ('{:2}'.format(val), end='')
    y+=1
    x=0

# draw random squares
pdf.set_fill_color(0)
for x in range(2, 208):
    for y in range(101, 196):
        r = random.getrandbits(1)
        if r == 1: pdf.rect(x, y, 1.05, 1.05, 'F')

for x in range(2, 208):
    for y in range(200, 295):
        r = random.getrandbits(1)
        if r == 1: pdf.rect(x, y, 1.05, 1.05, 'F')

# draw folding lines
pdf.set_draw_color(100)
pdf.dashed_line(0, 99, 210, 99)
pdf.dashed_line(0, 198, 210, 198)

# print wallet address and etherscan url with QR codes on another page
pdf.add_page()
# draw folding lines
pdf.set_draw_color(200)
pdf.dashed_line(0, 99, 210, 99)
pdf.dashed_line(0, 198, 210, 198)

pdf.set_text_color(0)
pdf.text(50, 115, 'Wallet address:')
pdf.text(78, 115, addrstr)

pdf.text(38, 135, 'Import for monitoring:')
pdf.set_fill_color(0)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=4,
)
qr.add_data(addrstr)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
A = numpy.asarray(img)
box = 1.15 # QR code dot size
x = 0
y = 0
pdf.set_line_width(0.1)
for row in A:
    for val in row:
        if val==0: pdf.rect(x*box+33, y*box+135, box+0.05, box+0.05, 'F')
        x+=1
        # print ('{:2}'.format(val), end='')
    y+=1
    x=0

pdf.text(133, 135, 'Balance and transactions:')
pdf.set_fill_color(0)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=4,
)
qr.add_data('https://etherscan.io/address/'+addrstr)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
A = numpy.asarray(img)
box = 1. # QR code dot size
x = 0
y = 0
pdf.set_line_width(0.1)
for row in A:
    for val in row:
        if val==0: pdf.rect(x*box+133, y*box+135, box+0.05, box+0.05, 'F')
        x+=1
        # print ('{:2}'.format(val), end='')
    y+=1
    x=0

# closing PDF file
pdfname = addrstr[0:6] + '-' + addrstr[-4:] + '_private.pdf'
pdf.output(pdfname, 'F')

# generating cover print
pdf = fpdf.FPDF('P', 'mm', (220, 110))
pdf.add_page()
pdf.set_font('Arial', '', 10)
pdf.set_text_color(0)
pdf.text(50, 15, 'Wallet address:')
pdf.text(78, 15, addrstr)

pdf.text(38, 35, 'Import for monitoring:')
pdf.set_fill_color(0)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=4,
)
qr.add_data(addrstr)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
A = numpy.asarray(img)
box = 1.15 # QR code dot size
x = 0
y = 0
pdf.set_line_width(0.1)
for row in A:
    for val in row:
        if val==0: pdf.rect(x*box+33, y*box+35, box+0.05, box+0.05, 'F')
        x+=1
        # print ('{:2}'.format(val), end='')
    y+=1
    x=0

pdf.text(133, 35, 'Balance and transactions:')
pdf.set_fill_color(0)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=4,
)
qr.add_data('https://etherscan.io/address/'+addrstr)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
A = numpy.asarray(img)
box = 1. # QR code dot size
x = 0
y = 0
pdf.set_line_width(0.1)
for row in A:
    for val in row:
        if val==0: pdf.rect(x*box+133, y*box+35, box+0.05, box+0.05, 'F')
        x+=1
        # print ('{:2}'.format(val), end='')
    y+=1
    x=0

# closing PDF file
pdfname = addrstr[0:6] + '-' + addrstr[-4:] + '_cover.pdf'
pdf.output(pdfname, 'F')
