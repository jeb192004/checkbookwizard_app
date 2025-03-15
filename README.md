# checkbookwizard_app
An Android/IOS app made using flet to compliment my website checkbookwizard.com



#BUILD ANDROID COMMAND
flet build aab \
--android-signing-key-store /Users/jamesburnison/checkbookwizard.jks \
--android-signing-key-alias wizard \
--android-signing-key-store-password "$ANDROID_SIGNING_KEY_STORE_PASSWORD" \
--android-signing-key-password "$ANDROID_SIGNING_KEY_STORE_PASSWORD" 

flet build apk && adb install build/apk/app-release.apk && adb shell monkey -p com.burnison.me.checkbook_wizard 1

#BUILD IOS COMMAND
flet build ipa