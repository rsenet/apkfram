# About apkFram

**apkfram** was written in order to help any mobile penetration testers to identify the Framework used to develop the Android application.

## Usage

Print the help to get all necessary information

```bash
$ python3 apkFram.py -h
usage: apkFram.py [-h] [--file FILE]

Android Framework Identifier

optional arguments:
  -h, --help   show this help message and exit
  --file FILE  Specify your APK file
```

You just have to specify the APK file in input to get the used framework:

```bash
$ python3 apkFram.py --file examples/diva.apk
[!] No framework detected

$ python3 apkFram.py --file examples/fanreact.apk
[!] Cordova/PhoneGap seems to be the best probability

$ python3 apkFram.py --file examples/flutter-app-release64.apk
[!] Flutter seems to be the best probability

$ python3 apkFram.py --file examples/ReactNative.apk
[!] ReactNative seems to be the best probability

$ python3 apkFram.py --file examples/ReactNativeHermes.apk
[!] ReactNative compiled with Hermes seems to be the best probability

$ python3 apkFram.py --file examples/tink.apk
[!] Xamarin seems to be the best probability

$ python3 apkFram.py --file examples/Unity_Loot\ Hunters.apk
[!] Unity seems to be the best probability
```

Currently supported frameworks:

* Cordova/PhoneGap
* Flutter
* Flutter in debug mode
* ReactNative
* ReactNative compiled with Hermes
* Unity
* Xamarin

## Author

Régis SENET ([rsenet](https://github.com/rsenet))


## Contributing

Bug reports and pull requests are welcome on [GitHub](https://github.com/rsenet/apkfram).

## License

The project is available as open source under the terms of the [GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html)
