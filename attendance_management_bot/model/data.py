#!/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2020-present Works Mobile Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
create message content
"""

__all__ = ['make_postback_action', 'make_message_action', 'make_url_action',
           'make_normal_action', 'make_quick_reply_item', 'make_quick_reply',
           'make_text', 'make_add_rich_menu', 'make_button', 
           'make_i18n_content_texts', 'i18n_text', 'make_i18n_label',
           'i18n_display_text', 'make_image_carousel_column',
           'make_i18n_image_url']

import json

def make_i18n_label(language, label):
    return {"language": language, "label": label}


def i18n_display_text(language, display_text):
    return {"language": language, "displayText": display_text}


def make_postback_action(data, label=None, i18n_labels=None,
                         display_text=None, i18n_display_texts=None):
    """
    make post back action.

        reference
        - https://developers.worksmobile.com/jp/document/1005050?lang=en

    :param data: post back string
    :return: actions content
    """

    action = {"type": "postback", "data": data}

    if display_text is not None:
        action["displayText"] = display_text
    if label is not None:
        action["label"] = label
    if i18n_labels is not None:
        action["i18nLabels"] = i18n_labels
    if i18n_display_texts is not None:
        action["i18nDisplayTexts"] = i18n_display_texts

    return action


def i18n_text(language, text):
    return {"language": language, "text": text}


def make_message_action(post_back, label, i18n_labels=None,
                        text=None, i18n_texts=None):
    """
    make message action.

        reference
        - https://developers.worksmobile.com/jp/document/1005050?lang=en

    :param post_back: post back string
    :return: actions content
    """

    action = {"type": "message", "label": label, "postback": post_back}
    if text is not None:
        action["text"] = text
    if i18n_labels is not None:
        action["i18nLabels"] = i18n_labels
    if i18n_texts is not None:
        action["i18nTexts"] = i18n_texts

    return action


def make_url_action(label, url, i18n_labels=None):
    """
    make url action.

        reference
        - https://developers.worksmobile.com/jp/document/1005050?lang=en

    :param url: User behavior will trigger the client to request this URL.
    :return: actions content
    """

    if i18n_labels is not None:
        return {"type": "uri", "label": label, "url": url,
                "i18nLabels": i18n_labels}
    return {"type": "uri", "label": label, "url": url}


def make_normal_action(atype, label, i18n_labels=None):
    """
    Create camera, camera roll, location action.

        reference
        - https://developers.worksmobile.com/jp/document/1005050?lang=en

    :param atype: action's type
    :return: None
    """
    if i18n_labels is not None:
        return {"type": atype, "label": label, "i18nLabels": i18n_labels}
    return {"type": atype, "label": label}


def make_i18n_thumbnail_image_url(language, thumbnail_image_url):
    return {"language": language, "thumbnailImageUrl": thumbnail_image_url}


def make_i18n_image_resource_id(language, image_resource_id):
    return {"language": language, "imageResourceId": image_resource_id}


def make_quick_reply_item(action,
                          url=None,
                          image_resource_id=None,
                          i18n_thumbnail_image_urls=None,
                          i18n_image_resource_ids=None):
    """
    Create quick reply message item.

        reference
        - https://developers.worksmobile.com/jp/document/100500807?lang=en

    :param action: The user clicks the quick reply button to trigger this action.
    :return: quick reply content.
    """

    reply_item = {"action": action}
    if url is not None:
        reply_item["imageUrl"] = url
    if image_resource_id is not None:
        reply_item["imageResourceId"] = image_resource_id
    if i18n_thumbnail_image_urls is not None:
        reply_item["i18nImageUrl"] = i18n_thumbnail_image_urls
    if i18n_image_resource_ids is not None:
        reply_item["i18nImageResourceIds"] = i18n_image_resource_ids
    return reply_item


def make_quick_reply(replay_items):
    """
    Create quick reply message.

        reference
        - https://developers.worksmobile.com/jp/document/100500807?lang=en

    :param replay_items: Array of return object of make_quick_reply_item function.
    :return: quick reply content.
    """
    return {"items": replay_items}


def make_text(text, i18n_texts=None):
    """
    make text.

        reference
        - https://developers.worksmobile.com/jp/document/100500801?lang=en

    :return: text content.
    """
    if i18n_texts is not None:
        return {"type": "text", "text": text, "i18nTexts": i18n_texts}
    return {"type": "text", "text": text}


def make_i18n_image_url(language, image_url):
    return {"language": language, "imageUrl": image_url}


def make_image_carousel_column(image_url=None,
                               image_resource_id=None,
                               action=None,
                               i18n_image_urls=None,
                               i18n_image_resource_ids=None):
    """
    Create a image carousel column object.

        reference
        - https://developers.worksmobile.com/jp/document/100500809?lang=en

    :return: carousel column
    """
    column_data = {}
    if image_url is not None:
        column_data["imageUrl"] = image_url
    if image_resource_id is not None:
        column_data["imageResourceId"] = image_resource_id
    if action is not None:
        column_data["action"] = action
    if i18n_image_urls is not None:
        column_data["i18nImageUrls"] = i18n_image_urls
    if i18n_image_resource_ids is not None:
        column_data["i18nImageResourceIds"] = i18n_image_resource_ids
    return column_data


def make_image_carousel(columns):
    """
    Image Carousel:

        reference
        - https://developers.worksmobile.com/jp/document/100500809?lang=en

    Request URL
    https://apis.worksmobile.com/r/{API ID}/message/v1/bot/{botNo}/message/push

    POST (Content-Type: application / json; charset = UTF-8)

    :param columns: image carousel columns
    :return: image carousel content
    """

    return {"type": "image_carousel", "columns": columns}


def make_size(w, h):
    return {"width": w, "height": h}


def make_bound(x, y, w, h):
    return {"x": x, "y": y, "width": w, "height": h}


def make_area(bound, action):
    return {"bounds": bound, "action": action}


def make_add_rich_menu(name, size, areas):
    """
    add rich menu content:

        reference
        - https://developers.worksmobile.com/jp/document/1005040?lang=en

    You can create a rich menu for the message bot by following these steps:
    1. Image uploads: using the "Upload Content" API
    2. Rich menu generation: using the "Register Message Rich Menu" API
    3. Rich Menu Image Settings: Use the "Message Rich Menu Image Settings" API
    """

    return {"name": name, "size": size, "areas": areas}


def make_i18n_content_texts(language, content_text):
    return {"language": language, "contentText": content_text}


def make_button(text, actions, content_texts=None):
    """
    create button message content

        reference
        - https://developers.worksmobile.com/jp/document/100500804?lang=en
    """
    if content_texts is not None:
        return {"type": "button_template", "contentText": text,
                "i18nContentTexts": content_texts, "actions": actions}
    return {"type": "button_template", "contentText": text, "actions": actions}
