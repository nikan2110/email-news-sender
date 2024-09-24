def generate_news_block(news_item):
    news_block = f"""
    <!-- News Block -->
    
    <tr>
        <td style="padding: 10px; background-color: #fcefe3; direction: rtl; text-align: right;">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="560" align="center">
                <tr>
                    <!-- Right image -->
                    
                    <td width="220" style="text-align: right;">
                        <img src="cid:news_image_{news_item.news_id}" alt="News Image" width="228" 
                        style="display: block; border-radius: 5px;">
                    </td>
                    
                    <!-- Spacer -->
                    <td width="20">
                        &nbsp;
                    </td>
                    
                    <!-- Left content (Text in Hebrew) -->
                    
                    <td width="328" style="direction: rtl; text-align: right;">
                        <h2 style="color: #7a2e2e; font-size: 18px; margin: 0;">{news_item.news_title}</h2>
                        <p style="color: #555555; font-size: 14px; direction: rtl; margin: 0;">
                        {news_item.news_description}
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

