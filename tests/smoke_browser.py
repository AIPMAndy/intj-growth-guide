"""Optional interactive browser smoke check (pip install playwright && playwright install chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
index=(ROOT/"index.html").read_text(encoding="utf-8")
plan=(ROOT/"plan.html").read_text(encoding="utf-8")
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width in (1440,390):
        page=browser.new_page(viewport={"width":width,"height":900 if width==1440 else 844})
        errors=[]
        page.on("pageerror",lambda err:errors.append(str(err)))
        page.set_content(index)
        assert page.locator(".work-card").count()==41
        assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
        page.locator("#search").fill("Deep Work")
        assert page.locator(".work-card").count()==1
        page.locator("#resetFilters").click()
        page.locator('[data-kind="film"]').click()
        assert page.locator(".work-card").count()==12
        page.locator("#resetFilters").click()
        page.locator(".work-card").first.locator("[data-fav]").click()
        page.locator('[data-mode="favorites"]').click()
        assert page.locator(".work-card").count()==1
        page.locator("#resetFilters").click()
        page.locator(".work-card").first.locator("[data-detail]").click()
        assert page.locator("#detailDialog").evaluate("e=>e.open")
        page.locator("[data-close-detail]").click()
        assert not errors,errors
        print("PASS homepage",width)
        page.close()
    page=browser.new_page(viewport={"width":390,"height":844},accept_downloads=True)
    page.set_content(plan)
    assert page.locator("input[data-task]").count()==21
    page.locator("input[data-task]").first.check()
    assert page.locator("#dayStatus").inner_text()=="1 / 21 已完成"
    with page.expect_download() as downloaded:
        page.locator("#export").click()
    assert downloaded.value.suggested_filename.endswith(".md")
    print("PASS interactive planner")
    page.close()
    browser.close()
