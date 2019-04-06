# スポーツ大会バックエンド
このシステムを使って、
- チームの
    - 一覧の閲覧 /api/teams/ (GET)
    - 追加 /api/teams/ (POST)
    - 編集 /api/teams/<team_pk>/ (PUT)
    - 削除 /api/teams/<team_pk>/ (DELETE)
- チームに所属するメンバーの
    - 一覧の閲覧 /api/teams/<team_pk>/members/ (GET)
    - 追加 /api/teams/<team_pk>/members/ (POST)
    - 編集 /api/teams/<team_pk>/members/<member_pk>/ (PUT)
    - 削除 /api/teams/<team_pk>/members/<member_pk>/ (DELETE)

を行うことができる。
また、Google Sign inを利用した、ログイン、ログアウトもできる。

## チーム一覧の閲覧
<domain_name>:8080/api/teams/ (HTTP_METHOD:GET)で、以下のような形式のデータが得られる。
```
[ //チームのリスト
    {
        "pk": 4, //チーム番号
        "name": "test", //チーム名
        "event": "Tennis", //競技種目
        "leader": { //リーダーの情報
            "pk": 22, //リーダー番号
            "name": "hako", //リーダーの名前
            "email": "c011199999@edu.teu.ac.jp", //メールアドレス
            "experience": false, //競技種目の経験があるか
            "team": "test" //所属チーム名
        },
        "members": [ //メンバーたちの情報、形式はリーダーと同じ
            {
                "pk": 22, //リーダー
                "name": "hako",
                "email": "c011199999@edu.teu.ac.jp",
                "experience": false,
                "team": "test"
            },
            { //上記のようにメンバーたちの情報が続く
             ...
            },
            ...
        ]
    },
    { //上記のようにチームの情報が続く
    ....
    },
]
```
### 注意点
- leaderのデータはmembersのデータの中にも含まれている
- サインインしたユーザーのみこれらの結果が帰ってくる

## チームの追加
<domain_name>:8080/api/teams/ (HTTP_METHOD:POST)に以下の形式でjsonを投げることで、チームを新しく作成することができる。
```
{
   "name": "test", //チーム名
   "event": "Tennis", //競技種目
   "leader": { //リーダーの情報
       "name": "hako", //名前
       "email": "c011199999@edu.teu.ac.jp", //メールアドレス
       "experience": false //競技種目の経験があるか
   },
   "members": [ //メンバーたちの情報　リーダーの情報と形式は同じ
       {
           "name": "hakomori",
           "email": "c011199999@edu.teu.ac.jp",
           "experience": true
       },
       { //以下にメンバーの情報が続く
       ...
       },
       ...
   ]
}
```
### 注意点
- サインインが必要
- eventに設定する値は、backend/sportsfes/api/models.pyのTeamクラス冒頭で宣言されている定数の中からその値を使う
- leaderの情報はmembersに繰り返し書かなくても、メンバーに入る。（GETすると、leaderもmembersに入っている）
- leader含めたチームのメンバーの人数が、設定した競技種目の最少人数以上、最多人数以下にならないとExceptionがかえってくる。
    - 各競技種目の最少人数、最多人数はbackend/sportsfes/sportsfes/settings.pyに設定してある。
- 初心者、経験者混合の場合、全員が経験者、もしくは、全員が初心者の場合Exceptionがかえってくる。
    - 初心者、経験者混合であるかは、backend/sportsfes/sportsfes/settings.pyに設定してある。
    
## チームの編集
<domain_name>:8080/api/teams/<team_pk:int>/ (HTTP_METHOD:PUT)に、以下の形式でデータを投げると、チームの情報を変更できる。
なお、<team_pk:int>には、編集したいチームのチーム番号を入れる (e.g. <domain_name>:8080/api/teams/1/)

```
{
   "name": "test", //チーム名
   "event": "Tennis", //競技種目
   "leader": { //リーダーの情報
       "name": "hako", //名前
       "email": "c011199999@edu.teu.ac.jp", //メールアドレス
       "experience": false //競技種目の経験があるかどうか
   },
   "members": [ //メンバーの情報 形式はリーダーと同じ 
       {
           "name": "hakomori",
           "email": "c011199999@edu.teu.ac.jp",
           "experience": true
       },
       {
        ...
       },
       ...
   ]
}
```
### 注意点
- 基本的な注意点は(チームの追加)の注意点と同じ
- チームの情報を編集できるのは、チームを作成したユーザーのみ
- membersの更新は完全な作り直しであるため、一括でチームのメンバーを変えたいときにおすすめ
- メンバーの情報を一人ひとり編集したい、もしくは、一人だけ削除、追加したいのなら、/api/teams/<team_pk>/members/<member_pk>/ですることをおすすめする
- リーダー以外のメンバーの情報を編集しない場合、以下のようにmembers:を省略できる
```
{
   "name": "test",
   "event": "Tennis",
   "leader": {
       "name": "hako",
       "email": "c011199999@edu.teu.ac.jp",
       "experience": false
   }
}
```
## チームの削除
<domain_name>:8080/api/teams/<team_pk>/ (HTTP_METHOD:DELETE)で、チーム番号<team_pk>のチームを削除することができる。

### 注意点
- チームの削除に伴い、そのチームに所属するリーダー、メンバーの情報もすべて消える
## メンバーの一覧の閲覧
<domain_name>:8080/api/teams/<team_pk>/members/ (HTTP_METHOD:GET)で、チーム番号<team_pk>に所属するチームの一覧が得られる。
```
[ //チームに所属するメンバーのリスト
    {
        "pk": 30, //メンバー番号
        "name": "yu", //名前
        "email": "e011199999@edu.teu.ac.jp", //メールアドレス
        "experience": true, //競技種目の経験があるか
        "team": "test" //所属チーム名
    },
    {
    ...
    },
    ...
]
```

### 注意点
- 閲覧にはサインインが必要
- このデータにはリーダーのデータも含まれている
## メンバーの追加 
<domain_name>:8080/api/teams/<team_pk>/members/ (HTTP_METHOD:POST)に以下の形式でjsonを投げることで、チーム番号<team_pk>のチームにメンバーを一人追加できる。
```
{ //メンバーの情報
    "name": "test", //名前
    "email": "e011199999@edu.teu.ac.jp", //メールアドレス
    "experience": false //競技種目の経験があるか
}
```

### 注意点
- サインインしていること、サインインしているユーザーが、メンバーが所属するチームを作成したユーザーであることが必要である
- メンバーの追加によって、競技種目の、１チームあたりのエントリー可能最多人数を超えた場合、Exceptionがかえってくる。
## メンバーの編集
<domain_name>:8080/api/teams/<team_pk>/members/<member_pk>/ (HTTP_METHOD:PUT)に、以下の形式でjsonを投げることで、チーム番号<team_pk>のチームに所属する、メンバー番号<member_pk>のメンバーの情報を更新することができる。
```
{ //メンバーの情報
    "name": "test", //名前
    "email": "c011199999@edu.teu.ac.jp", //メールアドレス
    "experience": false //競技種目の経験があるか
}
```

### 注意点
- サインインしていること、サインインしているユーザーが、メンバーが所属するチームを作成したユーザーであることが必要である。
- 競技種目が経験者、初心者混合の場合であり、このメンバーの情報の変更によってチームに経験者のみ、もしくは、初心者のみになってしまう場合、Exceptionを返す。
## メンバーの削除
<domain_name>:8080/api/teams/<team_pk>/members/<member_pk>/ (HTTP_METHOD:DELETE)で、チーム番号<team_pk>のチームに所属する、メンバー番号<member_pk>のメンバーを削除できる。

### 注意点
メンバーの削除によって、出場種目の１チームあたりのエントリー可能最少人数を下回るとき、Exceptionがかえる。

## Google Sign in
- <domain_name>:8080/api/ (HTTP_METHOD:GET)で、サインイン、サインアウト画面のサンプルに飛ぶ。
- サインインすることにより、バックエンドとsessionを用いたAuthenticationを行うことができる。
- ログイン時に、<domain_name>:8080/api/tokensignin (HTTP_METHOD:POST)で、tokenidを投げている
- ログアウト時に、<domain_name>:8080/api/tokenlogou (HTTP_METHOD:POST)を叩いている。
### 注意点
- googleのapiとしてのsignin、logout,backendとしてのsignin、logoutをサインイン、サインアウト時に一気にやっている。
- セッションが始まっているかは、Cookieにsessionidがあるかどうかを確認することでわかる。
- 基本、[ここ](https://developers.google.com/identity/sign-in/web/sign-in)にそって実装しているので、なにか困ったことがあればここを参照
