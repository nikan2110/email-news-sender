from constants import IMAGE_PREVIEW_PATH, FONT_FAMILY_MAIN_PAGE, LINE_HEIGHT_MAIN_PAGE, FONT_FAMILY_NEWS_BLOCK, \
    LINE_HEIGHT_NEWS_BLOCK
from db import fetch_main_page, fetch_pending_news


def generate_main_page_for_preview(main_page_content):
    """
    Generates the HTML structure for the main page preview, including header, title, date, and description.

    :param main_page_content: The content of the main page, including title, date, and description.
    :return: A string containing the HTML block for the main page.
    """

    formatted_description = main_page_content.description.replace("\n", "<br>")

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
                <img src="{IMAGE_PREVIEW_PATH}/basic_images/header_main_page.jpg" 
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
                font-size: 20px; font-weight: bold; padding-right: 20px;{FONT_FAMILY_MAIN_PAGE}">
                    {main_page_content.title}
                </td>
            </tr>
        </table>
    </td>
</tr>

                                    <!-- Main content with background and padding -->
        <tr>
            <td style="padding: 20px; 
            font-family: Arial, Helvetica, sans-serif;
            background-color: #fafafa; text-align: right; direction: rtl; color: #333333; 
            font-size: 15px; {LINE_HEIGHT_MAIN_PAGE} {FONT_FAMILY_MAIN_PAGE}">
                {formatted_description}
            </td>
        </tr>

                                                        <!-- Footer  -->
        <tr>
            <td style="padding: 20px; background-color: #ffffff;">
                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                    <tr>
                        <!-- Pomegranate Image on the Left -->
                        <td width="100" style="text-align: left;">
                            <img src="{IMAGE_PREVIEW_PATH}/basic_images/footer_main_page.png" alt="Footer Image" width="100" style="display: block;">
                        </td>
                        <!-- Signature on the Right -->
                        <td style="text-align: right; direction: rtl; font-size: 14px; {FONT_FAMILY_MAIN_PAGE} 
                        color: #7a2e2e;">
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

def generate_news_block_canvas_for_preview(main_page_content):
    """
    Generates the initial HTML structure for the news block preview, including the header.

    :param main_page_content: The content of the main page to provide context for the news blocks.
    :return: A string containing the base HTML for the news blocks.
    """

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
                <img src="{IMAGE_PREVIEW_PATH}/basic_images/header.jpg" alt="Header Image" width="600" style="display: block;">
            </td>
        </tr>

                                                        <!-- Title -->
        <tr>
            <td align="right" dir="rtl" style="padding: 20px; background-color: #7a2e2e; color: white;">
                <h1 style="margin: 0; font-size: 26px; {FONT_FAMILY_NEWS_BLOCK}">{main_page_content.title}</h1>
            </td>
        </tr>
"""
    return news_html_template

def generate_news_block_content_for_preview(news_item):
    """
    Generates the HTML for an individual news block, including the title, description, image, icon, and footer.

    :param news_item: The news item to be displayed in the email.
    :return: A string containing the HTML for the news block.
    """

    news_block = f"""
                                            <!-- News Block -->
<tr>
    <td style="padding: 10px; padding-bottom: 0px; background-color: #ffffff; direction: rtl; text-align: right;">
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="560" align="center">
            <tr>
            
                                <!-- Right image with icon in the bottom right corner -->
                <td width="220" style="text-align: right; vertical-align: top; ">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="228" style="position: relative;">
                        <tr>
                            <td>
    
                                                        <!-- Main image -->
                                <a href="{news_item.news_link}" target="_blank">
                                <img src="{IMAGE_PREVIEW_PATH}/news_images/{news_item.news_id}.png" 
                                    alt="News Image" width="228" style="display: block; border-radius: 5px;">
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
                
                                                        <!-- Spacer -->
                <td width="20">
                    &nbsp;
                </td>
                
                                    <!-- Left content (Text in Hebrew) with icon -->
                <td width="328" style="direction: rtl; text-align: right; vertical-align: top;">
                    <h2 style="color: #7a2e2e; font-size: 18px; margin: 0;{FONT_FAMILY_NEWS_BLOCK}
                        {LINE_HEIGHT_NEWS_BLOCK}">
                        {news_item.title}
                    </h2>
                    <p style="color: #555555; font-family: Arial, Helvetica, sans-serif;
                        font-size: 16px; direction: rtl; margin: 0;{FONT_FAMILY_NEWS_BLOCK} {LINE_HEIGHT_NEWS_BLOCK}">
                        {news_item.description}
                    </p>
                </td>
                
            </tr>
        </table>
    </td>
</tr>

                                        <!-- Footer with custom styling -->
<tr>
    <td style="padding: 0; text-align: center;">
                                                 <!-- White rounded top part -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="padding: 0; margin: 0;">
                                            <!-- Left side with arrow and text -->
            <tr>                     
                <td style="background-color: #ffffff; text-align: left; width: 30px; padding: 0 10px; padding-right: 0px">
                    <a href="{news_item.news_link}" target="_blank" style="text-decoration: none;">
                        <img src="{IMAGE_PREVIEW_PATH}/basic_images/arrow.png" alt="Arrow Icon" width="24" height="24" 
                        style="vertical-align: middle;">
                    </a>
                </td>
                
                <td style="vertical-align: middle; text-align: left; padding-left: 5px;">
                    <span style="font-size: 14px; {FONT_FAMILY_NEWS_BLOCK}; color: #555555; vertical-align: middle;">מעבר לאפליקציה</span>
                </td>
                
                                                    <!-- Right side with icon -->
                <td style="width: 0px; text-align: right; padding: 0;">
                    <div style="width: 70px; height: 70px; background-color: #ffffff; border-radius: 20px; 
                    display: inline-flex; align-items: flex-start; justify-content: center; padding-right: 10px;">
                        <img src="{IMAGE_PREVIEW_PATH}/basic_images/icon.png" alt="Security Icon" width="60" 
                        height="60" style="display: inline-block;">
                    </div>
                </td>
            </tr>
        </table>

                                                <!-- Orange background below -->
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="padding: 0; margin: 0;">
            <tr>
                <td style="background-color: #ff8c00; height: 10px; border-radius: 0 0 10px 10px;">
                    &nbsp;
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
    """
    Combines the main page content and individual news blocks into a full HTML structure for preview.

    :param news_items: List of news items to be included in the email.
    :param main_page_content: The content of the main page.
    :return: A string containing the full HTML structure for the news blocks preview.
    """

    news_block_html_page = generate_news_block_canvas_for_preview(main_page_content)

    for news_item in news_items:
        news_block = generate_news_block_content_for_preview(news_item)
        news_block_html_page += news_block

    news_block_html_page += """
        </table>
        </body>
        </html>
    """

    return news_block_html_page

def make_html_for_preview():
    """
    Fetches the main page and pending news items from the database, generates HTML for preview purposes.

    :return: A string containing the full HTML for the email preview.
    """

    news_main_page = fetch_main_page()
    pending_news = fetch_pending_news()

    if news_main_page and pending_news:
        main_page_content = news_main_page[0]

        main_page_html = generate_main_page_for_preview(main_page_content)
        news_block_html = generate_news_block_html_for_preview(pending_news, main_page_content)

        full_email_html = f"""{main_page_html}{news_block_html}"""
        return full_email_html