def generate_main_page_for_preview(main_page_content):
    main_page_block = f""" 
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
                <img src="http://localhost:8501/app/static/basic_images/header_main_page.jpg" 
                alt="Header Image" width="600" style="display: block;">
            </td>
        </tr>

        <!-- Title and Date Block  -->
<tr>
    <td style="padding: 10px 0; background-color: #7a2e2e;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0">
            <tr>
                <!-- Date -->
                <td style="text-align: left; font-size: 14px; color: white; padding-left: 20px;">
                    {main_page_content.news_date}
                </td>
                <!-- Title -->
                <td style="text-align: right; direction: rtl; color: white; 
                font-size: 20px; font-weight: bold; padding-right: 20px;">
                    {main_page_content.title}
                </td>
            </tr>
        </table>
    </td>
</tr>

        <!-- Main content with background and padding -->
        <tr>
            <td style="padding: 20px; background-color: #fafafa; text-align: right; direction: rtl; color: #333333; 
            font-size: 15px; line-height: 2;">
                {main_page_content.description}
            </td>
        </tr>

        <!-- Footer  -->
        <tr>
            <td style="padding: 20px; background-color: #ffffff;">
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                        <!-- Pomegranate Image on the Left -->
                        <td width="100" style="text-align: left;">
                            <img src="http://localhost:8501/app/static/basic_images/footer_main_page.png" alt="Footer Image" width="100" style="display: block;">
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
    return main_page_block

def generate_news_block_html_page_for_preview(main_page_content):
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
                <img src="http://localhost:8501/app/static/basic_images/header.jpg" alt="Header Image" width="600" style="display: block;">
            </td>
        </tr>

        <!-- Title -->
        <tr>
            <td align="right" dir="rtl" style="padding: 20px; background-color: #7a2e2e; color: white;">
                <h1 style="margin: 0; font-size: 26px;">פרדס רימונים: {main_page_content.title}</h1>
            </td>
        </tr>
"""
    return news_html_template


def generate_news_block_for_preview(news_item):
    news_block = f"""
    <!-- News Block -->
    <tr>
        <td style="padding: 10px; background-color: #fcefe3; direction: rtl; text-align: right;">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="560" align="center">
                <tr>
                    <!-- Right image -->
                    <td width="220" style="text-align: right;">
                    <a href="{news_item.news_link}" target="_blank">
                        <img src="http://localhost:8501/app/static/news_images/{news_item.news_id}.png" alt="News Image" width="228" 
                        style="display: block; border-radius: 5px;">
                    </a>
                    </td>

                    <!-- Spacer -->
                    <td width="20">
                        &nbsp;
                    </td>

                    <!-- Left content (Text in Hebrew) -->
                    <td width="328" style="direction: rtl; text-align: right;">
                        <h2 style="color: #7a2e2e; font-size: 18px; margin: 0;">{news_item.title}</h2>
                        <p style="color: #555555; font-size: 16px; direction: rtl; margin: 0;">
                        {news_item.description}
                        </p>
                    </td>
                </tr>
            </table>
        </td>
    </tr>

    <!-- Small white space between news blocks -->
    <tr>
        <td style="padding: 0.5px 0;">
              &nbsp;
        </td>
    </tr>
    """
    return news_block

def generate_news_block_html_for_preview(news_items, main_page_content):
    news_block_html_page = generate_news_block_html_page_for_preview(main_page_content)

    for news_item in news_items:
        news_block = generate_news_block_for_preview(news_item)
        news_block_html_page += news_block

    news_block_html_page += """
        </table>
        </body>
        </html>
    """

    return news_block_html_page