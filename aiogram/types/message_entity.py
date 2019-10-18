import sys

from . import base
from . import fields
from .user import User
from ..utils import helper, markdown


class MessageEntity(base.TelegramObject):
    """
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.

    https://core.telegram.org/bots/api#messageentity
    """
    type: base.String = fields.Field()
    offset: base.Integer = fields.Field()
    length: base.Integer = fields.Field()
    url: base.String = fields.Field()
    user: User = fields.Field(base=User)

    def get_text(self, text):
        """
        Get value of entity

        :param text: full text
        :return: part of text
        """
        if sys.maxunicode == 0xffff:
            return text[self.offset:self.offset + self.length]

        if not isinstance(text, bytes):
            entity_text = text.encode('utf-16-le')
        else:
            entity_text = text

        entity_text = entity_text[self.offset * 2:(self.offset + self.length) * 2]
        return entity_text.decode('utf-16-le')

    def parse(self, text, as_html=True):
        """
        Get entity value with markup

        :param text: original text
        :param as_html: as html?
        :return: entity text with markup
        """
        if not text:
            return text
        entity_text = self.get_text(text)

        if self.type == MessageEntityType.BOLD:
            method = markdown.hbold if as_html else markdown.bold
            return method(entity_text)
        if self.type == MessageEntityType.ITALIC:
            method = markdown.hitalic if as_html else markdown.italic
            return method(entity_text)
        if self.type == MessageEntityType.PRE:
            method = markdown.hpre if as_html else markdown.pre
            return method(entity_text)
        if self.type == MessageEntityType.CODE:
            method = markdown.hcode if as_html else markdown.code
            return method(entity_text)
        if self.type == MessageEntityType.URL:
            method = markdown.hlink if as_html else markdown.link
            return method(entity_text, entity_text)
        if self.type == MessageEntityType.TEXT_LINK:
            method = markdown.hlink if as_html else markdown.link
            return method(entity_text, self.url)
        if self.type == MessageEntityType.TEXT_MENTION and self.user:
            return self.user.get_mention(entity_text, as_html=as_html)

        return entity_text


class MessageEntityType(helper.Helper):
    """
    List of entity types

    :key: MENTION
    :key: HASHTAG
    :key: CASHTAG
    :key: BOT_COMMAND
    :key: URL
    :key: EMAIL
    :key: PHONE_NUMBER
    :key: BOLD
    :key: ITALIC
    :key: CODE
    :key: PRE
    :key: TEXT_LINK
    :key: TEXT_MENTION
    """
    mode = helper.HelperMode.snake_case

    MENTION = helper.Item()  # mention - @username
    HASHTAG = helper.Item()  # hashtag
    CASHTAG = helper.Item()  # cashtag
    BOT_COMMAND = helper.Item()  # bot_command
    URL = helper.Item()  # url
    EMAIL = helper.Item()  # email
    PHONE_NUMBER = helper.Item()  # phone_number
    BOLD = helper.Item()  # bold -  bold text
    ITALIC = helper.Item()  # italic -  italic text
    CODE = helper.Item()  # code -  monowidth string
    PRE = helper.Item()  # pre -  monowidth block
    TEXT_LINK = helper.Item()  # text_link -  for clickable text URLs
    TEXT_MENTION = helper.Item()  # text_mention -  for users without usernames
