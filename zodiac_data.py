# -*- coding: utf-8 -*-
"""
ZODIAC - Astronomical Data & Calculation Engine
Preserves all original mathematical calculation logic while providing
rich astrological data for all 12 Zodiac signs in elegant Arabic.
"""

from datetime import date, datetime, timedelta
import calendar
import arabic_reshaper
from bidi.algorithm import get_display

# ---------------------------------------------------------
# Arabic Text Shaping Engine (Line-aware & Safe)
# ---------------------------------------------------------
_reshaper = arabic_reshaper.ArabicReshaper(
    configuration={
        'delete_harakat': False,
        'support_ligatures': True,
    }
)


def ar(text):
    """
    Reshapes and applies BiDi algorithm to Arabic text line-by-line.
    Safe for empty or non-string inputs.
    """
    if text is None:
        return ""
    text_str = str(text)
    if not text_str:
        return ""

    lines = text_str.split("\n")
    processed_lines = []
    for line in lines:
        if line.strip():
            reshaped = _reshaper.reshape(line)
            bidi_text = get_display(reshaped)
            processed_lines.append(bidi_text)
        else:
            processed_lines.append("")
    return "\n".join(processed_lines)


# ---------------------------------------------------------
# Original SIGNS tuple preserved for backward compatibility
# ---------------------------------------------------------
SIGNS = [
    ((1, 20), (2, 18), "الدلو", "♒", "مستقل ويحب الأفكار الجديدة والتجربة."),
    ((2, 19), (3, 20), "الحوت", "♓", "خيالي وحساس ويميل إلى الإبداع."),
    ((3, 21), (4, 19), "الحمل", "♈", "متحمس ويحب التحديات."),
    ((4, 20), (5, 20), "الثور", "♉", "عملي ويحب الاستقرار."),
    ((5, 21), (6, 20), "الجوزاء", "♊", "فضولي واجتماعي ويحب التعلم."),
    ((6, 21), (7, 22), "السرطان", "♋", "يهتم بالعائلة والأمان."),
    ((7, 23), (8, 22), "الأسد", "♌", "واثق ويحب الإبداع."),
    ((8, 23), (9, 22), "العذراء", "♍", "منظم ويهتم بالتفاصيل."),
    ((9, 23), (10, 22), "الميزان", "♎", "يحب التوازن والانسجام."),
    ((10, 23), (11, 21), "العقرب", "♏", "مثابر ويحب فهم الأمور."),
    ((11, 22), (12, 21), "القوس", "♐", "يحب الاستكشاف والمغامرة."),
    ((12, 22), (12, 31), "الجدي", "♑", "طموح وعملي."),
    ((1, 1), (1, 19), "الجدي", "♑", "طموح وعملي."),
]


# ---------------------------------------------------------
# Comprehensive 12 Zodiac Signs Details (Arabic & Astrological)
# ---------------------------------------------------------
ALL_ZODIAC_SIGNS = [
    {
        "id": "aries",
        "name": "الحمل",
        "name_en": "Aries",
        "symbol": "♈",
        "start": (3, 21),
        "end": (4, 19),
        "date_range": "21 مارس - 19 أبريل",
        "element": "ناري",
        "element_icon": "🔥",
        "element_color": (0.97, 0.44, 0.44, 1.0),
        "planet": "المريخ",
        "quality": "كاردينال (مبادر)",
        "traits": ["الشجاعة", "القيادة", "الحماس", "الجرأة", "الصراحة"],
        "strengths": "مقدام، مبدع، واثق بنفسه، ينبض بالحيوية والنشاط.",
        "challenges": "التسرع أحياناً، قلة الصبر مع الأمور البطيئة.",
        "lucky_numbers": "1 ، 9",
        "lucky_color": "الأحمر الملكي",
        "compatibility": ["الأسد", "القوس", "الجوزاء", "الدلو"],
        "description": "برج ناري شجاع ومقدام، يتمتع بطاقة حيوية متقدة وروح مبادرة لا تهدأ. لا يتردد في خوض التحديات والمغامرات الجديدة. يتميز بالصراحة المطلقة والشغف العالي في كل ما يفعله.",
    },
    {
        "id": "taurus",
        "name": "الثور",
        "name_en": "Taurus",
        "symbol": "♉",
        "start": (4, 20),
        "end": (5, 20),
        "date_range": "20 أبريل - 20 مايو",
        "element": "ترابي",
        "element_icon": "🌿",
        "element_color": (0.20, 0.83, 0.53, 1.0),
        "planet": "الزهرة",
        "quality": "ثابت",
        "traits": ["الصبر", "الإخلاص", "الاستقرار", "العملية", "الذوق الرفيع"],
        "strengths": "وفي إلى أقصى حد، حكيم في قراراته، يمتلك عزيمة حديدية.",
        "challenges": "العناد أحياناً، صعوبة تقبل التغييرات المفاجئة.",
        "lucky_numbers": "2 ، 6",
        "lucky_color": "الأخضر الزمردي",
        "compatibility": ["العذراء", "الجدي", "السرطان", "الحوت"],
        "description": "برج ترابي يتسم بالهدوء والثبات وحب الاستقرار. يعشق الجمال والراحة ويسعى لبناء أسس متينة في حياته وعلاقاته. وفي جداً لمن يحب، ويتمتع بصبر نادر يُمكّنه من بلوغ أهدافه بثقة.",
    },
    {
        "id": "gemini",
        "name": "الجوزاء",
        "name_en": "Gemini",
        "symbol": "♊",
        "start": (5, 21),
        "end": (6, 20),
        "date_range": "21 مايو - 20 يونيو",
        "element": "هوائي",
        "element_icon": "💨",
        "element_color": (0.38, 0.65, 0.98, 1.0),
        "planet": "عطارد",
        "quality": "متغير",
        "traits": ["الذكاء", "سرعة البديهة", "الفضول", "التواصل", "المرونة"],
        "strengths": "بارع في الحديث والإقناع، اجتماعي، سريع التعلم والاستيعاب.",
        "challenges": "تشتت الانتباه أحياناً لكثرة اهتماماته وتغير مزاجه.",
        "lucky_numbers": "5 ، 7",
        "lucky_color": "الأصفر المشرق",
        "compatibility": ["الميزان", "الدلو", "الحمل", "الأسد"],
        "description": "برج هوائي يفيض بالحيوية والفضول المعرفي. يمتلك قدرة استثنائية على التواصل والتعبير والتكيف مع مختلف المواقف والأشخاص. محب للتعلم واستكشاف كل فكرة جديدة ومبتكرة.",
    },
    {
        "id": "cancer",
        "name": "السرطان",
        "name_en": "Cancer",
        "symbol": "♋",
        "start": (6, 21),
        "end": (7, 22),
        "date_range": "21 يونيو - 22 يوليو",
        "element": "مائي",
        "element_icon": "💧",
        "element_color": (0.51, 0.55, 0.97, 1.0),
        "planet": "القمر",
        "quality": "كاردينال (مبادر)",
        "traits": ["الحنان", "الحدس القوي", "الوفاء", "العاطفة", "حماية العائلة"],
        "strengths": "إحساس عميق بالآخرين، مخلص ومحب، يمنح الأمان لمن حوله.",
        "challenges": "الحساسية الزائدة والانطواء أحياناً في قوقعته الدفاعية.",
        "lucky_numbers": "2 ، 7",
        "lucky_color": "الفضي والأبيض اللؤلؤي",
        "compatibility": ["العقرب", "الحوت", "الثور", "العذراء"],
        "description": "برج مائي صاحب قلب فياض بالمحبة والتعاطف. يتمتع بحدس داخلي فائق وقدرة عميقة على فهم مشاعر الآخرين. العائلة والأمان والاستقرار الداخلي هم جوهر حياته وأثمن أولوياته.",
    },
    {
        "id": "leo",
        "name": "الأسد",
        "name_en": "Leo",
        "symbol": "♌",
        "start": (7, 23),
        "end": (8, 22),
        "date_range": "23 يوليو - 22 أغسطس",
        "element": "ناري",
        "element_icon": "🔥",
        "element_color": (0.97, 0.44, 0.44, 1.0),
        "planet": "الشمس",
        "quality": "ثابت",
        "traits": ["الثقة", "الكرم", "الكاريزما", "الإبداع", "النبل"],
        "strengths": "قائد بالفطرة، كريم النفس، يمنح الدفء والأمل لمن حوله.",
        "challenges": "حب لفت الأنظار، وصعوبة تقبل الانتقاد في بعض الأحيان.",
        "lucky_numbers": "1 ، 4",
        "lucky_color": "الذهبي والأرجواني",
        "compatibility": ["الحمل", "القوس", "الجوزاء", "الميزان"],
        "description": "برج ناري ملكي يسطع كالشمس كاريزما وإشراقاً. يتمتع بثقة عالية وكرم لا محدود وروح دافئة تبث الحماس في قلوب الجميع. قائد ملهم يعشق الإنجاز والتألق في مجاله.",
    },
    {
        "id": "virgo",
        "name": "العذراء",
        "name_en": "Virgo",
        "symbol": "♍",
        "start": (8, 23),
        "end": (9, 22),
        "date_range": "23 أغسطس - 22 سبتمبر",
        "element": "ترابي",
        "element_icon": "🌿",
        "element_color": (0.20, 0.83, 0.53, 1.0),
        "planet": "عطارد",
        "quality": "متغير",
        "traits": ["الدقة", "التحليل", "التنظيم", "التفاني", "الذكاء العملي"],
        "strengths": "منظم بدقة بالغة، موثوق جداً، يحل المشكلات المعقدة بهدوء.",
        "challenges": "الميل المفرط للمثالية وكثرة انتقاد الذات والآخرين.",
        "lucky_numbers": "3 ، 5",
        "lucky_color": "الأزرق الداكن والرمادي الأنيق",
        "compatibility": ["الثور", "الجدي", "السرطان", "العقرب"],
        "description": "برج ترابي دقيق ومنظم يمتلك عقلاً تحليلياً فذاً. يعتني بأدق التفاصيل ويسعى دوماً للإتقان والتميز في كل مهمة. وفي ومخلص ويحب تقديم العون والحلول العملية المبتكرة لمن يحتاجه.",
    },
    {
        "id": "libra",
        "name": "الميزان",
        "name_en": "Libra",
        "symbol": "♎",
        "start": (9, 23),
        "end": (10, 22),
        "date_range": "23 سبتمبر - 22 أكتوبر",
        "element": "هوائي",
        "element_icon": "💨",
        "element_color": (0.38, 0.65, 0.98, 1.0),
        "planet": "الزهرة",
        "quality": "كاردينال (مبادر)",
        "traits": ["العدل", "الدبلوماسية", "الانسجام", "اللباقة", "الذوق الرفيع"],
        "strengths": "صانع سلام بارع، متوازن في أحكامه، جذاب ولبق في التعامل.",
        "challenges": "التردد في اتخاذ القرارات الحاسمة خوفاً من إزعاج أحد.",
        "lucky_numbers": "6 ، 9",
        "lucky_color": "الوردي الفاتح والأزرق السماوي",
        "compatibility": ["الجوزاء", "الدلو", "الأسد", "القوس"],
        "description": "برج هوائي عاشق للسلام والتناغم والجمال في كل تفاصيله. يسعى دائماً للإنصاف والعدالة وبناء علاقات متوازنة وراقية. يتمتع بذوق فني رفيع وسحر فطري يجذب القلوب إليه.",
    },
    {
        "id": "scorpio",
        "name": "العقرب",
        "name_en": "Scorpio",
        "symbol": "♏",
        "start": (10, 23),
        "end": (11, 21),
        "date_range": "23 أكتوبر - 21 نوفمبر",
        "element": "مائي",
        "element_icon": "💧",
        "element_color": (0.51, 0.55, 0.97, 1.0),
        "planet": "بلوتو والمريخ",
        "quality": "ثابت",
        "traits": ["الشغف", "العمق", "الحدس الفارق", "الإصرار", "القوة النفسية"],
        "strengths": "عزيمة لا تلين، وفي حتى النهاية، يكتشف الحقائق بحدسه.",
        "challenges": "الغموض الشديد وصعوبة منح الثقة بسهولة للآخرين.",
        "lucky_numbers": "4 ، 8",
        "lucky_color": "الأسود القرمزي والعنابي",
        "compatibility": ["السرطان", "الحوت", "العذراء", "الجدي"],
        "description": "برج مائي ذو شخصية مغناطيسية وعميقة تأسر الألباب. يمتلك حدساً خارقاً وشغفاً صادقاً، ويسعى دائماً لفهم الجوهر الحقيقي للأشياء. يتمتع بقوة إرادة حديدية وقدرة مبهرة على التجدد.",
    },
    {
        "id": "sagittarius",
        "name": "القوس",
        "name_en": "Sagittarius",
        "symbol": "♐",
        "start": (11, 22),
        "end": (12, 21),
        "date_range": "22 نوفمبر - 21 ديسمبر",
        "element": "ناري",
        "element_icon": "🔥",
        "element_color": (0.97, 0.44, 0.44, 1.0),
        "planet": "المشتري",
        "quality": "متغير",
        "traits": ["التفاؤل", "المغامرة", "حب المعرفة", "الصدق", "الحرية"],
        "strengths": "روح مرحة، نظرة فلسفية إيجابية، شجاع في اكتشاف آفاق جديدة.",
        "challenges": "الصراحة الزائدة أحياناً التي قد تُفهم بشكل خاطئ.",
        "lucky_numbers": "3 ، 7",
        "lucky_color": "البنفسجي الملكي والأزرق النيلي",
        "compatibility": ["الحمل", "الأسد", "الميزان", "الدلو"],
        "description": "برج ناري محب للحرية والانطلاق والاستكشاف. يمتلك روحاً متفائلة تنشر البهجة والأمل أينما حل، ونظرة فلسفية واسعة للحياة. يعشق السفر والتجارب الملهمة والحوارات العميقة.",
    },
    {
        "id": "capricorn",
        "name": "الجدي",
        "name_en": "Capricorn",
        "symbol": "♑",
        "start": (12, 22),
        "end": (1, 19),
        "date_range": "22 ديسمبر - 19 يناير",
        "element": "ترابي",
        "element_icon": "🌿",
        "element_color": (0.20, 0.83, 0.53, 1.0),
        "planet": "زحل",
        "quality": "كاردينال (مبادر)",
        "traits": ["الطموح", "الانضباط", "الصبر", "المسؤولية", "الحكمة"],
        "strengths": "عزيمة لا تعرف المستحيل، قيادي حكيم، يبني نجاحاته بثبات.",
        "challenges": "الجدية المفرطة في بعض الأحيان وصعوبة الاسترخاء.",
        "lucky_numbers": "4 ، 8",
        "lucky_color": "البني الداكن والرمادي الفحمي",
        "compatibility": ["الثور", "العذراء", "العقرب", "الحوت"],
        "description": "برج ترابي طموح وجاد يبني مستقبله خطوة بخطوة بصبر وعزم لا يلين. يتمتع بانضباط عالٍ وحس مسؤولية استثنائي، ويصل إلى قمم النجاح بفضل عمله الدؤوب وحكمته الواقعية.",
    },
    {
        "id": "aquarius",
        "name": "الدلو",
        "name_en": "Aquarius",
        "symbol": "♒",
        "start": (1, 20),
        "end": (2, 18),
        "date_range": "20 يناير - 18 فبراير",
        "element": "هوائي",
        "element_icon": "💨",
        "element_color": (0.38, 0.65, 0.98, 1.0),
        "planet": "أورانوس وزحل",
        "quality": "ثابت",
        "traits": ["الابتكار", "الاستقلالية", "الإنسانية", "التفرد", "التفكير المستقبلي"],
        "strengths": "مبتكر سابق لعصره، صديق وفي، يدافع عن العدالة والإنسانية.",
        "challenges": "الميل أحياناً للتباعد العاطفي والتفرد المفرط.",
        "lucky_numbers": "4 ، 7",
        "lucky_color": "الفيروزي والأزرق الكهربائي",
        "compatibility": ["الجوزاء", "الميزان", "الحمل", "القوس"],
        "description": "برج هوائي صاحب فكر حر ورؤية مستقبلية متقدمة. يعشق الابتكار والأفكار غير المألوفة ويهتم بالقضايا الإنسانية والتطور. مستقل تماماً ويسير في دربه الخاص بثقة وإبداع.",
    },
    {
        "id": "pisces",
        "name": "الحوت",
        "name_en": "Pisces",
        "symbol": "♓",
        "start": (2, 19),
        "end": (3, 20),
        "date_range": "19 فبراير - 20 مارس",
        "element": "مائي",
        "element_icon": "💧",
        "element_color": (0.51, 0.55, 0.97, 1.0),
        "planet": "نبتون والمشتري",
        "quality": "متغير",
        "traits": ["الخيال", "التعاطف", "الروحانية", "الإلهام", "الرقة"],
        "strengths": "إحساس فني بديع، تعاطف إنساني عميق، روح نقية ملهمة.",
        "challenges": "الهروب إلى عالم الأحلام والهروب من المواجهات الواقعية.",
        "lucky_numbers": "3 ، 7",
        "lucky_color": "البحري والأخضر المائي الفاتح",
        "compatibility": ["السرطان", "العقرب", "الثور", "الجدي"],
        "description": "برج مائي حالم وروحاني يفيض رقة وتعاطفاً وإحساساً مرهفاً. يتمتع بخيال خصب وموهبة فنية استثنائية، ويسعد بتقديم العطاء لمن حوله. صاحب روح نقية تنشر السلام والطمأنينة.",
    },
]

# Quick lookup by id
SIGNS_BY_ID = {sign["id"]: sign for sign in ALL_ZODIAC_SIGNS}


# ---------------------------------------------------------
# Core Astrological & Age Calculations (Strictly Preserved)
# ---------------------------------------------------------
def get_zodiac(day, month):
    """
    Finds Zodiac sign for a given day and month.
    Preserves exact original interface: returns (name, symbol, description)
    """
    current = (month, day)

    for start, end, name, symbol, description in SIGNS:
        if start <= current <= end:
            return name, symbol, description

    return "غير معروف", "✦", ""


def get_zodiac_full(day, month):
    """
    Returns full enriched dictionary for the Zodiac sign of day and month.
    """
    current = (month, day)

    for sign in ALL_ZODIAC_SIGNS:
        start_m, start_d = sign["start"]
        end_m, end_d = sign["end"]

        # Check normal month interval
        if start_m < end_m:
            if (month == start_m and day >= start_d) or (month == end_m and day <= end_d) or (start_m < month < end_m):
                return sign
        else:
            # Crosses year boundary (Capricorn: Dec 22 - Jan 19)
            if (month == 12 and day >= start_d) or (month == 1 and day <= end_d):
                return sign

    # Default fallback
    return ALL_ZODIAC_SIGNS[0]


def next_month(d, count):
    """
    Calculates date advanced by count months.
    Exact original implementation preserved.
    """
    index = d.month - 1 + count
    year = d.year + index // 12
    month = index % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def calculate_age(birthday, today):
    """
    Calculates exact years, months, and days between birthday and today.
    Exact original implementation preserved.
    """
    years = today.year - birthday.year

    try:
        anniversary = birthday.replace(year=today.year)
    except ValueError:
        anniversary = date(today.year, 2, 28)

    if anniversary > today:
        years -= 1
        try:
            anniversary = birthday.replace(year=today.year - 1)
        except ValueError:
            anniversary = date(today.year - 1, 2, 28)

    current = anniversary
    months = 0

    while next_month(current, 1) <= today:
        current = next_month(current, 1)
        months += 1

    days = (today - current).days

    return years, months, days


def get_arabic_month_name(month_num):
    """Returns Arabic name of Gregorian months."""
    months = [
        "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
        "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
    ]
    if 1 <= month_num <= 12:
        return months[month_num - 1]
    return ""


def format_arabic_date(day, month, year):
    """Returns formatted Arabic date string, e.g. 15 مايو 1998"""
    month_name = get_arabic_month_name(month)
    return f"{day} {month_name} {year}"
