# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in D:\AndroidSDK/tools/proguard/proguard-android.txt
# You can edit the include path and order by changing the proguardFiles
# directive in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Add any project specific keep options here:

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Android Support Library
-keep class !android.support.v7.internal.view.menu.**,android.support.** {*;}
-keep class android.support.v7.graphics.** { *; }
-dontwarn android.support.v7.graphics.**

-keep class android.support.design.widget.** { *; }
-keep interface android.support.design.widget.** { *; }
-dontwarn android.support.design.**

# Keep the source line when using ProGuard
-renamesourcefileattribute SourceFile
-keepattributes SourceFile,LineNumberTable

# LoganSquare JSON parser
-keep class com.bluelinelabs.logansquare.** { *; }
-keep @com.bluelinelabs.logansquare.annotation.JsonObject class *
-keep class **$$JsonObjectMapper { *; }

# Java 8
-dontwarn java.lang.invoke.*
-dontwarn **$$Lambda$*

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
-dontwarn javax.annotation.**
