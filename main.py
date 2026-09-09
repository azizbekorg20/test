import os
import random
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

# Railway Variables yoki kompyuterda environment orqali BOT_TOKEN bering.
BOT_TOKEN = "8880088268:AAFaB9HplUgEx8pyPzW8zv0bfBGhrczmjNQ"

# Har bir savol: (savol, [A,B,C,D], to'g'ri_javob_indeksi)
QUESTIONS = [('1499 sonini Rim raqamida yozilishini aniqlang.', ['MCDIX', 'MCDIC', 'MCCCCXXXXIX', 'MCCCCXL'], 0), ('1987 sonini Rim raqamida yozilishini aniqlang.', ['MCMLXXXVII', 'MCMLXXVII', 'MCMXXVII', 'MCMLXXXIV'], 0), ('246 sonini Rim raqamida yozilishini aniqlang.', ['CCXLVI', 'CCXVI', 'CCLVI', 'CCXLIV'], 0), ("Dastur natijasini aniqlang:\na = []\na += 'abc'\nprint(a)", ["['abc']", "['a', 'b', 'c']", 'abc', '[]'], 1), ("Dastur natijasini aniqlang:\na = ['salom']\na += ['dunyo']\nprint(a)", ["['salomdunyo']", "['salom', 'dunyo']", 'salom dunyo', '[]'], 1), ('Dastur natijasini aniqlang:\na = []\na += [5]\nprint(a)', ['[5]', "['5']", '5', '[]'], 0), ('Elektron hukumat nechta yo‘nalishda faoliyat olib boradi?', ['6 ta', '5 ta', '4 ta', '3 ta'], 0), ('Elektron hukumat xizmatlaridan foydalanishda asosiy maqsad nima?', ['Davlat xizmatlarini elektron ko‘rinishda taqdim etish', 'Faqat o‘yin o‘ynash', 'Faqat reklama joylashtirish', 'Faqat video ko‘rish'], 0), ('Elektron hukumat tizimining asosiy afzalliklaridan biri qaysi?', ['Xizmatlarni masofadan olish imkoniyati', 'Kompyuterni o‘chirish', 'Internetni sekinlashtirish', 'Fayllarni o‘chirish'], 0), ('Windows muhitidagi Telegram ilovasida smayliklar panelini chaqirish uchun qaysi tugmalar birikmasi ishlatiladi?', ['Win + .', 'Alt + S', 'Win + >', 'Alt + Tab'], 0), ('Windowsda emoji oynasini ochish uchun qaysi tugmalar birikmasi ishlatiladi?', ['Win + .', 'Ctrl + Alt + Del', 'Alt + F4', 'Ctrl + P'], 0), ('Windowsda smaylik tanlash panelini chaqirishning to‘g‘ri usulini belgilang.', ['Win + .', 'Shift + F5', 'Ctrl + S', 'Alt + Enter'], 0), ('Photoshop dasturida Ctrl+Shift+I tugmalari bosilsa nima sodir bo‘ladi?', ['Inversiya-teskari buyrug‘i beriladi', 'Qatlam hosil bo‘ladi', 'O‘lcham o‘zgaradi', 'Tasvir to‘liq belgilanadi'], 0), ('Photoshopda Ctrl+Shift+I buyrug‘i asosan qaysi amalni bajaradi?', ['Tanlovni inversiya qiladi', 'Faylni saqlaydi', 'Tasvirni yopadi', 'Yangi qatlam yaratadi'], 0), ('Photoshopda tanlangan sohani teskari tanlash uchun qaysi tugmalar birikmasi ishlatiladi?', ['Ctrl+Shift+I', 'Ctrl+S', 'Ctrl+N', 'Ctrl+P'], 0), ('Dastur natijasini aniqlang:\na = 10\nb = 4\nprint(a & b)', ['40', '0', 'True', 'None'], 1), ('Dastur natijasini aniqlang:\na = 12\nb = 10\nprint(a & b)', ['8', '22', '2', '120'], 0), ('Dastur natijasini aniqlang:\na = 7\nb = 3\nprint(a & b)', ['3', '4', '10', '21'], 0), ('Dastur natijasini aniqlang:\na = 5\nprint(a << 2)', ['1', '20', 'True', 'None'], 1), ('Dastur natijasini aniqlang:\na = 3\nprint(a << 3)', ['24', '6', '11', '1'], 0), ('Dastur natijasini aniqlang:\na = 16\nprint(a >> 2)', ['4', '8', '32', '2'], 0), ('.tiff formatining to‘liq nomi qaysi?', ['Transfer Image File Format', 'Transfer Interchange File Format', 'Tagged Image File Format', 'Tag Imagine File Format'], 2), ('TIFF formatining kengaytmasi qaysi?', ['.txt', '.tiff', '.exe', '.mp3'], 1), ('TIFF formatidan odatda qaysi turdagi ma’lumotni saqlashda foydalaniladi?', ['Rastr tasvirlar', 'Audio fayllar', 'Bajariluvchi dasturlar', 'Matnli buyruqlar'], 0), ('To‘g‘ri to‘rtburchakning eni 1A₁₆ ga, bo‘yi 27₈ ga teng. Perimetrini ikkilik sanoq sistemasida toping.', ['1110010', '1010010', '1010100', '1100010'], 0), ('1F₁₆ sonini ikkilik sanoq sistemasida ifodalang.', ['11111', '10111', '11011', '10011'], 0), ('25₈ sonini o‘nlik sanoq sistemasiga o‘tkazing.', ['19', '21', '23', '25'], 0), ("Dastur natijasini toping:\na = '5.6'\nprint(int(a))", ['5', 'TypeError', '6', 'ValueError'], 3), ("Dastur natijasini toping:\na = '12'\nprint(int(a))", ['12', 'TypeError', '1', 'ValueError'], 0), ("Dastur natijasini toping:\na = '7.9'\nprint(float(a))", ['7', '7.9', 'TypeError', '79'], 1), ("Dastur natijasini toping:\na = ['matematika', 'informatika', 'kimyo', 'fizika']\nprint(a[True])", ['matematika', 'True', 'informatika', 'AttributeError'], 2), ("Dastur natijasini toping:\na = ['a', 'b', 'c']\nprint(a[False])", ['a', 'b', 'False', 'IndexError'], 0), ("Dastur natijasini toping:\na = ['x', 'y', 'z']\nprint(a[1])", ['x', 'y', 'z', '1'], 1), ('101,01₂ + 2A,48₁₆ + 33,4₈ ifodasining o‘nlikdagi qiymatini toping.', ['75,09375', '23,09733', '74,11275', '74,46287'], 0), ('1011₂ sonining o‘nlikdagi qiymatini toping.', ['9', '10', '11', '12'], 2), ('2A₁₆ sonining o‘nlikdagi qiymatini toping.', ['40', '42', '44', '46'], 1), ('Dastur natijasini toping:\na = 23\na >>= 2\nprint(a)', ['11', '3', '21', '5'], 1), ('Dastur natijasini toping:\na = 20\na >>= 2\nprint(a)', ['5', '10', '8', '4'], 0), ('Dastur natijasini toping:\na = 9\na <<= 1\nprint(a)', ['18', '10', '4', '81'], 0), ('Dastur natijasini toping:\na = 7\na |= 4\nprint(a)', ['7', '11', '4', '3'], 0), ('Dastur natijasini toping:\na = 8\na |= 3\nprint(a)', ['11', '8', '5', '24'], 0), ('Dastur natijasini toping:\na = 5\na |= 2\nprint(a)', ['7', '3', '5', '10'], 0), ('“Brend marketingdagi muhim tushunchadir...” mazmunidagi berilgan gaplar muallifini toping.', ['Mark Sukkerberg', 'Filip Kotler', 'Chriz Huhez', 'Steve Chen'], 1), ('Marketing va brending bo‘yicha mashhur mutaxassislardan biri kim?', ['Filip Kotler', 'Linus Torvalds', 'Dennis Ritchie', 'Tim Berners-Lee'], 0), ('“Marketing” tushunchasi bilan bog‘liq mashhur olimni belgilang.', ['Filip Kotler', 'James Gosling', 'Guido van Rossum', 'Bjarne Stroustrup'], 0), ('Dastur natijasini toping:\na = 543\nb = -82\nprint(a // b)', ['7', '-7', '6', '-8'], 3), ('Dastur natijasini toping:\nprint(17 // 5)', ['3', '3.4', '4', '2'], 0), ('Dastur natijasini toping:\nprint(-17 // 5)', ['-3', '-4', '3', '4'], 1), ('MS Excelda shartni qanoatlantiruvchi kataklar sonini sanaydigan funksiya qaysi?', ['ИСТИНА', 'ЕСЛИ', 'СЧЁТЕСЛИ', 'НОК'], 2), ('Excelda berilgan shartga mos kataklar sonini hisoblash uchun qaysi funksiya ishlatiladi?', ['СЧЁТЕСЛИ', 'СУММ', 'СРЗНАЧ', 'МАКС'], 0), ('Excelda kataklardagi sonlarni yig‘ish uchun qaysi funksiya ishlatiladi?', ['СЧЁТЕСЛИ', 'СУММ', 'ЕСЛИ', 'НОК'], 1), ('Scratch dasturining eng kichik fragmenti nima deb nomlanadi?', ['Sprayt', 'Sahna', 'Blok', 'Skript'], 2), ('Scratchda buyruqlar qaysi ko‘rinishda tuziladi?', ['Bloklar', 'Jadvallar', 'Formulalar', 'Slaydlar'], 0), ('Scratchdagi obyekt qaysi nom bilan ataladi?', ['Sprayt', 'Katak', 'Formula', 'Fayl'], 0), ('8 bit bilan necha xil rangni kodlash mumkin?', ['3 xil', '256 xil', '8 xil', '128 xil'], 1), ('4 bit yordamida nechta turli qiymatni kodlash mumkin?', ['4', '8', '16', '32'], 2), ('6 bit yordamida nechta turli qiymatni kodlash mumkin?', ['32', '64', '128', '256'], 1), ('Pythonda fayldan matnni qatorma-qator o‘qish uchun qaysi funksiya ishlatiladi?', ['write', 'writeline', 'read', 'readline'], 3), ('Pythonda faylga matn yozish uchun qaysi metod ishlatiladi?', ['write', 'readline', 'read', 'split'], 0), ('Pythonda faylning barcha mazmunini o‘qish uchun qaysi metoddan foydalanish mumkin?', ['write', 'read', 'writeline', 'append'], 1), ('Dastur natijasini toping:\na = (5, 4, 3, 2, 1)\na[1] = 6\nprint(a)', ['(6, 4, 3, 2, 1)', 'TypeError', '(5, 6, 3, 2, 1)', 'AttributeError'], 1), ('Dastur natijasini toping:\na = (1, 2, 3)\na[0] = 9\nprint(a)', ['(9, 2, 3)', 'TypeError', '(1, 9, 3)', 'AttributeError'], 1), ('Dastur natijasini toping:\na = [1, 2, 3]\na[0] = 9\nprint(a)', ['[9, 2, 3]', 'TypeError', '[1, 9, 3]', 'None'], 0), ("Dastur natijasini toping:\na = {'facebook', 'youtube', 'telegram'}\ndel a\nprint('a')", ['a', 'TypeError', '3', 'NameError'], 0), ('Dastur natijasini toping:\na = 10\ndel a\nprint(a)', ['10', 'None', 'NameError', 'TypeError'], 2), ("Dastur natijasini toping:\nx = 5\ndel x\nprint('x')", ['x', '5', 'NameError', 'None'], 0), ('Dastur natijasini aniqlang: print(8**4//6+202//10*(12-8)%12)', ['160', '690', '4520', '785'], 0), ('Dastur natijasini aniqlang: print(2**5 + 18//3)', ['38', '32', '40', '24'], 0), ('Dastur natijasini aniqlang: print(10%3 + 4*2)', ['9', '8', '3', '11'], 0), ("Dastur natijasini aniqlang:\na = '{0}{0}'.format(7, 17)\nprint(int(a))", ['717', '77', '1717', '17'], 1), ("Dastur natijasini aniqlang:\na = '{1}{0}'.format(7, 17)\nprint(a)", ['717', '177', '77', '17'], 1), ("Dastur natijasini aniqlang:\na = '{}{}'.format(3, 8)\nprint(a)", ['38', '11', '24', '83'], 0), ('IP: 177.68.32.5, maska: 255.255.224.0. Tarmoq manzilini aniqlang.', ['177.68.32.255', '255.255.254.5', '177.68.32.0', '255.255.255.0'], 2), ('IP: 192.168.1.25, maska: 255.255.255.0. Tarmoq manzilini aniqlang.', ['192.168.1.0', '192.168.1.25', '255.255.255.0', '192.168.0.0'], 0), ('IP: 10.0.5.20, maska: 255.255.0.0. Tarmoq manzilini aniqlang.', ['10.0.0.0', '10.0.5.0', '10.0.5.20', '255.255.0.0'], 0), ('Dastur natijasini aniqlang:\ndef f(n):\n    if n <= 2:\n        return 1\n    return 2*f(n-1)+f(n-2)\nprint(f(6))', ['64', '20', '46', '41'], 2), ('Dastur natijasini aniqlang:\ndef f(n):\n    if n <= 1:\n        return 1\n    return f(n-1)+f(n-2)\nprint(f(5))', ['5', '8', '13', '3'], 1), ('Dastur natijasini aniqlang:\ndef f(n):\n    if n == 0:\n        return 0\n    return n + f(n-1)\nprint(f(4))', ['4', '6', '10', '12'], 2), ('7 ning 27-darajasi sakkizlik sanoq sistemasida qanday raqam bilan tugaydi?', ['1', '7', '3', '9'], 2), ('3 ning istalgan musbat darajasi 10 ga bo‘lganda qaysi raqamlar bilan tugashi mumkin?', ['Faqat 3', 'Faqat 9', '3 yoki 9', 'Faqat 0'], 2), ('2 ning 10-darajasini sakkizlik sanoq sistemasiga o‘tkazganda oxirgi raqam qaysi?', ['1', '2', '4', '6'], 2), ('Dastur natijasini aniqlang:\na = (5, 6, 7, 5, 7, 4)\nx = 7\nb = list(a)\nfor i in b:\n    if x == i:\n        b.remove(i)\nb1 = tuple(b)\nprint(b1)', ['(5, 6, 5, 4)', '{5, 6, 5, 4}', '[5, 6, 5, 4]', '5, 6, 5, 4'], 0), ('Dastur natijasini toping:\na = [1, 2, 2, 3]\na.remove(2)\nprint(a)', ['[1, 2, 3]', '[1, 3]', '[2, 2, 3]', 'TypeError'], 0), ('Dastur natijasini toping:\na = [4, 5, 4, 6]\na.remove(4)\nprint(a)', ['[5, 4, 6]', '[4, 5, 6]', '[5, 6]', '[4, 4, 6]'], 0), ('64 xil rangli, gorizontaliga 1240 ta va vertikaliga 1024 ta nuqtali rasm axborot hajmini Kbaytlarda toping.', ['19 Kbayt', '930 Kbayt', '840 Kbayt', '7380 Kbayt'], 1), ('256 xil rangli, 800×600 nuqtali rasmning axborot hajmi taxminan qancha?', ['468,75 KB', '937,5 KB', '1200 KB', '2400 KB'], 0), ('16 xil rangli, 640×480 nuqtali rasm uchun qancha bit kerak?', ['614400 bit', '1228800 bit', '307200 bit', '2457600 bit'], 0), ('Tasvir 16 ta rangga ega. O‘lchami 10×15 sm, ekran imkoniyati 1 dyuymga 250 nuqta. Axborot hajmini Kbaytlarda hisoblang.', ['36,6 Kbayt', '228,9 Kbayt', '732 Kbayt', '5859 Kbayt'], 0), ('Tasvir 4 ta rangga ega va 100×100 piksel. Axborot hajmi qancha?', ['2500 bit', '20000 bit', '10000 bit', '40000 bit'], 1), ('Tasvir 256 ta rangga ega va 200×300 piksel. Axborot hajmi qancha?', ['60 000 bit', '480 000 bit', '240 000 bit', '960 000 bit'], 1)]

dp = Dispatcher()

# Foydalanuvchining test holati:
# user_id -> {"questions": [...], "index": 0, "score": 0}
sessions = {}


def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha, testni boshlaymiz", callback_data="test_start")]
    ])


def answer_keyboard(options):
    letters = ["A", "B", "C", "D"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{letters[i]}) {options[i]}", callback_data=f"ans:{i}")]
        for i in range(4)
    ])


def next_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Keyingi savol", callback_data="next_question")]
    ])


def question_text(number, total, question):
    return f"📝 <b>{number}/{total}-savol</b>\n\n{question}"


@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Eski testni tozalaymiz
    sessions.pop(message.from_user.id, None)

    await message.answer(
        "👋 <b>Informatika olimpiada test botiga xush kelibsiz!</b>\n\n"
        "Sizga PDFdagi mavzular asosida tayyorlangan 90 ta test savoli beriladi.\n"
        "Har bir savolga A, B, C yoki D tugmasi orqali javob berasiz.\n\n"
        "🎯 Testni boshlaymizmi?",
        reply_markup=start_keyboard()
    )


@dp.callback_query(F.data == "test_start")
async def test_start(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Savollarni aralashtiramiz, lekin test davomida tartib o'zgarmaydi.
    qlist = list(range(len(QUESTIONS)))
    random.shuffle(qlist)

    sessions[user_id] = {
        "questions": qlist,
        "index": 0,
        "score": 0,
    }

    await callback.answer("Test boshlandi!")
    await send_question(callback.message, user_id)


async def send_question(message: Message, user_id: int):
    session = sessions.get(user_id)
    if not session:
        await message.answer("Test topilmadi. /start ni bosing.")
        return

    idx = session["questions"][session["index"]]
    question, options, correct = QUESTIONS[idx]
    number = session["index"] + 1
    total = len(session["questions"])

    await message.answer(
        question_text(number, total, question),
        reply_markup=answer_keyboard(options),
        parse_mode="HTML"
    )


@dp.callback_query(F.data.startswith("ans:"))
async def answer_question(callback: CallbackQuery):
    user_id = callback.from_user.id
    session = sessions.get(user_id)

    if not session:
        await callback.answer("Avval /start orqali testni boshlang.", show_alert=True)
        return

    # Bir savolga qayta javob berishni bloklaymiz.
    if session.get("answered", False):
        await callback.answer("Bu savolga javob berilgandi.", show_alert=False)
        return

    selected = int(callback.data.split(":")[1])
    qidx = session["questions"][session["index"]]
    question, options, correct = QUESTIONS[qidx]

    session["answered"] = True
    is_correct = selected == correct

    if is_correct:
        session["score"] += 1

    letters = ["A", "B", "C", "D"]

    # Savol ostida o'quvchi tanlagan javobni ko'rsatamiz.
    if is_correct:
        result = f"✅ <b>To‘g‘ri!</b>\n\nSizning javobingiz: <b>{letters[selected]}) {options[selected]}</b>"
    else:
        result = (
            f"❌ <b>Noto‘g‘ri!</b>\n\n"
            f"Sizning javobingiz: <b>{letters[selected]}) {options[selected]}</b>\n"
            f"To‘g‘ri javob: <b>{letters[correct]}) {options[correct]}</b>"
        )

    # Javob berilgan savolning tugmalarini belgilab qo'yamiz.
    buttons = []
    for i, option in enumerate(options):
        if i == selected:
            mark = "🟢" if is_correct else "🔴"
        elif i == correct and not is_correct:
            mark = "✅"
        else:
            mark = "▫️"
        buttons.append([
            InlineKeyboardButton(
                text=f"{mark} {letters[i]}) {option}",
                callback_data="disabled"
            )
        ])

    await callback.message.edit_reply_markup(
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

    # Natijani savol tagidan alohida yozamiz.
    await callback.message.answer(result, parse_mode="HTML")

    # Keyingi savolni alohida xabarda beramiz.
    await asyncio.sleep(0.4)

    if session["index"] + 1 >= len(session["questions"]):
        score = session["score"]
        total = len(session["questions"])
        percent = score / total * 100
        sessions.pop(user_id, None)

        await callback.message.answer(
            f"🏁 <b>Test tugadi!</b>\n\n"
            f"📊 Natija: <b>{score}/{total}</b>\n"
            f"📈 Foiz: <b>{percent:.1f}%</b>\n\n"
            f"🔄 Qayta ishlash uchun /start ni bosing.",
            parse_mode="HTML"
        )
    else:
        # Avtomatik ravishda keyingi savolni yuboramiz.
        session["index"] += 1
        session["answered"] = False
        await send_question(callback.message, user_id)

    await callback.answer()


@dp.callback_query(F.data == "next_question")
async def next_question(callback: CallbackQuery):
    # Bu callback hozir ishlatilmaydi; keyingi savol avtomatik yuboriladi.
    await callback.answer("Keyingi savol avtomatik yuboriladi.")


@dp.callback_query(F.data == "disabled")
async def disabled(callback: CallbackQuery):
    await callback.answer("Bu savolga allaqachon javob bergansiz.")


async def main():
    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
