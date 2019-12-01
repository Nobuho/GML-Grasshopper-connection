国土地理院の用途地域データをPythonでパースする

## Geospatial Information Authority of Japan(国土地理院) data download

[国土地理院数値情報ダウンロードサービス : Geospatial Information download service](http://nlftp.mlit.go.jp/ksj/index.html)

[用途地域データ : Site usage data](http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A29.html)

### 用途地域データの中身

| 属性名（かっこ内はshp属性名） | 説明                                            | 属性の型                           |
|-------------------------------|-------------------------------------------------|------------------------------------|
| 範囲                          | 用途地域として用途が指定された区域              | 曲面型（GM_Surface）               |
| (A29_001)行政区域コード       | 用途地域がある市区町村の行政コード              | コードリスト「行政コード」         |
| (A29_002)都道府県名           | 用途地域がある都道府県の名称                    | 文字列型(CharacterString)          |
| (A29_003)市区町村名           | 用途地域がある市区町村の名称                    | 文字列型(CharacterString)          |
| (A29_004)用途地域分類         | 用途地域分類コード                              | コードリスト「用途地域分類コード」 |
| (A29_005)用途地域名           | 用途地域の名称                                  | 文字列型(CharacterString)          |
| (A29_006)建ぺい率             | 用途地域別の建ぺい率(%)。不明の時は'9999'とする | 整数型(Decimal)                    |
| (A29_007)容積率               | 用途地域別の容積率(%)。不明の時は'9999'とする   | 整数型(Decimal)                    |
| (A29_008)総括図作成団体名     | 都市計画総括図の作成団体名                      | 文字列型(CharacterString)          |
| (A29_009)総括図作成年         | 都市計画総括図の作成年（西暦）                  | 時間型(TM_Instant)                 |
| (A29_010)備考                 | 用途地域に関する備考                            | 文字列型(CharacterString)          |

## 問題

XMLはXMLNSで名前空間が定義されている。なので下記気を付けないと通常通りPythonとlxmlでパースできない。

- 問題1
    
    `xmlns:schemaLocation` が有効なURIではないという例外が発生する。
    デフォルトで構文がおかしいのでこのエラーは無視する必要がある。

    ```python
    Exception has occurred: XMLSyntaxError
    xmlns:schemaLocation: 'http://nlftp.mlit.go.jp/ksj/schemas/ksj-app KsjAppSchema-A29-v1_0.xsd' is not a valid URI, line 7, column 94 (A29-11_27.xml, line 7)
    ```

- 問題2

    xml名前空間で name space が定義されている場合、XPATHで要素を探す際には、明示的に`namespaces=***`を指定する必要がある。

    ```python
    element = tree.xpath("/x:sample/x:rec/x:title", namespaces=mynsmap)
    ```

    参考：[トホホな疑問(13) Python、lxml、デフォルト名前空間とXPath](https://jhalfmoon.com/dbc/2019/10/20/%E3%83%88%E3%83%9B%E3%83%9B%E3%81%AA%E7%96%91%E5%95%8F13-python%E3%80%81lxml%E3%80%81%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E5%90%8D%E5%89%8D%E7%A9%BA%E9%96%93%E3%81%A8xpath/)


http://www.opengis.net/gml/3.2

http://www.w3.org/1999/xlink

ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

## 問題 : Problems

XMLはXMLNSで名前空間が定義されている。なので下記気を付けないと通常通りPythonとlxmlでパースできない。

In it xmlns(xml name space) is difined.Some 

- Problem1
    
    The URI of `xmlns:schemaLocation` is not valid originally.
    I need to ignore this exception.

    ```python
    Exception has occurred: XMLSyntaxError
    xmlns:schemaLocation: 'http://nlftp.mlit.go.jp/ksj/schemas/ksj-app KsjAppSchema-A29-v1_0.xsd' is not a valid URI, line 7, column 94 (A29-11_27.xml, line 7)
    ```

- Problem2

    It is needed to difine again in Python scripts to parse correctly.
    xlmns is difined inside of the xml, but python lxml doesn't read it correctlly.

