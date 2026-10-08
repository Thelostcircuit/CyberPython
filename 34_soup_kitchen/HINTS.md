# HINTS // 34 SOUP KITCHEN

## page_title
<details><summary>Hint</summary>

`soup.title` is `None` when there's no title. Otherwise use `soup.title.get_text(strip=True)`.
</details>

## staff_rows
<details><summary>Hint</summary>

`table = soup.find("table", id="staff")`, then `rows = table.find_all("tr")`. Headers come from
`rows[0].find_all("th")`. For the rest, `dict(zip(headers, cell_texts))`. The last `<tr>`
isn't closed, and the parser copes.
</details>

## absolute_links
<details><summary>Hint</summary>

`soup.find_all("a", href=True)` skips anchors without an href. `urljoin(base, a["href"])`.
</details>

## texts_with_class / select_texts
<details><summary>Hint</summary>

`soup.find_all(class_=cls)` matches any tag. `soup.select(selector)` takes CSS. Use
`get_text(" ", strip=True)` on each.
</details>

## clearance_of
<details><summary>Hint</summary>

`soup.find("td", string=name)` matches the exact text (so `" I. Vale "` with spaces wouldn't
match `"I. Vale"`). Then `.find_parent("tr").find("td", class_="clearance")`.
</details>

## visible_text
<details><summary>Hint</summary>

`for tag in soup.find_all(["script", "style"]): tag.decompose()`, then
`soup.get_text(" ", strip=True)`.
</details>

## meta_tags / next_page
<details><summary>Hint</summary>

`soup.find_all("meta", attrs={"name": True})`. For the link: `soup.find("a", rel="next")`
matches even though rel is `["next", "nofollow"]`, because multi-valued attributes match any
value.
</details>
