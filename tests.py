import os
import pages
from conftest import browser


def test_task_1(browser) -> None:
    page = pages.Page(browser)
    page.get_base_page()
    page.go_to_contacts()
    page.go_to_tensor()
    assert page.get_title() == 'Сила в людях'
    page.go_to_about()
    assert browser.current_url == 'https://tensor.ru/about'
    photo = page.get_photo()
    assert photo[0] == photo[1] == photo[2] == photo[3]


def test_task_2(browser) -> None:
    page = pages.Page(browser)
    page.get_base_page()
    page.go_to_contacts()
    assert page.get_location() == 'Тюменская обл.'
    assert len(page.get_partners()) > 1
    page.set_location()
    assert page.get_location() == 'Камчатский край'
    assert page.get_partners()[0].text == 'Петропавловск-Камчатский'
    assert '41-kamchatskij-kraj' in page.get_current_url()
    assert 'Камчатский край' in page.get_page_title()


def test_task_3(browser) -> None:
    page = pages.Page(browser)
    page.get_base_page()
    name = page.download_plugin()
    page.download_waiting(name)
    assert os.path.isfile(name)
    assert page.plugin_size() == round(os.path.getsize(name) / 1024 / 1024, 2)
