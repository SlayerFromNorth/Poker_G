import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image
import pyscreenshot as ImageGrab
from fastbook import *
import re
import pyautogui
import ctypes

from Poker import ai_poker_v01 as aa


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
learn_inf = load_learner(r'C:\Users\Marius\Desktop\ARBEID\Jupyter bok arbeid\export.pkl')

BB = 100
AGV = [10, 0, 0, 0]  # hands, checks, calls, raises -- Totalt
BS = [0, 0, 0]  # Check, Call, Raise
CB = 0
HB = [85, 115]  # hide bet range

kjør = True
print("Ready set go!")


def get_pot():
    try:
        # Her er pot størrelse
        pot = ImageGrab.grab(bbox=(5243, 113, 5333, 133))  # X1,Y1,X2,Y2
        pot_tall = pytesseract.image_to_string(pot)
        # Cash Game
        #pot_tall = re.findall(r"[-+]?\d*\.\d+|\d+", pot_tall)
        #tallet_pot = int(pot_tall[0]) + int(pot_tall[1])/100
        # Lekepenger
        tallet_pot = re.sub(r"\D", "", pot_tall)
        return int(tallet_pot)
    except:
        return 0
def get_call():
    try:
        # Her har du call/check sum
        raised_amout = ImageGrab.grab(bbox=(5460, 544, 5580, 570))  # X1,Y1,X2,Y2
        raised_amout = pytesseract.image_to_string(raised_amout)
        # Cash Game
        #raised_amout = re.findall(r"[-+]?\d*\.\d+|\d+", raised_amout)
        #tallet_raised = int(raised_amout[0]) + int(raised_amout[1]) / 100
        # Lekepenger
        tallet_raised = re.sub(r"\D", "", raised_amout)
        return int(tallet_raised)
    except:
        return 0

while(kjør):

    time.sleep(1)
    # HER er Det som finner ut om det er min tur.
    my_turn = ImageGrab.grab(bbox=(5530, 420, 5580, 480))  # X1,Y1,X2,Y2
    my_turn = pytesseract.image_to_string(my_turn)
    my_turn = re.findall(r"[-+]?\d*\.\d+|\d+", my_turn)
    allin_move = 0

    # All in
    allin = ImageGrab.grab(bbox=(5600, 524, 5750, 547))  # X1,Y1,X2,Y2
    allin = pytesseract.image_to_string(allin)
    if allin[0:4] == "Syne":
        allin_move, my_turn = 1, 1

    if my_turn:
        my_turn = 0
        res = [random.randrange(1, 1000000, 1) for i in range(7)]

        #spillerInput = int(input('Ditt bet?'))

        hand1 = ImageGrab.grab(bbox=(5220, 320, 5282, 370))  # X1,Y1,X2,Y2
        hand2 = ImageGrab.grab(bbox=(5282, 320, 5344, 370))  # X1,Y1,X2,Y2

        flop1 = ImageGrab.grab(bbox=(5126, 137, 5188, 187))  # X1,Y1,X2,Y2
        flop2 = ImageGrab.grab(bbox=(5188, 137, 5250, 187))  # X1,Y1,X2,Y2
        flop3 = ImageGrab.grab(bbox=(5250, 137, 5315, 187))  # X1,Y1,X2,Y2

        turn = ImageGrab.grab(bbox=(5318, 137, 5380, 187))  # X1,Y1,X2,Y2

        river = ImageGrab.grab(bbox=(5380, 137, 5442, 187))  # X1,Y1,X2,Y2

        """my_chips = ImageGrab.grab(bbox=(5275, 400, 5350, 432))  # X1,Y1,X2,Y2
        pot_amout = ImageGrab.grab(bbox=(5275, 400, 5350, 432))  # X1,Y1,X2,Y2

        chips_tall = pytesseract.image_to_string(my_chips)
        chips_tall = re.findall(r"[-+]?\d*\.\d+|\d+", chips_tall)"""



        hand1.save(r'cards\scrap\\'+str(res[3])+'.jpg')
        hand2.save(r'cards\scrap\\' + str(res[4]) + '.jpg')
        a = learn_inf.predict(r'cards\scrap\\' + str(res[3]) + '.jpg')
        b = learn_inf.predict(r'cards\scrap\\' + str(res[4]) + '.jpg')




        flop1.save(r'cards\scrap\\'+str(res[0])+'.jpg')
        flop2.save(r'cards\scrap\\' + str(res[1]) + '.jpg')
        flop3.save(r'cards\scrap\\' + str(res[2]) + '.jpg')
        c = learn_inf.predict(r'cards\scrap\\'+str(res[0])+'.jpg')
        d = learn_inf.predict(r'cards\scrap\\' + str(res[1]) + '.jpg')
        e = learn_inf.predict(r'cards\scrap\\' + str(res[2]) + '.jpg')



        turn.save(r'cards\scrap\\' + str(res[5]) + '.jpg')
        f = learn_inf.predict(r'cards\scrap\\' + str(res[5]) + '.jpg')



        river.save(r'cards\scrap\\'+str(res[6])+'.jpg')
        g = learn_inf.predict(r'cards\scrap\\' + str(res[6]) + '.jpg')


        ggg = []
        koretene = []
        [koretene.append(int(mm)) if not int(mm) == 52 else ggg.append(mm) for mm in [a[0], b[0], c[0], d[0], e[0], f[0], g[0]]]

        pot_sum = get_pot()
        call_sum = get_call()
        AGV[3] += 1
        if len(koretene) == 2:
            BS = [0, 0, 0]
        if call_sum > BB/2:
            BS[2] += 1
            AGV[2] += 1
        else:
            BS[0] += 1
            AGV[0] += 1
        if allin_move == 1:
            try:
                allin = ImageGrab.grab(bbox=(5600, 524, 5750, 587))  # X1,Y1,X2,Y2
                allin1 = pytesseract.image_to_string(allin)
                call_sum = int(re.sub(r"\D", "", allin1))
            except:
                call_sum = 444


        ai_move = aa.ai_starter(koretene, [pot_sum, call_sum, BB, BS[0], BS[1], BS[2]])


        rng = np.random.default_rng(int(time.time()))
        HB_r = int((rng.random() * 60) + 70) / 100

        if len(koretene) == 2:
            betting_ratio = 1.7 * HB_r
        else:
            betting_ratio = 0.13 + 2 * (ai_move[1][2] - 0.85) * HB_r
            if betting_ratio < 0.23:
                betting_ratio = 0.23 * HB_r
            print("betting ratio", betting_ratio)
        if ai_move[0] == 0 and call_sum == 0:
            BS[0] += 1
            ai_move[0] = 1

        if ai_move[0] == 2 and HB_r > 1.12:
            ai_move[0] = 1
            print("lucky 10 % suprise, HB_r =  ", HB_r)
        if allin_move == 1 and ai_move[0] == 1:
            ai_move[0] = 2
        # fold
        action = 0
        print(ai_move)
        if action == 0:
            if ai_move[0] == 0:
                ctypes.windll.user32.SetCursorPos(7963, 833)
                time.sleep(0.6)
                pyautogui.click()

            # call
            if ai_move[0] == 1:
                ctypes.windll.user32.SetCursorPos(8230, 833)
                pyautogui.click()

            # raise min
            if ai_move[0] == 11:
                ctypes.windll.user32.SetCursorPos(8500, 833)
                pyautogui.click()

            # raise amount
            if ai_move[0] == 2:
                ctypes.windll.user32.SetCursorPos(8230, 733)
                time.sleep(0.3)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.click()
                time.sleep(1)
                BS[1] += 1
                AGV[1] += 1
                bet = str(int(pot_sum * betting_ratio)).replace(".", ",")
                pyautogui.write(bet, interval=0.35) # Random interval??!

                # submit
                time.sleep(0.6)
                ctypes.windll.user32.SetCursorPos(8500, 833)
                time.sleep(0.3)
                pyautogui.click()
