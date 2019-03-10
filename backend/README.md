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
```json
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
- leaderのデータはmembersのデータの中にも含まれているので要注意
- サインインしたユーザーのみこれらの結果が帰ってくる

## チームの追加
<domain_name>:8080/api/teams/ (HTTP_METHOD:POST)で、以下の形式でjsonを投げることで、チームを新しく作成することができる。

## チームの編集 
## チームの削除
## メンバーの一覧の閲覧 
## メンバーの追加 
## メンバーの編集 
## メンバーの削除
