# from db import get_gmail_creds


class EmailBody:

    def __init__(self, df=None, index=False, table_data=None, headers=None, msg=None, bold=False, underline=False):

        self.css = {'table': {'border': '1px solid black', 'border-collapse': 'collapse'},
                             'th': {'border': '1px solid black', 'border-collapse': 'collapse', 'padding': '5px',
                                    'font-size': '12px', 'font-family': 'Helvetica', 'text-align': 'left',},
                             'td': {'border': '1px solid black', 'border-collapse': 'collapse', 'padding': '5px',
                                    'font-size': '12px', 'font-family': 'Helvetica',},
                             'pre': {'font-size': '12px', 'font-family': 'Helvetica',},}

        self.input_html = []
        # self.add_table(table_data, headers, omit_headers, msg)
        self.add_df_html(df, index, msg, bold, underline)
        self.add_table(table_data, headers=headers)

    def add_msg(self, msg=None, bold=False, underline=False, append_index=None):
        """Add a message to the email body

        msg: String. Message is added to the email
        append_index: Optional way to insert message at certain index
        """

        # If available, append the message to the list of input html
        if bold:
            _b, b_ = '<b>', '</b>'
        else:
            _b, b_ = '', ''

        if underline:
             _u, u_ = '<u>', '</u>'
        else:
            _u, u_ = '', ''

        pre = _b + _u
        post = b_ + u_

        if msg:
            try:
                html = '<p><pre>{0}{1}{2}</pre></p><br>'.format(pre, msg, post)
            except:
                raise EmailBodyError('Invalid message')
            try:
                if append_index is not None:
                    self.input_html.insert(append_index, html)
                else:
                    self.input_html.append(html)
            except:
                raise EmailBodyError('Invalid index')

    def add_table(self, table_data=None, headers=None, omit_headers=False, msg=None):
        """Add a table and an optional leading message to this emails tables list

        table_data: list of lists/tuples. First row is used as headers if headers is None and omit_headers is False
        headers: list. Defaults to None
        omit_headers: boolean. Defaults to False. If True, does not use the first row of table_data as headers
        msg: String. Optional message that is shown before the table in the final email
        append_index: Optional way to insert message at certain index
        """

        # If available, append the message to the list of input html
        if msg:
            self.add_msg(msg=msg)

        # If available, convert an iterable of iterables into an html table
        if table_data:
            try:
                # If a headers list is provided, use that. If not, check if omit_headers was enabled.
                # If not, use the first row of table_data and omit the first row for the table_body
                if headers:
                    # Converts a list of headers into an html row with th elements
                    header_html = '<tr>{0}</tr>\n'.format(' '.join(["<th>{0}</th>\n".format(header) for header in headers]))
                    table_body = table_data
                elif not omit_headers:
                    header_html = '<tr>{0}</tr>\n'.format(' '.join(["<th>{0}</th>\n".format(header) for header in table_data[0]]))
                    table_body = table_data[1:]
                else:
                    header_html = ''
                    table_body = table_data
            except:
                    raise EmailBodyError('Invalid header input. Header should be an iterable')

            try:
                # Using the table_body iterable from above, convert into a list of <tr> strings and join
                rows = []
                for row in table_body:
                    rows.append('<tr>{0}</tr>\n'.format(' '.join(["<td>{0}</td>\n".format(cell) for cell in row])))
                body_html = ' '.join(rows)
            except:
                raise EmailBodyError('Invalid table data. Should be a iterable of iterables')

            self.input_html.append('<table>{header_html}{body_html}</table> </br>\n'.format_map(locals()))

    def add_bullet_list(self, bullet_data=None, msg=None):
        """Add a bulleted list and an optional leading message to this Email Body

        bullet_data: list of lists (up to 2 values per row) to be broken up as bullets in the email
        msg: String. Optional message that is shown before the table in the final email
        """
        # If available, append the message to the list of input html
        if msg:
            self.add_msg(msg=msg)

        # If available, convert an iterable of iterables into an html bulleted list
        if bullet_data:
            try:
                bullet_rows = ''
                if not any(isinstance(el, list) for el in bullet_data):
                    for row in bullet_data:
                        bullet_rows += '<li>{}'.format(row)
                else:
                    for row in bullet_data:
                        if len(row) == 1:
                            bullet_rows += '<li>{}'.format(row)
                        elif len(row) == 2:
                            bullet_rows += '<li>{} -- {}'.format(*row)
                        elif len(row) == 3:
                            bullet_rows += '<li>{} -- {} -- {}'.format(*row)

                bullet_list = """<style="list-style-type:disc">
                              <div><pre>{}</pre></div>\n<br><br>\n""".format(bullet_rows)
            except:
                raise EmailBodyError('Invalid bullet list data. Should be a iterable of iterables')

            self.input_html.append(bullet_list)

    def add_df_html(self, df=None, index=False, msg=None, bold=False, underline=False):
        """ """
        import pandas as pd
        # If available, append the message to the list of input html
        if msg:
            self.add_msg(msg=msg, bold=bold, underline=underline)

        if isinstance(df, pd.DataFrame):
            if any(df):
                try:
                    df_html = df.to_html(index=index, escape=False)
                    df_html.replace(' border="1" class="dataframe"', '')
                    self.input_html.append(df_html + '<br>')
                except:
                    raise EmailBodyError('INVESTIGATE')

    @property
    def html(self):
        # Convert the css hash into html style code
        style_html = ''
        for item in self.css:
            item_html = " ".join(["{0}: {1}; \n".format(att, self.css[item][att]) for att in self.css[item]])
            style_html += "{0} {{ {1} }} \n".format(item, item_html)

        # Join the list of input html into 1 string of html code
        body_html = ' \n'.join(self.input_html)
        return """ <html>
                            <head>
                                <style>
                                    {style_html}
                                </style>
                            </head>
                            {body_html}
                        </html>
                    """.format_map(locals())


class EmailBodyError(Exception):
    def __init__(self, message):
        super(EmailBodyError, self).__init__(message)


def get_nfl_week_num():
    """
    returns: Use beginning and end dates of 2017 nfl season to map weeks to date ranges.
    Use today's date to determine what week of the season we fall under. Return week (int).
    """
    import pandas as pd
    from datetime import datetime as dt
    week_begin = pd.date_range(start='2017-09-12', end='2017-12-29', freq='7D')
    week_end = pd.date_range(start='2017-09-18', end='2018-01-04', freq='7D')
    week_nums = list(range(2, 18))
    week_lol = [[dt(2017, 8, 1), dt(2017, 9, 11), 1]] + [[week_b, week_e, num] for week_b, week_e, num in
                                                         zip(week_begin, week_end, week_nums)]

    today = dt(dt.today().year, dt.today().month, dt.today().day)
    week_mapping_df = pd.DataFrame(week_lol, columns=['Week_Begin', 'Week_End', 'Week_Num'])
    week = week_mapping_df.loc[(week_mapping_df['Week_Begin'] <= today) &
                               (week_mapping_df['Week_End'] >= today)]['Week_Num'].iloc[0]

    return week


def convert_tz(x, est_to_utc=False):
    """
    :return: Convert utc datetimes to est and remove timezone stamp.
    """
    from dateutil import tz
    if est_to_utc:
        from_zone = tz.gettz('America/New_York')
        to_zone = tz.tzutc()

    else:
        from_zone = tz.tzutc()
        to_zone = tz.gettz('America/New_York')

    try:
        ctz = x.replace(tzinfo=from_zone)
        return ctz.astimezone(to_zone).replace(tzinfo=None)
    except:
        return x


# def send_html_email(email_body, subject, sender, recipient):
#     """ Send an html email using smtp server. Only call this when using email tracebacks.
#     email_body: html input for your message
#     subject: subject line as string
#     sender: sender email address as string
#     recipient: semicolon delimited string of recipients
#     """
#
#     import smtplib
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = recipient
#
#     part = MIMEText(email_body, 'html')
#
#     msg.attach(part)
#
#     server = smtplib.SMTP('smtp.gmail.com:587')
#     server.ehlo()
#     server.starttls()
#     username, pw = get_gmail_creds()
#     server.login(username, pw)
#     server.sendmail(sender, recipient.split(';'), msg.as_string())
#     server.close()
