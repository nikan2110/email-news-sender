import os
from dotenv import load_dotenv

load_dotenv()

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_user = "nikan2110isr@gmail.com"
smtp_password = os.getenv('SMTP_PASSWORD')

news_html_template = f"""
<!DOCTYPE html>
<html lang="he">

<head>
    <meta charset="UTF-8">
    <title>Email Template</title>
</head>

<body style="margin:0; padding:0; background-color:#ffffff; font-family: Arial, sans-serif;">

    <!-- Main container -->

    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" 
    style="background-color: #ffffff; margin: 0 auto;">

        <!-- Header Image -->

        <tr>
            <td style="text-align: center;">
                <img src="cid:header_image" alt="Header Image" width="600" style="display: block;">
            </td>
        </tr>

        <!-- Title -->

        <tr>
            <td align="right" dir="rtl" style="padding: 20px; background-color: #7a2e2e; color: white;">
                <h1 style="margin: 0; font-size: 26px;">פרדס רימונים: רימונים של יולי</h1>
            </td>
        </tr>
"""

main_page_html_template_begin = """
<!DOCTYPE html>
    <html lang="he">
    <head>
        <meta charset="UTF-8">
        <title>Custom Email</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, sans-serif;">

        <!-- Main container -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" align="center" 
        style="background-color: #ffffff; margin: 0 auto; border-collapse: collapse;">
            
            <!-- Header Image -->
            <tr>
                <td style="text-align: center;">
                    <img src="cid:main_page_header_image" alt="Header Image" width="600" style="display: block;">
                </td>
            </tr>
"""

main_page_html_template_end = """
 <!-- Footer (Static Pomegranate Image on the left and Signature on the right) -->
            <tr>
                <td style="padding: 20px; background-color: #ffffff;">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                        <tr>
                            <!-- Pomegranate Image on the Left -->
                            <td width="100" style="text-align: left;">
                                <img src="cid:main_page_footer_image" alt="Footer Image" width="100" 
                                style="display: block;">
                            </td>
                            <!-- Signature on the Right -->
                            <td style="text-align: right; direction: rtl; font-size: 14px; color: #7a2e2e;">
                                <span>רות אליעזר<br>מנהלת מחלקת BI</span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>

        </table>
    </body>
    </html>
"""

main_page_content = """שלום רב,
קצב הזדקנות האוכלוסייה בישראל נמצא במגמת עלייה משמעותית בשנים האחרונות בעקבות מגמות שונות, כאשר המרכזית בהן היא העלייה המבורכת בתוחלת החיים. בשנת 2020, מנו בני ה-65 ומעלה בישראל כ-1.1 מיליון איש ואישה, וההערכות הן כי בשנת 2040 מספרם יכפיל את עצמו.
אצלנו במאוחדת גדלנו מ 115,000 ב 2020 עד כ 133,000 ב 2024 אזרחים בני ה-65 ולמעלה (גידול האוכלוסייה המזדקנת הוא בכל המגזרים).
העלייה בתוחלת החיים בישראל מוגדרת כאחד מהצלחות הגדולות של מערכת הבריאות של מדינת ישראל.
עם זאת, העלייה בתוחלת החיים מלווה לעיתים קרובות בהידרדרות הדרגתית וממושכת בתפקוד ומצב הבריאות והיא מאיימת על איכות החיים בגיל המבוגר .
כחלק מהשאיפה לצמצם את הפער בין תוחלת החיים ואיכות החיים, הולך וגובר העיסוק בקרב מדינות העולם, בניהן ישראל, במניעת הדרדרות בקרב האוכלוסייה המזדקנת.
אחד מהאתגרים – הוא ההתמודדות עם מחלת הדמנציה.
אם שואלים מה זו דמנציה התשובה מתחילה בזה שדמנציה היא מונח גג המשמש לתיאור קבוצה של תסמינים אשר נגרמים כתוצאה מפגיעה בתאי המוח ומשפיעים על תפקודי הזיכרון, על בהירות החשיבה ועל היכולות החברתיות בצורה חמורה מספיק כדי להפריע לתפקוד היומיומי. בניגוד לדעה הרווחת,  דמנציה אינה מהווה חלק בלתי נפרד מהליך ההזדקנות, וחומרתה עשויה להשתנות מאוד מאדם לאדם .
חשוב לציין שגילוי מוקדם וטיפול יכולים להשפיע באופן משמעותי על הפרוגנוזה ואיכות החיים של החולים. הרפואה המודרנית מפתחת שיטות אבחון וטיפול חדשות שמטרתן להאט את ההתקדמות ולשפר את איכות החיים של אנשים הסובלים מדמנציה. למודעות למצב ולתמיכה בחולים ויקיריהם תפקיד מרכזי במאבק בדמנציה, מה שהופך את העולם סביבנו למקום אכפתי ומודע יותר.

פיתוח מרכזי ביולי – היה שילוב רשם חדש של דמנציה באפליקציה הקיימת "אזרחים וותיקים". האינטגרציה הזו מאפשרת בניית אוכלוסיות יעד לתוכניות התערבות שונות לצוותים רפואיים.
בנוסף, בדף מש"א, הוספנו נתונים של מקצעות הבריאות (פיזיותרפיסטים, קליניות תקשורת וריפוי בעיסוק). בתחום הלקוחות הוספנו ניתוח מצב שימוש לשירות "פנייה מקוונת " ודוחות חדשים לשב"ן.
"""
