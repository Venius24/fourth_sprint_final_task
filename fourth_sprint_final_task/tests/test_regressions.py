import pytest
from django.urls import reverse


def test_unknown_post_returns_404(client):
    response = client.get(reverse('blog:post_detail', args=[999]))
    assert response.status_code == 404


def test_category_shows_only_matching_posts(client):
    response = client.get(reverse('blog:category_posts', args=['travel']))
    assert response.status_code == 200
    assert len(response.context['filtered_posts']) == 1
    assert response.context['filtered_posts'][0]['id'] == 0
    assert 'posts/0/' in response.content.decode('utf-8')


def test_index_uses_preserved_template(client):
    response = client.get(reverse('blog:index'))
    assert response.status_code == 200
    assert any(template.name == 'blog/index2.html' for template in response.templates)


@pytest.mark.parametrize('url', [
    '/', '/posts/0/', '/category/travel/', '/pages/about/', '/pages/rules/',
])
def test_pages_have_one_doctype(client, url):
    response = client.get(url)
    assert response.status_code == 200
    assert response.content.lower().count(b'<!doctype html>') == 1
