-optimizationpasses 5
-overloadaggressively
-dontpreverify
-repackageclasses 'o'
-allowaccessmodification

-keep class **.R
-keep class **.R$* {
    <fields>;
}

-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

-dontwarn org.conscrypt.**
-dontwarn org.bouncycastle.**
-dontwarn org.openjsse.**
