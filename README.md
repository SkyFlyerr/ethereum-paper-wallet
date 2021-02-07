# Ethereum paper wallet generator

If you would like to store a significant amount of Ethereum assets (such as Ethers or ERC-20 tokens) in safe
you might consider to use a so-called paper wallet. You generate a private key on your device (it is recommended to be offline while generating), print it on the paper and then wipe files, so it is no more reachable for hackers or thieves.

This python script helps you to generate paper wallet for Ethereum assets as PDF file, which then can be printed and stored in a safe place.

Assuming that you are using Linux or MacOS distribution.
Download archive, unzip to a local folder.
Open terminal, navigate to this folder.
First install all dependencies:

```$ pip install -r requirements.txt```

Now it is better if you switch off all network interfaces on your device to be sure generated secrets are in safe. Now launch the script, it will generate 2 PDF files: paper wallet itself and cover (220x110 mm):

```$ python3 walletgen.py```

Print these files (don't use your printer wirelessly - connect it with USB cable).
Wipe files from your system after printing them (don't use 'rm' command as it just remove record in file system table, but leaves files itself, so they can be restored):

```$ wipe *.pdf```

In paper wallet file (named as "...private.pdf") you will find private key for generated wallet and its QR code. 
Print this PDF file. For your convenience you can fold this paper wallet (folding dashed lines are printed either)
and put it in standard posting envelope. Random squares are printed there to avoid visibility of the key in the light.
Second page of this PDF can be printed on the second side of the same sheet for convenient recognition of wallet address. It contains 2 QR codes:
wallet address itself (e.g. if you want to top it up) on the left side and link to etherscan's page to check the balance and transactions of this wallet.

The second PDF file (named "...cover.pdf") you can use to print on standard postal envelope 220 x 110 mm, and it duplicates 
wallet address and etherscan link with QR codes which is also useful if you seal the secret inside the envelope.

Feel free to support author if you find this stuff useful: 0x374F6EFC0A28144914854d9fdb10738be79a6c88
