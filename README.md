# checkbookwizard_app
An Android/IOS app made using flet to compliment my website checkbookwizard.com



#BUILD COMMAND
flet build aab \
--include-packages flet_ads \
--android-signing-key-store /Users/jamesburnison/checkbookwizard.jks \
--android-signing-key-alias wizard \
--android-signing-key-store-password "$ANDROID_SIGNING_KEY_STORE_PASSWORD" \
--android-signing-key-password "$ANDROID_SIGNING_KEY_STORE_PASSWORD" \
--android-permissions com.google.android.gms.permission.AD_ID=True