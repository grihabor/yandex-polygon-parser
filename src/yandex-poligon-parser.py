import argparse
from typing import Generator
import bs4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    path = args.path

    with open(path) as f:
        bs = bs4.BeautifulSoup(f, features="html.parser")
        for http_method, path in parse(bs):
            print(http_method, path)


def parse(bs: bs4.BeautifulSoup) -> Generator[tuple[str, str]]:
    resources_list = bs.find_all("ul", {"id": "resources"})
    assert len(resources_list) == 1, len(resources_list)
    resources_ul = resources_list[0]
    assert isinstance(resources_ul, bs4.PageElement), type(resources_ul)

    for resource_li in resources_ul:
        if resource_li.name != "li":
            continue

        assert isinstance(resource_li, bs4.Tag)
        _, _div, _, endpoints_ul, _ = iter(resource_li)

        assert endpoints_ul["class"] == ["endpoints"], endpoints_ul["class"]
        for endpoint_li in endpoints_ul:
            if endpoint_li.name != "li":
                continue

            assert isinstance(endpoint_li, bs4.Tag)
            assert endpoint_li["class"] == ["endpoint"], endpoint_li["class"]
            for operations_ul in endpoint_li:
                if operations_ul.name != "ul":
                    continue

                assert operations_ul["class"] == ["operations"], operations_ul["class"]

                for operation_li in operations_ul:
                    if operation_li.name != "li":
                        continue

                    assert "operation" in operation_li["class"]
                    h3 = operation_li.find("h3")
                    http_method = h3.find("span", {"class": "http_method"}).text.strip()
                    path = h3.find("span", {"class": "path"}).text.strip()
                    yield http_method, path


if __name__ == "__main__":
    main()
