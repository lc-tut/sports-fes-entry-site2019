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
            "email": "yuhaco0725@gmail.com", //メールアドレス
            "grade": 3, //学年
            "experience": false, //競技種目の経験があるか
            "team": "test" //所属チーム名
        },
        "members": [ //メンバーたちの情報、形式はリーダーと同じ
            {
                "pk": 22, //リーダー
                "name": "hako",
                "email": "yuhaco0725@gmail.com",
                "grade": 3,
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
<domain_name>:8080/api/teams/ (HTTP_METHOD:POST)で、以下の形式でjsonを投げることで、チームを新しく作成することができる。
```
{
   "name": "test", //チーム名
   "event": "Tennis", //競技種目
   "leader": { //リーダーの情報
       "name": "hako", //名前
       "email": "yuhaco0725@gmail.com", //メールアドレス
       "grade": 3, //学年
       "experience": false //競技種目の経験があるか
   },
   "members": [ //メンバーたちの情報　リーダーの情報と形式は同じ
       {
           "name": "hakomori",
           "email": "hakomori64@gmail.com",
           "grade": 1,
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
- gradeに設定する値は、backend/sportsfes/api/models.pyのMemberクラス冒頭で宣言されているGRADEのなかの数値の中から使う
- leaderの情報はmembersに繰り返し書かなくても、メンバーに入る。（GETすると、leaderもmembersに入っている）
- leader含めたチームのメンバーの人数が、設定した競技種目の最低人数以上、最大人数以内にならないとExceptionがかえってくる。
## チームの編集
## チームの削除
## メンバーの一覧の閲覧 
## メンバーの追加 
## メンバーの編集 
## メンバーの削除
