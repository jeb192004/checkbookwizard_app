import flet as ft
isAds=True
try:
    import flet_ads as ads
except ModuleNotFoundError:
    print("The module was not found.")
    isAds=False

#import flet.ads as ads
class Ads():
    def __init__(self, page:ft.Page):
        self.page = page
        self.id_banner = ("ca-app-pub-1830788262544752/7238552149" if page.platform == ft.PagePlatform.ANDROID else "ca-app-pub-1830788262544752/9353316267")

    def banner_ad(self):
        if (self.page.platform is ft.PagePlatform.ANDROID and isAds) or (self.page.platform is ft.PagePlatform.IOS and isAds):
            return ft.Container(
                content=ads.BannerAd(
                    unit_id=self.id_banner,
                    on_click=lambda e: print("BannerAd clicked"),
                    on_load=lambda e: print("BannerAd loaded"),
                    on_error=lambda e: print("BannerAd error", e.data),
                    on_open=lambda e: print("BannerAd opened"),
                    on_close=lambda e: print("BannerAd closed"),
                    on_impression=lambda e: print("BannerAd impression"),
                    on_will_dismiss=lambda e: print("BannerAd will dismiss"),
                ),
                #width=320,
                height=50,
                bgcolor=ft.Colors.TRANSPARENT,
                alignment=ft.alignment.top_center,
                expand=True,
                margin=ft.margin.only(top=5)
            )
        else:
            return ft.Container(height=0, visible=False)