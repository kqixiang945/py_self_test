#!/opt/homebrew/bin/python3
import pyotp

def getLfOtpCode():
    totp = pyotp.TOTP("DFWRJO7JHM3KGFDESZFHXABLT6QHDCHX")
    return totp.now()

# ***该类的入口main方法
if __name__ == "__main__":
    print(getLfOtpCode())
