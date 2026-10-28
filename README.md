# About apkFram

**apkfram** was written in order to help any mobile penetration testers to identify the Framework used to develop the Android application.

## Usage

Print the help to get all necessary information

```bash
$ python3 apkFram.py -h
usage: apkFram.py [-h] [--file FILE] [-v]

Android Framework Identifier

optional arguments:
  -h, --help     show this help message and exit
  --file FILE    Specify your APK file
  -v, --verbose  Also print the tools needed to read the source code
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

$ python3 apkFram.py --file examples/maui.apk
[!] .NET MAUI seems to be the best answer

$ python3 apkFram.py --file examples/Unity_Loot\ Hunters.apk
[!] Unity seems to be the best probability

$ python3 apkfram.py --file examples/Apps.apk
[!] Ionic Cordova seems to be the best answer

$ python3 apkfram.py --file examples/Kony.apk
[!] Kony seems to be the best answer

$ python3 apkfram.py --file examples/Corona.apk
[!] Corona SDK seems to be the best answer
```

With `-v` / `--verbose`, apkFram also prints where the source code lives and the tools needed to read it, based on the detected framework:

```bash
$ python3 apkFram.py --file examples/net_maui.apk --verbose
[!] .NET MAUI seems to be the best answer
[*] Signals matched: libaot-Microsoft.Maui.dll.so, libaot-Microsoft.Maui.Controls.dll.so
[*] Source code location: assemblies/*.dll (plain or in assemblies.blob) or lib/<abi>/libaot-*.dll.so (AOT)
[*] Tools to read the source code:
     - ilspycmd               dotnet tool install -g ilspycmd
     - ILSpy                  brew install --cask ilspy
     - dotPeek                JetBrains dotPeek
     - pyxamstore             https://github.com/jakev/pyxamstore  (unpack assemblies.blob store)
```

The per-framework tooling is configured in `tools.json`.

Currently supported frameworks:

* Cordova/PhoneGap
* Ionic Cordova
* Flutter
* ReactNative
* ReactNative compiled with Hermes
* Unity
* Xamarin
* .NET MAUI
* Kony
* Corona SDK

## Author

Régis SENET ([rsenet](https://github.com/rsenet))


## Contributing

Bug reports and pull requests are welcome on [GitHub](https://github.com/rsenet/apkfram).

## License

The project is available as open source under the terms of the [GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html)
