import re


class RegexChecker:

    @staticmethod
    def is_valid_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_regex, email):
            return False

        return True
